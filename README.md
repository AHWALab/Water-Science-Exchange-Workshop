# Module 1. Quantitative Precipitation Estimation

Branch `module-1-qpe` of the workshop repository for **Predicting Flash Floods in Working Landscapes**, CUAHSI Water Science Exchange 2026, University of Missouri, Saturday November 14, 2026.

Instructors. Mohamed Abdelkader, Humberto Vergara and Santiago Henao Gomez, University of Iowa, IIHR Hydroscience and Engineering and the Iowa Flood Center.

The other modules live on their own branches. `module-2-ef5` (distributed simulation with EF5) and `module-3-evaluation` (event based evaluation and forecast skill). The `main` branch holds the overview and the setup instructions.

## Learning objectives

By the end of this module you will be able to

1. Describe the main sources of precipitation estimates (rain gauge networks, weather radar, satellites, model analyses) and the multi-sensor products built from them.
2. Access near real time precipitation products and gauge observations from public archives with Python, clip them to a region of interest, and compare them on a map.
3. Explain the trade-off between latency and accuracy in operational QPE, and measure it directly in the archives.
4. Evaluate radar-only and gauge-corrected rainfall estimates against independent gauges for a flash flood event.

## Schedule, two hours

| Time | Part | Material |
|---|---|---|
| 0:00 to 0:20 | What is QPE. Instruments, networks, products, latency | `slides/` |
| 0:20 to 0:50 | Where to find precipitation observations, guided tour | `notebooks/01_where_to_find_qpe_data.ipynb` |
| 0:50 to 1:50 | One storm, three estimates. The June 2024 northwest Iowa flood | `notebooks/02_june2024_event_three_estimates.ipynb` |
| 1:50 to 2:00 | Discussion, bridge to Module 2 | |

## Folder layout

```
notebooks/
    01_where_to_find_qpe_data.ipynb                participant version, with placeholders
    01_where_to_find_qpe_data_solution.ipynb       instructor version, executed, with outputs
    02_june2024_event_three_estimates.ipynb        participant version
    02_june2024_event_three_estimates_solution.ipynb
    qpe_tools.py                                   helper functions used by both notebooks
data/cache/                                        pre-clipped fields and gauge tables, the notebooks run offline from here
docs/qpe_data_catalog.md                           where to find precipitation data, with latencies and sources
docs/references.md                                 reading list
slides/QPE_theory_slide_content.md                 content of the opening talk, slide by slide
tools/make_workshop_version.py                     builds the participant notebook from the solution notebook
environment.yml, requirements.txt                  Python environment
```

## Setup

Participants need Python 3.10 or newer with the packages in `requirements.txt`. The GRIB2 decoder (ecCodes) ships as a binary wheel, so a plain pip install works on Windows, macOS and Linux.

Option A, conda or mamba

```
git clone -b module-1-qpe https://github.com/AHWALab/Water-Science-Exchange-Workshop.git
cd Water-Science-Exchange-Workshop
conda env create -f environment.yml
conda activate wse-qpe
jupyter lab notebooks
```

Option B, pip in an existing environment

```
pip install -r requirements.txt
```

Option C, CUAHSI JupyterHub or any hosted Jupyter. Clone the branch in a terminal, open the notebooks, run the install cell at the top of each notebook once.

Check the installation with

```
python -c "import eccodes, cfgrib, xarray, cartopy, s3fs; print('ready')"
```

## Data

Everything downloads live from public archives without an account.

- MRMS from the NOAA bucket `noaa-mrms-pds` on AWS and from the Iowa State University mtarchive mirror
- NCEP Stage IV from the Iowa Environmental Mesonet archive
- Gauges from the Iowa Environmental Mesonet (ASOS, ISU Soil Moisture Network, CoCoRaHS) and from NOAA NCEI (US Climate Reference Network)
- GOES Rainfall Rate from the NOAA bucket `noaa-goes16`
- Basin boundaries from the USGS Network Linked Data Index

The helper functions keep a clipped copy of each field in `data/cache`. The repository ships with the cache filled for the workshop windows (about 11 MB), so both notebooks also run on a slow or absent network. Delete `data/cache` to force fresh downloads.

## The case study

Flash flood of June 21 to 22, 2024, in northwest Iowa, southeast South Dakota and southwest Minnesota. Rock River near Rock Valley (USGS 06483500) and Floyd River at Alton (USGS 06600100). The same event is simulated in Module 2 and evaluated in Module 3.

## Credits and licenses

- Data access patterns follow the Project Pythia MRMS Cookbook (Janoski, Sears, Condo, Heaton, Collins and Grover), content CC BY 4.0, code Apache 2.0. https://projectpythia.org/mrms-cookbook/
- MRMS is produced by NOAA National Severe Storms Laboratory and NCEP. Zhang, J. and coauthors, 2016, Bulletin of the American Meteorological Society, 97, 621 to 638.
- Gauge data are served by the Iowa Environmental Mesonet, Iowa State University, and by NOAA NCEI.
- Notebooks and code in this branch are released under the MIT license. Text and figures under CC BY 4.0.
