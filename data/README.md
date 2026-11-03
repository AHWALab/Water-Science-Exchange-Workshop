# Data cache

The helper functions in `notebooks/qpe_tools.py` store every clipped field and gauge table here, so a second run of a notebook is instant and the notebooks also work without a network connection.

```
cache/mrms/     one NetCDF file per MRMS product, hour and bounding box (about 1 km grid, mm)
cache/stage4/   NCEP Stage IV hourly fields on the HRAP grid, clipped
cache/goes/     GOES Rainfall Rate scans put on a 0.02 degree grid
cache/gauges/   CSV tables of hourly and daily gauge records for the event window
```

The cache shipped with the repository covers the windows used in the two notebooks (June 21 to 22, 2024). New hours or boxes are downloaded on first use and added here. Delete the folder to force fresh downloads.

Sources. NOAA MRMS on AWS (`noaa-mrms-pds`), Iowa State University mtarchive, Iowa Environmental Mesonet archive and web services, NOAA NCEI USCRN, NOAA GOES-16 on AWS (`noaa-goes16`).
