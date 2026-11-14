# Module 1. Quantitative Precipitation Estimation

Hands-on materials for the first two-hour module of **Predicting Flash Floods in Working Landscapes**, a one day workshop at the CUAHSI Water Science Exchange 2026, *Water in Working Landscapes*, University of Missouri, Columbia, Missouri. This branch, `module-1-qpe`, holds Module 1. The other modules are on `module-2-ef5` (distributed simulation with EF5) and `module-3-evaluation` (event based evaluation and forecast skill).

A flash flood model is only as good as the rain it is given. In this module participants find out where precipitation estimates come from, pull them from public archives with Python, and measure how the estimate of one real storm changed while forecasters waited for gauges to report. The case is the flood of June 21 to 22, 2024, in northwest Iowa, the same event that Modules 2 and 3 simulate and evaluate. Everything runs in Google Colab with no installation, or on any computer with Python.

## Workshop at a glance

| | |
|---|---|
| Event | [CUAHSI Water Science Exchange 2026, Water in Working Landscapes](https://www.cuahsi.org/events/cuahsi-water-science-exchange-water-in-working-landscapes), University of Missouri, November 12 to 14, 2026 |
| Session | Saturday, November 14, 2026, Module 1 of 3 (two hours) |
| Format | 20 minute talk, then two notebooks in Google Colab or on your own computer |
| Leads | Mohamed Abdelkader, Humberto Vergara and Santiago Henao Gomez, IIHR Hydroscience and Engineering and Iowa Flood Center, University of Iowa |
| Capacity | 30 participants |
| Audience | Graduate students, postdoctoral researchers and early career professionals with hydrologic training |

## Quick start

1. Open notebook 1 with the badge below and run the cells from top to bottom. Continue with notebook 2.
2. The first cell of every notebook copies this branch to the Colab machine and installs the two libraries Colab lacks (about one minute). No account is needed, the repository is public.
3. Each notebook ends with a guided activity in blocks marked `Your Code Goes Here`. The activity of each notebook is solved in a short separate notebook, `N1_solution` and `N2_solution`, and the `_solution` notebooks hold the full notebooks executed with every output.

## The notebooks

| | Notebook | What happens | Time | Open |
|---|---|---|---|---|
| 1 | Where to find precipitation observations | MRMS from the NOAA bucket on AWS, step by step, and from the Iowa State mirror. Latency measured from the archive itself. NCEP Stage IV. Four gauge networks (airports, Iowa mesonet, NOAA USCRN, CoCoRaHS). GOES satellite rain rate against radar | 30 min | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AHWALab/Water-Science-Exchange-Workshop/blob/module-1-qpe/notebooks/01_where_to_find_qpe_data.ipynb) |
| 2 | One storm, three estimates | 24 hours of the June 2024 flood as radar only, Pass 1 and Pass 2. Where the gauges acted. Storm totals against hourly gauges and against independent volunteer gauges. Basin rainfall for the Floyd River. The forecaster at 6 am | 60 min | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AHWALab/Water-Science-Exchange-Workshop/blob/module-1-qpe/notebooks/02_june2024_event_three_estimates.ipynb) |

Activity solutions, short notebooks that rebuild only what the activity needs and run on their own

| | Activity solved | Open |
|---|---|---|
| N1 | Another hour and another gauge against the three MRMS products | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AHWALab/Water-Science-Exchange-Workshop/blob/module-1-qpe/notebooks/N1_solution.ipynb) |
| N2 | The forecaster at 06:30 UTC, what each product showed against the final amount | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AHWALab/Water-Science-Exchange-Workshop/blob/module-1-qpe/notebooks/N2_solution.ipynb) |

Full notebooks executed with every output: [notebook 1](notebooks/01_where_to_find_qpe_data_solution.ipynb), [notebook 2](notebooks/02_june2024_event_three_estimates_solution.ipynb).

## Learning objectives

By the end of the module participants will be able to

1. describe the main sources of precipitation estimates (rain gauge networks, weather radar, satellites, model analyses) and the multi-sensor products built from them;
2. access near real time precipitation products and gauge observations from public archives with Python, clip them to a region of interest, and compare them on a map;
3. explain the trade-off between latency and accuracy in operational QPE, and measure it directly in the archives;
4. evaluate radar-only and gauge-corrected rainfall estimates against independent gauges for a flash flood event.

## Session plan

| Time | Part | Material |
|---|---|---|
| 0:00 | What is QPE. Instruments, networks, products, latency | `slides/` |
| 0:20 | Where to find precipitation observations | Notebook 1 |
| 0:50 | One storm, three estimates | Notebook 2 |
| 1:50 | Discussion, bridge to Module 2 | |

## The case study

Flash flood of June 21 to 22, 2024, in northwest Iowa, southeast South Dakota and southwest Minnesota. Training thunderstorms dropped 150 to 250 mm in a few hours. The Rock River near Rock Valley (USGS 06483500) set a record of 157,000 cubic feet per second in 127 years of observations, and the Floyd River at Alton (USGS 06600100) reached its highest flow since 1953.

What the default run produces (24 hours ending June 22, 2024, 12 UTC, box 97.5 to 94.5 W and 42 to 44.5 N)

| | |
|---|---|
| Latency measured from the AWS upload times | radar only median 11 min, Pass 1 median 18 min, Pass 2 median 68 min |
| Largest 24 h total in the box | 236 mm (radar only), 212 mm (Pass 1), 218 mm (Pass 2) |
| Against 144 CoCoRaHS gauges, not used by MRMS | bias ratio 1.02, 1.00, 1.04 and RMSE 16.1, 13.6, 11.8 mm for radar only, Pass 1, Pass 2 |
| Floyd River basin at Alton, 24 h basin mean | 110, 116 and 107 mm for the three products |

## Data sources

Everything downloads live from public archives without an account. The helper functions keep a clipped copy of every field in `data/cache`, and the repository ships with the cache filled for the workshop windows (about 11 MB), so both notebooks also run on a slow network.

| Source | Used for | Provider and access |
|---|---|---|
| MRMS radar only, multi-sensor Pass 1 and Pass 2, gauge influence index, 2 minute rate, 24 h totals | All gridded rainfall in both notebooks | NOAA NSSL and NCEP, AWS bucket `noaa-mrms-pds`, and the Iowa State University mtarchive mirror |
| NCEP Stage IV hourly analysis | A second multi-sensor product on the 4 km HRAP grid | NOAA NCEP, through the Iowa Environmental Mesonet archive |
| ASOS and AWOS airport stations, ISU Soil Moisture Network, CoCoRaHS | Hourly and daily gauge records, station lists | Iowa Environmental Mesonet, Iowa State University, web services |
| US Climate Reference Network | Hourly weighing gauge record at Sioux Falls 14 NNE | NOAA NCEI, text files |
| GOES-16 Rainfall Rate (SCaMPR) | Satellite rain rate for one scan | NOAA, AWS bucket `noaa-goes16` |
| USGS Network Linked Data Index | Basin boundary of the Floyd River at Alton | USGS water data web services |

The catalog `docs/qpe_data_catalog.md` lists resolution, latency and access for these and other products, with sources. `docs/references.md` is the reading list.

## Repository layout

```
README.md                  this page
requirements.txt           Python dependencies for a local run
environment.yml            the same as a conda environment
notebooks/
  01_where_to_find_qpe_data.ipynb                 participant version
  01_where_to_find_qpe_data_solution.ipynb        executed, with the completed activity
  02_june2024_event_three_estimates.ipynb         participant version
  02_june2024_event_three_estimates_solution.ipynb
  N1_solution.ipynb        the activity of notebook 1, solved, runs on its own
  N2_solution.ipynb        the activity of notebook 2, solved, runs on its own
  qpe_tools.py             helper functions, documented and meant to be read
data/cache/                pre-clipped fields and gauge tables for the workshop windows
docs/
  qpe_data_catalog.md      where to find precipitation data, with latencies and sources
  references.md            reading list
slides/
  QPE_theory_slide_content.md   content of the opening talk, slide by slide
tools/
  make_workshop_version.py builds the participant and solution notebooks from a marked source
```

### Running outside Colab

```
git clone -b module-1-qpe https://github.com/AHWALab/Water-Science-Exchange-Workshop.git
cd Water-Science-Exchange-Workshop
pip install -r requirements.txt
jupyter lab notebooks
```

Python 3.10 or newer. The GRIB2 reader (ecCodes) ships as a binary wheel, so a plain pip install works on Windows, macOS and Linux. The setup cell detects that the helper file is already there and only checks the packages.

## Notes for instructors

- The notebooks clone this branch from GitHub, so changes must be pushed before participants open the badges, and the repository must be public for the badges to work without a GitHub login.
- A Colab session opened before a push keeps the old code. Choose Runtime, Disconnect and delete runtime, then open the badge again.
- Live downloads of the 72 hourly files of notebook 2 took about one minute in the instructors' tests. With the shipped cache nothing is downloaded. Delete `data/cache` to force fresh downloads.
- MRMS latencies in older papers are 60 and 120 minutes for Pass 1 and Pass 2. The current version (12.2) lists 20 minutes and 1 hour, and section 4 of notebook 1 confirms it from the archive.
- Several AWOS airports in the box report zero through the storm. Notebook 2 flags them with a simple consistency rule, the same idea MRMS applies before using a gauge.
- The ISU Soil Moisture Network gauge at Doon reads about half of the product values in the heaviest hours. Notebook 2 presents it as an open question (hail, undercatch, or a true local maximum); the nearby volunteer gauges agree with the products within 10 to 20 percent.

## Credits and license

Data access patterns follow the [Project Pythia MRMS Cookbook](https://projectpythia.org/mrms-cookbook/) (Janoski, Sears, Condo, Heaton, Collins and Grover), content CC BY 4.0. MRMS is produced by NOAA National Severe Storms Laboratory and NCEP (Zhang and coauthors, 2016, Bulletin of the American Meteorological Society, 97, 621 to 638). Gauge data are served by the Iowa Environmental Mesonet, Iowa State University, and by NOAA NCEI.

Code in this branch is released under the MIT license, text and figures under CC BY 4.0.

## Contact

Mohamed Abdelkader, mohamed-abdelkader@uiowa.edu, IIHR Hydroscience and Engineering, University of Iowa.
