# Where to find precipitation data

A reference list for participants of Module 1. Every entry gives what the product is, its grid or network, its latency, where to read it, and the source of the numbers. Latency is the time between the end of the observation period and the moment the data can be downloaded. Access notes are current as of November 2026.

## 1. Multi-sensor gridded products (United States)

| Product | What it is | Grid and time step | Latency | Access | Source |
|---|---|---|---|---|---|
| MRMS Radar only QPE | Rainfall from the national radar mosaic, about 180 radars, no gauges | 0.01 degree (about 1 km), 2 min rate, 1 h to 72 h totals | Minutes (measured median 11 min on June 22, 2024) | AWS `noaa-mrms-pds`, Iowa State mtarchive | NSSL product tables, v12.2 |
| MRMS Multi-sensor QPE Pass 1 | Radar QPE corrected with the gauges received early, plus model and climatology where radar is poor | 1 km, hourly, 1 h to 72 h totals | About 20 min (measured median 18 min) | AWS | NSSL product tables, v12.2 |
| MRMS Multi-sensor QPE Pass 2 | Same with more gauges | 1 km, hourly | About 1 h (measured median 68 min) | AWS, Iowa State mtarchive | NSSL product tables, v12.2 |
| MRMS Gauge Influence Index | 0 where the estimate is radar, 1 where it is gauge, for Pass 1 and Pass 2 | 1 km, hourly | Same as the pass | AWS | NSSL product tables, v12.2 |
| MRMS Radar Quality Index | Confidence in the radar estimate, from beam blockage, height and melting layer | 1 km, 2 min | Minutes | AWS | Zhang et al. 2016 |
| NCEP Stage IV | Mosaic of the twelve River Forecast Center analyses, radar plus gauges, manual quality control | HRAP polar stereographic, about 4 km, 1 h, 6 h, 24 h | About 1 h for the first version, revised hourly for 23 h and again at 1, 3, 5 and 7 days | NOMADS (14 days), Iowa Environmental Mesonet archive, NCAR EOL dataset 21.093 | NCEP EMC pcpanl page |
| NOAA AORC | Analysis of Record for Calibration, the forcing of the National Water Model retrospective | About 1 km (30 arc seconds), hourly, 1979 to near present | Produced with a 10 day lag, not a real time product | AWS `noaa-nws-aorc-v1-1-1km`, Zarr | AWS Open Data registry |
| PRISM | Climatologically aided interpolation of gauges with terrain | 4 km (800 m for some products), daily and monthly | Provisional next day, stable after six months | PRISM Climate Group, Oregon State University | PRISM documentation |

Older names you may still meet in papers and file systems: Q3RAD and Q3GC (MRMS radar-only and gauge-corrected QPE before 2020), GaugeCorr_QPE (the single gauge-corrected product before Pass 1 and Pass 2 were introduced with MRMS v12 in October 2020), Stage II (discontinued July 2020).

## 2. Radar networks

| Network | What it is | Coverage | Notes | Source |
|---|---|---|---|---|
| NEXRAD, WSR-88D | S band, dual polarization, operated by NWS, FAA and DoD | 158 operational radars, maximum range 430 km | The backbone of MRMS. Beam height rises with range, about 1.5 km at 100 km, over 5 km at 230 km | NWS Radar Operations Center |
| TDWR | C band terminal Doppler radars at large airports | 45 radars | Used by MRMS for coverage near cities | NSSL MRMS pages |
| Canadian radars | S and C band, Environment and Climate Change Canada | 30 radars | Included in the MRMS mosaic for the northern border | Zhang et al. 2016 |
| Gap filling X band radars | Short range research radars, for example the Iowa Flood Center XPOL units | Local | Fine resolution near the ground, strong attenuation in heavy rain | Iowa Flood Center |

## 3. Rain gauge networks

| Network | Instrument | Size | Time step and latency | Access | Source |
|---|---|---|---|---|---|
| ASOS | Airport stations run by NWS, FAA and DoD. Heated tipping bucket or all weather weighing gauge | About 950 sites | 1 min and hourly, available within minutes through METAR | Iowa Environmental Mesonet `asos.py`, NCEI Local Climatological Data | NWS ASOS page |
| AWOS | FAA and state airport stations | Hundreds | Many report no precipitation at all. Check before use | Iowa Environmental Mesonet | This module, Notebook 2 |
| HADS | NWS collection of hydrometeorological gauges transmitted through GOES, mostly tipping buckets | Thousands of platforms | Hourly, within the hour | NWS HADS, MADIS | Zhang et al. 2016 |
| USCRN | NOAA Climate Reference Network. Geonor weighing gauge read by three independent sensors inside a wind shield | 114 stations in the contiguous US, 25 in Alaska, 2 in Hawaii | 5 min and hourly, posted within about an hour | NCEI text files `pub/data/uscrn/products` | NCEI USCRN overview and measurements pages |
| COOP | NWS Cooperative Observer Program, manual 8 inch gauges | More than 8,000 volunteers | Daily, same or next day | NCEI GHCN Daily, Iowa Environmental Mesonet | NWS COOP program |
| CoCoRaHS | Volunteer 4 inch manual gauges, read near 7 am local time | More than 26,000 observers in the US, Canada and the Bahamas | Daily, same morning | CoCoRaHS, Iowa Environmental Mesonet `daily.json` | Colorado State University, 2023 |
| State mesonets | Research grade automated stations, for example the ISU Soil Moisture Network in Iowa, the Oklahoma Mesonet, the Kentucky Mesonet | Tens to hundreds per state | 1 min to hourly, within the hour | Each network, many through the Iowa Environmental Mesonet and MADIS | Network websites |
| Iowa Flood Center rain gauges and stream sensors | Tipping buckets paired with bridge mounted stage sensors | More than 250 stream sensors in Iowa | Real time | Iowa Flood Information System | Iowa Flood Center |
| SNOTEL | Snow pillows and storage gauges in the mountain West | About 900 sites | Hourly and daily | USDA NRCS | NRCS |

Gauges feed the correction of the gridded products. HADS and MADIS gauges enter MRMS Pass 1 and Pass 2. CoCoRaHS reports do not enter the hourly products and are used by NSSL as independent verification.

## 4. Satellite products

| Product | What it is | Grid and time step | Latency | Access | Source |
|---|---|---|---|---|---|
| GOES RRQPE (SCaMPR) | Rain rate from GOES ABI infrared and water vapour bands, calibrated against passive microwave rain rates | 2 km at nadir, every 10 min | Minutes | AWS `noaa-goes16`, `noaa-goes18`, `noaa-goes19`, product `ABI-L2-RRQPEF` | NOAA TOWR-S GOES RRQPE page |
| IMERG Early | GPM constellation, passive microwave plus infrared morphing | 0.1 degree, 30 min, global 60 S to 60 N and beyond | 4 h | NASA GES DISC, Earthdata login | NASA GPM data directory |
| IMERG Late | Same with backward morphing | 0.1 degree, 30 min | 12 to 14 h | NASA GES DISC | NASA GPM data directory |
| IMERG Final | Same with monthly gauge adjustment | 0.1 degree, 30 min, daily, monthly | About 3.5 months | NASA GES DISC | NASA GPM data directory |
| PERSIANN CCS | Infrared cloud classification, University of California Irvine | 0.04 degree, hourly | About 1 h | CHRS Data Portal | CHRS |
| GSMaP | JAXA passive microwave and infrared blend | 0.1 degree, hourly | 4 h near real time | JAXA | JAXA |

## 5. Model based analyses

These are not observations. They are useful where observations are missing and as the gap filler inside multi-sensor products.

| Product | What it is | Grid and time step | Latency | Access |
|---|---|---|---|---|
| HRRR analysis and 1 h forecast | NOAA convection allowing model, 1 h precipitation from the first forecast hour. Used by MRMS where radar quality is low | 3 km, hourly | About 1 h | AWS `noaa-hrrr-bdp-pds` |
| National Water Model Analysis and Assimilation forcing | MRMS gauge corrected QPE blended with HRRR and RAP | 1 km, hourly | About 1 h | NOMADS, AWS `noaa-nwm-pds` |
| NLDAS 2 | North American Land Data Assimilation System, gauge analysis disaggregated with radar and model | 0.125 degree, hourly | Several days | NASA GES DISC |
| ERA5 | ECMWF global reanalysis | 0.25 degree, hourly | 5 days | Copernicus Climate Data Store |

## 6. Where we read each source in the notebooks

| Source | Helper in `qpe_tools.py` | Notebook |
|---|---|---|
| MRMS on AWS and Iowa State | `read_mrms`, `read_mrms_series`, `mrms_upload_latency` | 1 and 2 |
| Stage IV | `read_stage4` | 1 |
| ASOS, ISUSM, CoCoRaHS, station lists | `iem_asos_hourly`, `iem_isusm_hourly`, `iem_cocorahs_daily`, `iem_stations` | 1 and 2 |
| USCRN | `uscrn_hourly` | 1 and 2 |
| GOES RRQPE | `read_goes_rrqpe` | 1 |
| USGS basin boundaries | `nldi_basin`, `basin_mask`, `basin_mean_series` | 2 |

## Sources

- NOAA NSSL, MRMS operational product tables, version 12.2. https://nssl.noaa.gov/projects/mrms/operational/tables.php
- Zhang, J. and coauthors, 2016. Multi-Radar Multi-Sensor (MRMS) Quantitative Precipitation Estimation, Initial Operating Capabilities. Bulletin of the American Meteorological Society, 97, 621 to 638. https://doi.org/10.1175/BAMS-D-14-00174.1
- NOAA NWS Warning Decision Training Division, Multi-Sensor QPE. https://vlab.noaa.gov/web/wdtd/-/multi-sensor-qpe
- NOAA NCEP EMC, Stage IV precipitation analysis. https://www.emc.ncep.noaa.gov/mmb/SREF/pcpanl/
- AWS Open Data registry, NOAA Analysis of Record for Calibration. https://registry.opendata.aws/noaa-nws-aorc/
- NWS Radar Operations Center, about us. https://www.roc.noaa.gov/roc-about-us.php
- NWS ASOS program. https://www.weather.gov/asos/
- NOAA NCEI, USCRN program overview and measurements. https://www.ncei.noaa.gov/access/crn/overview.html and https://www.ncei.noaa.gov/access/crn/measurements.html
- Colorado State University, 2023. Every drop counts, CoCoRaHS celebrates 25 years. https://engr.source.colostate.edu/every-drop-counts-precipitation-measuring-network-celebrates-25-years-with-no-signs-of-slowing-down/
- Martinaitis, S. M., 2021. MRMS QPE and CoCoRaHS, WERA-1012 presentation. https://media.cocorahs.org/docs/Martinaitis-WERA21.pdf
- NOAA TOWR-S, GOES RRQPE. https://vlab.noaa.gov/web/towr-s/goes-rrqpe
- NASA GPM, data directory with IMERG latencies. https://gpm.nasa.gov/data/directory
- Iowa Environmental Mesonet. https://mesonet.agron.iastate.edu/
- Iowa State University mtarchive. https://mtarchive.geol.iastate.edu/
- Measured latencies in this document come from Notebook 1, section 4, upload times of the AWS objects for June 22, 2024.
