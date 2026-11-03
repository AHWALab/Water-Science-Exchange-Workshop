"""
qpe_tools.py

Small helper functions for the QPE module of the flash flood workshop
(CUAHSI Water Science Exchange 2026, University of Iowa).

Everything here is plain Python. Read the function you are about to use,
the comments explain each step. The notebooks import this file with

    from qpe_tools import *

Data sources covered
    MRMS            NOAA Multi-Radar Multi-Sensor, AWS bucket noaa-mrms-pds
                    and the Iowa State University mtarchive mirror
    Stage IV        NCEP multi-sensor analysis, Iowa Environmental Mesonet archive
    IEM             Iowa Environmental Mesonet web services (ASOS, ISU Soil
                    Moisture Network, CoCoRaHS, station metadata)
    USCRN           NOAA NCEI U.S. Climate Reference Network text files
    GOES RRQPE      Satellite rainfall rate (SCaMPR) from the NOAA GOES bucket
    NLDI            USGS Network Linked Data Index, basin boundaries
"""

import gzip
import io
import os
import tempfile
import datetime as dt

import numpy as np
import pandas as pd
import xarray as xr
import requests
import eccodes as ec

# ----------------------------------------------------------------------------
# 1. Constants
# ----------------------------------------------------------------------------

MRMS_AWS = "https://noaa-mrms-pds.s3.amazonaws.com/CONUS"
MRMS_ISU = "https://mtarchive.geol.iastate.edu"
IEM = "https://mesonet.agron.iastate.edu"
USCRN_HOURLY = "https://www.ncei.noaa.gov/pub/data/uscrn/products/hourly02"
NLDI = "https://api.water.usgs.gov/nldi/linked-data/nwissite"

# Short name used in the notebooks  ->  folder name in the AWS bucket.
# The "_00.00" suffix is the product height tag that AWS keeps in the name.
MRMS_PRODUCTS = {
    "PrecipRate":  "PrecipRate_00.00",
    "RadarOnly":   "RadarOnly_QPE_01H_00.00",
    "Pass1":       "MultiSensor_QPE_01H_Pass1_00.00",
    "Pass2":       "MultiSensor_QPE_01H_Pass2_00.00",
    "GII_Pass1":   "GaugeInflIndex_01H_Pass1_00.00",
    "GII_Pass2":   "GaugeInflIndex_01H_Pass2_00.00",
    "RQI":         "RadarQualityIndex_00.00",
    "RadarOnly24": "RadarOnly_QPE_24H_00.00",
    "Pass2_24":    "MultiSensor_QPE_24H_Pass2_00.00",
}

# Products mirrored by Iowa State (a subset of the AWS list, no Pass 1).
MRMS_ISU_DIRS = {
    "PrecipRate":  "PrecipRate",
    "RadarOnly":   "RadarOnly_QPE_01H",
    "Pass2":       "MultiSensor_QPE_01H_Pass2",
    "RadarOnly24": "RadarOnly_QPE_24H",
    "Pass2_24":    "MultiSensor_QPE_24H_Pass2",
}

# Readable labels for plots.
LABELS = {
    "RadarOnly": "Radar only",
    "Pass1": "Multi-sensor Pass 1",
    "Pass2": "Multi-sensor Pass 2",
    "GII_Pass1": "Gauge influence, Pass 1",
    "GII_Pass2": "Gauge influence, Pass 2",
}

# A rainfall colour scale close to the one used on NWS maps (mm).
RAIN_LEVELS = [0.2, 1, 2.5, 5, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200, 300]
RAIN_COLORS = ["#e8f4ff", "#b7e0ff", "#7fc6ff", "#3f9bff", "#1f5fd8", "#00c853",
               "#7cd63a", "#ffff33", "#ffd21f", "#ff9c00", "#ff5500", "#e60000",
               "#b3001b", "#8a0073", "#d04ad6", "#ffffff"]


def rain_cmap():
    """Return (cmap, norm) for rainfall maps in mm. Use with pcolormesh."""
    from matplotlib.colors import ListedColormap, BoundaryNorm
    cmap = ListedColormap(RAIN_COLORS[:len(RAIN_LEVELS) + 1])
    cmap.set_under("white")
    norm = BoundaryNorm([0] + RAIN_LEVELS, cmap.N, extend="max")
    return cmap, norm


# ----------------------------------------------------------------------------
# 2. MRMS, download and decode
# ----------------------------------------------------------------------------

def to_timestamp(when):
    """Accept '2024-06-22 04:00', a datetime or a pandas Timestamp. Return a Timestamp in UTC."""
    t = pd.Timestamp(when)
    return t.tz_localize("UTC") if t.tzinfo is None else t.tz_convert("UTC")


def mrms_url(product, when, source="aws"):
    """Build the download link of one MRMS file.

    AWS layout
        CONUS/<PRODUCT>/<YYYYMMDD>/MRMS_<PRODUCT>_<YYYYMMDD>-<HHMMSS>.grib2.gz
    Iowa State layout
        <YYYY>/<MM>/<DD>/mrms/ncep/<PRODUCT>/<PRODUCT>_00.00_<YYYYMMDD>-<HHMMSS>.grib2.gz
    """
    t = to_timestamp(when)
    stamp = t.strftime("%Y%m%d-%H%M%S")
    if source == "aws":
        name = MRMS_PRODUCTS[product]
        return f"{MRMS_AWS}/{name}/{t:%Y%m%d}/MRMS_{name}_{stamp}.grib2.gz"
    if source == "iastate":
        if product not in MRMS_ISU_DIRS:
            raise ValueError(f"{product} is not mirrored at Iowa State. Use source='aws'.")
        folder = MRMS_ISU_DIRS[product]
        return f"{MRMS_ISU}/{t:%Y/%m/%d}/mrms/ncep/{folder}/{folder}_00.00_{stamp}.grib2.gz"
    raise ValueError("source must be 'aws' or 'iastate'")


def decode_grib2(raw_bytes):
    """Decode one GRIB2 message (already decompressed) with ecCodes.

    Returns an xarray DataArray with latitude and longitude coordinates
    and the valid time stored in the attributes.

    Why ecCodes directly and not cfgrib? The national MRMS grid has
    3500 x 7000 points. cfgrib takes about 10 s per file to build its
    index, ecCodes reads the values in well under a second.
    """
    h = ec.codes_new_from_message(raw_bytes)
    try:
        ni = ec.codes_get(h, "Ni")                 # number of columns (longitude)
        nj = ec.codes_get(h, "Nj")                 # number of rows (latitude)
        lat1 = ec.codes_get(h, "latitudeOfFirstGridPointInDegrees")
        lon1 = ec.codes_get(h, "longitudeOfFirstGridPointInDegrees")
        dlat = ec.codes_get(h, "jDirectionIncrementInDegrees")
        dlon = ec.codes_get(h, "iDirectionIncrementInDegrees")
        date = ec.codes_get(h, "dataDate")         # YYYYMMDD
        time = ec.codes_get(h, "dataTime")         # HHMM
        values = ec.codes_get_values(h).reshape(nj, ni).astype("float32")
    finally:
        ec.codes_release(h)

    # MRMS rows run from north to south, columns from west to east.
    lat = lat1 - dlat * np.arange(nj)
    lon = lon1 + dlon * np.arange(ni)
    lon = np.where(lon > 180, lon - 360, lon)      # 230..300 E  ->  -130..-60

    valid = pd.Timestamp(f"{date:08d}{time:04d}", tz="UTC")
    da = xr.DataArray(values, dims=("lat", "lon"), coords={"lat": lat, "lon": lon})
    da.attrs["valid_time"] = valid.isoformat()
    return da


def clip(da, bbox):
    """Cut a lat/lon DataArray to bbox = (west, east, south, north)."""
    west, east, south, north = bbox
    lat_slice = slice(north, south) if da.lat[0] > da.lat[-1] else slice(south, north)
    return da.sel(lat=lat_slice, lon=slice(west, east))


def read_mrms(product, when, bbox, source="aws", cache_dir="../data/cache/mrms", refresh=False, save_cache=True):
    """Download one MRMS file, decode it, clip it to bbox, return a DataArray in mm.

    Steps
        1. look for a cached copy of the clipped field (fast, works offline)
        2. download the .grib2.gz file (about 1 MB)
        3. decompress and decode
        4. mask negative values (-1 missing, -3 no coverage) and clip
        5. save the clipped field to the cache

    refresh=True forces a new download. save_cache=False leaves the cache untouched.
    """
    t = to_timestamp(when)
    os.makedirs(cache_dir, exist_ok=True)
    tag = "_".join(f"{v:.2f}" for v in bbox).replace("-", "m")
    cache_file = os.path.join(cache_dir, f"{product}_{t:%Y%m%d-%H%M}_{tag}.nc")

    if os.path.exists(cache_file) and not refresh:                  # step 1
        with xr.open_dataarray(cache_file) as cached:
            return cached.load()

    url = mrms_url(product, t, source)                              # step 2
    r = requests.get(url, timeout=120)
    if r.status_code == 404:
        raise FileNotFoundError(f"No file at {url}")
    r.raise_for_status()

    da = decode_grib2(gzip.decompress(r.content))                   # step 3
    da = clip(da.where(da >= 0), bbox)                              # step 4
    da.name = product
    da.attrs.update(product=product, source=source, units="mm",
                    long_name=LABELS.get(product, product))

    if save_cache:                                                  # step 5
        tmp = cache_file + ".tmp"
        da.to_netcdf(tmp, encoding={product: {"zlib": True, "complevel": 4}})
        os.replace(tmp, cache_file)
    return da


def read_mrms_series(product, times, bbox, source="aws", verbose=True, **kw):
    """Read many hourly files and stack them along a time axis."""
    fields = []
    for i, t in enumerate(times):
        try:
            fields.append(read_mrms(product, t, bbox, source=source, **kw))
        except FileNotFoundError:
            if verbose:
                print("missing", product, t)
            continue
        if verbose and (i + 1) % 6 == 0:
            print(f"{product}: {i + 1}/{len(times)} files")
    out = xr.concat(fields, dim="time")
    out["time"] = pd.to_datetime([f.attrs["valid_time"] for f in fields]).tz_localize(None)
    out.name = product
    return out


def mrms_upload_latency(product, day):
    """Measure the real latency of an MRMS product from the archive itself.

    Every object in the AWS bucket carries an upload time (LastModified).
    Upload time minus valid time tells us how long after the hour the
    file became available. Returns a DataFrame for the top-of-hour files.
    """
    import s3fs
    fs = s3fs.S3FileSystem(anon=True)
    t = to_timestamp(day)
    objects = fs.ls(f"noaa-mrms-pds/CONUS/{MRMS_PRODUCTS[product]}/{t:%Y%m%d}", detail=True)
    rows = []
    for o in objects:
        name = o["name"].split("/")[-1]
        if not name.endswith(".grib2.gz"):
            continue
        stamp = name.split("_")[-1].replace(".grib2.gz", "")      # YYYYMMDD-HHMMSS
        valid = pd.Timestamp(f"{stamp[:8]} {stamp[9:11]}:{stamp[11:13]}", tz="UTC")
        uploaded = pd.Timestamp(o["LastModified"])
        rows.append((valid, uploaded, (uploaded - valid).total_seconds() / 60))
    df = pd.DataFrame(rows, columns=["valid_time", "uploaded", "latency_min"])
    df = df[df.valid_time.dt.minute == 0].reset_index(drop=True)
    df.insert(0, "product", product)
    return df


# ----------------------------------------------------------------------------
# 3. Stage IV (NCEP) from the Iowa Environmental Mesonet archive
# ----------------------------------------------------------------------------

def read_stage4(when, bbox, cache_dir="../data/cache/stage4"):
    """Read one hourly Stage IV file and return the cells inside bbox.

    Stage IV is on the HRAP polar stereographic grid (about 4 km), so the
    result is a 2-D field with 2-D latitude and longitude arrays, not a
    regular lat/lon grid like MRMS.
    """
    t = to_timestamp(when)
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"stage4_{t:%Y%m%d%H}.nc")
    if os.path.exists(cache_file):
        with xr.open_dataset(cache_file) as cached:
            return cached.load()

    url = f"{IEM}/archive/data/{t:%Y/%m/%d}/stage4/ST4.{t:%Y%m%d%H}.01h.grib"
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    with tempfile.NamedTemporaryFile(suffix=".grib2", delete=False) as f:
        f.write(r.content)
        path = f.name
    try:
        ds = xr.open_dataset(path, engine="cfgrib", backend_kwargs={"indexpath": ""})
        tp = ds["tp"].load()                                   # total precipitation, kg m-2 = mm
    finally:
        os.remove(path)

    lon = np.where(ds.longitude.values > 180, ds.longitude.values - 360, ds.longitude.values)
    lat = ds.latitude.values
    west, east, south, north = bbox
    inside = (lon >= west) & (lon <= east) & (lat >= south) & (lat <= north)
    rows = np.where(inside.any(axis=1))[0]
    cols = np.where(inside.any(axis=0))[0]
    sub = xr.Dataset(
        {"precip": (("y", "x"), tp.values[rows.min():rows.max() + 1, cols.min():cols.max() + 1])},
        coords={"lat": (("y", "x"), lat[rows.min():rows.max() + 1, cols.min():cols.max() + 1]),
                "lon": (("y", "x"), lon[rows.min():rows.max() + 1, cols.min():cols.max() + 1])},
        attrs={"valid_time": t.isoformat(), "units": "mm", "grid": "HRAP polar stereographic, about 4 km"},
    )
    sub.to_netcdf(cache_file)
    return sub


# ----------------------------------------------------------------------------
# 4. Gauges from the Iowa Environmental Mesonet (IEM)
# ----------------------------------------------------------------------------

def iem_stations(network, bbox=None, active=True):
    """Station list of one IEM network (for example 'IA_ASOS', 'ISUSM', 'IA_COCORAHS', 'USCRN').

    active=True keeps only stations that are still reporting (no archive end date).
    """
    r = requests.get(f"{IEM}/api/1/network/{network}.geojson", timeout=60)
    r.raise_for_status()
    rows = []
    for f in r.json()["features"]:
        p = f["properties"]
        lon, lat = f["geometry"]["coordinates"]
        rows.append({"station": p["id"], "name": p["name"], "lon": lon, "lat": lat,
                     "network": network, "archive_end": p.get("archive_end")})
    df = pd.DataFrame(rows)
    if active:
        df = df[df.archive_end.isna()]
    if bbox is not None:
        west, east, south, north = bbox
        df = df[(df.lon >= west) & (df.lon <= east) & (df.lat >= south) & (df.lat <= north)]
    return df.reset_index(drop=True)


def iem_asos_hourly(stations, start, end):
    """Hourly precipitation from ASOS and AWOS airports (routine METAR reports).

    The METAR field p01i is the precipitation of the past hour in inches.
    Routine reports are issued a few minutes before the hour (for example
    04:55), so we round the time up to the hour they represent.
    Returns a DataFrame with columns station, valid_time (hour ending), mm.
    """
    t0, t1 = to_timestamp(start), to_timestamp(end)
    t1_request = t1 + pd.Timedelta(days=1)          # the IEM end date is exclusive, so ask for one more day
    params = [("data", "p01i"), ("tz", "Etc/UTC"), ("format", "onlycomma"),
              ("latlon", "yes"), ("missing", "empty"), ("trace", "0.0001"),
              ("direct", "no"), ("report_type", "3"),
              ("year1", t0.year), ("month1", t0.month), ("day1", t0.day),
              ("year2", t1_request.year), ("month2", t1_request.month), ("day2", t1_request.day)]
    params += [("station", s) for s in stations]
    r = requests.get(f"{IEM}/cgi-bin/request/asos.py", params=params, timeout=120)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df["valid"] = pd.to_datetime(df["valid"], utc=True)
    df["valid_time"] = df["valid"].dt.ceil("h")
    df["mm"] = pd.to_numeric(df["p01i"], errors="coerce") * 25.4
    df = df[(df.valid_time > t0) & (df.valid_time <= t1)]
    df = df.groupby(["station", "valid_time"], as_index=False).agg(mm=("mm", "max"),
                                                                   lon=("lon", "first"),
                                                                   lat=("lat", "first"))
    df["network"] = "ASOS"
    return df


def iem_isusm_hourly(stations, start, end):
    """Hourly rainfall from the ISU Soil Moisture Network (tipping bucket gauges)."""
    t0, t1 = to_timestamp(start), to_timestamp(end)
    t1_request = t1 + pd.Timedelta(hours=1)          # the IEM end time is exclusive, so ask for one more hour
    params = [("mode", "hourly"), ("vars", "rain_in_tot"), ("format", "comma"), ("tz", "UTC"),
              ("sts", t0.strftime("%Y-%m-%dT%H:%MZ")), ("ets", t1_request.strftime("%Y-%m-%dT%H:%MZ"))]
    params += [("station", s) for s in stations]
    r = requests.get(f"{IEM}/cgi-bin/request/isusm.py", params=params, timeout=120)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df["valid_time"] = pd.to_datetime(df["valid"], utc=True)
    df["mm"] = pd.to_numeric(df["rain_in_tot"], errors="coerce") * 25.4
    df = df[(df.valid_time > t0) & (df.valid_time <= t1)][["station", "valid_time", "mm"]]
    df["network"] = "ISUSM"
    return df.reset_index(drop=True)


def iem_cocorahs_daily(network, date):
    """Daily CoCoRaHS reports (volunteer 4 inch gauges, read near 7 am local time).

    Returns one row per station with lon, lat and the 24 h total in mm.
    The date is the morning the gauge was read.
    """
    t = to_timestamp(date)
    r = requests.get(f"{IEM}/api/1/daily.json", params={"network": network, "date": t.strftime("%Y-%m-%d")},
                     timeout=120)
    r.raise_for_status()
    df = pd.DataFrame(r.json()["data"])[["station", "name", "precip"]]
    meta = iem_stations(network)[["station", "lon", "lat"]]
    df = df.merge(meta, on="station", how="inner")
    df["mm"] = pd.to_numeric(df["precip"], errors="coerce") * 25.4
    df["network"] = "CoCoRaHS"
    return df.dropna(subset=["mm"]).reset_index(drop=True)


def load_or_fetch(csv_file, fetch, cache_dir="../data/cache/gauges"):
    """Read a table from the local cache if it exists, otherwise call fetch() and save it.

    Example
        asos = load_or_fetch("asos_event.csv", lambda: iem_asos_hourly(ids, t0, t1))
    The cache lets the notebook run without internet access.
    """
    os.makedirs(cache_dir, exist_ok=True)
    path = os.path.join(cache_dir, csv_file)
    if os.path.exists(path):
        df = pd.read_csv(path)
        if "valid_time" in df.columns:
            df["valid_time"] = pd.to_datetime(df["valid_time"], utc=True)
        return df
    df = fetch()
    df.to_csv(path, index=False)
    return df


# ----------------------------------------------------------------------------
# 5. USCRN from NOAA NCEI
# ----------------------------------------------------------------------------

USCRN_COLUMNS = ["WBANNO", "UTC_DATE", "UTC_TIME", "LST_DATE", "LST_TIME", "CRX_VN", "LONGITUDE",
                 "LATITUDE", "T_CALC", "T_HR_AVG", "T_MAX", "T_MIN", "P_CALC", "SOLARAD",
                 "SOLARAD_FLAG", "SOLARAD_MAX", "SOLARAD_MAX_FLAG", "SOLARAD_MIN", "SOLARAD_MIN_FLAG",
                 "SUR_TEMP_TYPE", "SUR_TEMP", "SUR_TEMP_FLAG", "SUR_TEMP_MAX", "SUR_TEMP_MAX_FLAG",
                 "SUR_TEMP_MIN", "SUR_TEMP_MIN_FLAG", "RH_HR_AVG", "RH_HR_AVG_FLAG",
                 "SOIL_MOISTURE_5", "SOIL_MOISTURE_10", "SOIL_MOISTURE_20", "SOIL_MOISTURE_50",
                 "SOIL_MOISTURE_100", "SOIL_TEMP_5", "SOIL_TEMP_10", "SOIL_TEMP_20", "SOIL_TEMP_50",
                 "SOIL_TEMP_100"]


def uscrn_hourly(station_file, year, start=None, end=None):
    """Hourly precipitation (P_CALC, mm) from one USCRN station text file.

    station_file is the station part of the NCEI file name, for example
    'SD_Sioux_Falls_14_NNE'. Times are the end of the observed hour (UTC).
    """
    url = f"{USCRN_HOURLY}/{year}/CRNH0203-{year}-{station_file}.txt"
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text), sep=r"\s+", header=None, names=USCRN_COLUMNS, dtype={"UTC_DATE": str, "UTC_TIME": str})
    df["valid_time"] = pd.to_datetime(df["UTC_DATE"] + df["UTC_TIME"], format="%Y%m%d%H%M", utc=True)
    df["mm"] = df["P_CALC"].where(df["P_CALC"] >= 0)        # -9999 means missing
    df["station"] = station_file
    df["lon"], df["lat"] = df["LONGITUDE"], df["LATITUDE"]
    if start is not None:
        df = df[df.valid_time > to_timestamp(start)]
    if end is not None:
        df = df[df.valid_time <= to_timestamp(end)]
    df["network"] = "USCRN"
    return df[["station", "valid_time", "mm", "lon", "lat", "network"]].reset_index(drop=True)


# ----------------------------------------------------------------------------
# 6. GOES satellite rainfall rate (SCaMPR, product ABI-L2-RRQPEF)
# ----------------------------------------------------------------------------

def read_goes_rrqpe(when, bbox, satellite="goes16", step_deg=0.02, cache_dir="../data/cache/goes"):
    """Read the GOES rainfall rate scan closest to 'when' and put it on a lat/lon grid.

    GOES data sit on the satellite's own view geometry, so we
        1. find the file for that 10 minute scan in the AWS bucket
        2. compute longitude and latitude of each pixel with the geostationary projection
        3. keep pixels inside bbox and interpolate them to a regular grid
    Returns a DataArray of rain rate in mm per hour.
    """
    import s3fs
    from pyproj import Proj
    from scipy.interpolate import griddata

    t = to_timestamp(when)
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"rrqpe_{satellite}_{t:%Y%m%d-%H%M}.nc")
    if os.path.exists(cache_file):
        with xr.open_dataarray(cache_file) as cached:
            return cached.load()
    fs = s3fs.S3FileSystem(anon=True)
    doy = t.timetuple().tm_yday
    files = sorted(fs.glob(f"noaa-{satellite}/ABI-L2-RRQPEF/{t.year}/{doy:03d}/{t.hour:02d}/*.nc"))
    if not files:
        raise FileNotFoundError("No GOES RRQPE files for that hour")
    # file names contain the scan start time as _sYYYYDDDHHMMSSS (year, day of year, time)
    starts = [pd.to_datetime(f.split("_s")[1][:13], format="%Y%j%H%M%S", utc=True) for f in files]
    i = int(np.argmin([abs((s - t).total_seconds()) for s in starts]))   # closest scan

    with fs.open(files[i]) as f:
        ds = xr.open_dataset(f, engine="h5netcdf")
        geo = ds["goes_imager_projection"].attrs
        h = geo["perspective_point_height"]
        proj = Proj(proj="geos", h=h, lon_0=geo["longitude_of_projection_origin"], sweep=geo["sweep_angle_axis"])
        x = ds.x.values * h
        y = ds.y.values * h
        X, Y = np.meshgrid(x, y)
        lon, lat = proj(X, Y, inverse=True)
        rate = ds["RRQPE"].values

    west, east, south, north = bbox
    inside = np.isfinite(lon) & (lon >= west) & (lon <= east) & (lat >= south) & (lat <= north)
    pts = np.column_stack([lon[inside], lat[inside]])
    vals = np.where(rate[inside] >= 0, rate[inside], np.nan)

    glon = np.arange(west, east, step_deg)
    glat = np.arange(north, south, -step_deg)
    G_lon, G_lat = np.meshgrid(glon, glat)
    grid = griddata(pts, vals, (G_lon, G_lat), method="nearest")
    da = xr.DataArray(grid.astype("float32"), dims=("lat", "lon"), coords={"lat": glat, "lon": glon},
                      name="rrqpe")
    da.attrs.update(units="mm/h", scan_start=starts[i].isoformat(), file=files[i])
    da.to_netcdf(cache_file)
    return da


# ----------------------------------------------------------------------------
# 7. Point and basin extraction
# ----------------------------------------------------------------------------

def point_series(da, lon, lat):
    """Time series of the grid cell nearest to (lon, lat). Works on (time, lat, lon) arrays."""
    s = da.sel(lon=lon, lat=lat, method="nearest").to_series()
    return s


def nldi_basin(usgs_site):
    """Drainage basin polygon of a USGS gauge from the NLDI service. Returns a shapely geometry."""
    from shapely.geometry import shape
    r = requests.get(f"{NLDI}/USGS-{usgs_site}/basin", timeout=120)
    r.raise_for_status()
    return shape(r.json()["features"][0]["geometry"])


def basin_mask(da, geometry):
    """Boolean mask of grid cells whose centre falls inside the polygon."""
    from shapely import contains_xy
    LON, LAT = np.meshgrid(da.lon.values, da.lat.values)
    inside = contains_xy(geometry, LON, LAT)
    return xr.DataArray(inside, dims=("lat", "lon"), coords={"lat": da.lat, "lon": da.lon})


def basin_mean_series(da, geometry):
    """Basin average of a (time, lat, lon) field. Cells outside the basin are ignored."""
    mask = basin_mask(da.isel(time=0), geometry)
    return da.where(mask).mean(dim=("lat", "lon")).to_series()


# ----------------------------------------------------------------------------
# 8. Plotting helpers
# ----------------------------------------------------------------------------

def add_map_features(ax, bbox, counties=False):
    """State borders, lakes and a light grid on a cartopy axis."""
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    ax.set_extent(bbox, crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.STATES.with_scale("10m"), linewidth=0.8, edgecolor="black")
    ax.add_feature(cfeature.LAKES.with_scale("10m"), facecolor="none", edgecolor="black", linewidth=0.4)
    gl = ax.gridlines(draw_labels=True, linewidth=0.3, color="gray", linestyle=":")
    gl.top_labels = gl.right_labels = False
    gl.xlabel_style = gl.ylabel_style = {"size": 10, "color": "black"}
    return ax


def rain_map(da, bbox, title="", ax=None, vmax=None, cbar_label="mm", lon=None, lat=None):
    """Draw one rainfall field with the shared colour scale. Returns the mesh for a colour bar."""
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    if ax is None:
        fig = plt.figure(figsize=(9, 7))
        ax = plt.axes(projection=ccrs.PlateCarree())
    cmap, norm = rain_cmap()
    x = da.lon if lon is None else lon
    y = da.lat if lat is None else lat
    mesh = ax.pcolormesh(x, y, da.values, cmap=cmap, norm=norm, transform=ccrs.PlateCarree(), shading="auto")
    add_map_features(ax, bbox)
    ax.set_title(title, fontsize=13, color="black", loc="left")
    return mesh


def score(obs, est):
    """Three simple scores between gauge values (obs) and product values (est)."""
    obs, est = np.asarray(obs, float), np.asarray(est, float)
    ok = np.isfinite(obs) & np.isfinite(est)
    obs, est = obs[ok], est[ok]
    bias = est.sum() / obs.sum() if obs.sum() > 0 else np.nan     # multiplicative bias
    rmse = float(np.sqrt(np.mean((est - obs) ** 2)))
    corr = float(np.corrcoef(obs, est)[0, 1]) if len(obs) > 2 else np.nan
    return {"n": int(len(obs)), "bias_ratio": round(float(bias), 2), "rmse_mm": round(rmse, 1),
            "correlation": round(corr, 2)}
