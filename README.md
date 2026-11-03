# Predicting Flash Floods in Working Landscapes

Workshop materials for the CUAHSI Water Science Exchange 2026, University of Missouri, Saturday November 14, 2026, full day with a lunch break.

Instructors. Santiago Henao Gomez, Mohamed Abdelkader and Humberto Vergara, University of Iowa, IIHR Hydroscience and Engineering and the Iowa Flood Center.

## One repository, one branch per module

The workshop has three two hour modules. Each module lives on its own branch so that participants can clone exactly what they need for the session in front of them.

| Module | Branch | Content |
|---|---|---|
| 1. Quantitative Precipitation Estimation | `module-1-qpe` | Sources of precipitation data, access with Python, radar only against gauge corrected estimates for the June 2024 northwest Iowa flood |
| 2. Distributed flash flood simulation | `module-2-ef5` | Running the EF5 model in a prepared container, forcing it with the Module 1 rainfall, reading its outputs |
| 3. Event based evaluation and forecast skill | `module-3-evaluation` | Comparing simulated and observed hydrographs, event metrics, what rainfall latency does to lead time |

Clone one module

```
git clone -b module-1-qpe https://github.com/AHWALab/Water-Science-Exchange-Workshop.git wse-module-1
```

Clone everything and switch between modules

```
git clone https://github.com/AHWALab/Water-Science-Exchange-Workshop.git
cd Water-Science-Exchange-Workshop
git checkout module-1-qpe
```

Each branch carries its own README with the schedule, the learning objectives and the setup steps for that module.

## The case study

Flash flood of June 21 to 22, 2024, in northwest Iowa, southeast South Dakota and southwest Minnesota. Training thunderstorms dropped 150 to 250 mm in a few hours. The Rock River near Rock Valley (USGS 06483500) set a record of 157,000 cubic feet per second in 127 years of observations and the Floyd River at Alton (USGS 06600100) reached its highest flow since 1953. The three modules follow this event from rainfall to simulation to evaluation.

## Before you arrive

- Python and Jupyter basics, an introductory hydrology background
- Accounts. GitHub, HydroShare, NASA Earthdata Login
- Docker Desktop installed and tested before the workshop, with administrator rights on your laptop and about 10 GB of free disk (Module 2 ships the model as a prepared container image)
- A laptop with a current browser

Setup instructions for each module are in the branch README. Participants on the list receive them by email before the meeting.

## Credits

Data access patterns follow the Project Pythia MRMS Cookbook (CC BY 4.0). MRMS is produced by NOAA National Severe Storms Laboratory and NCEP. Gauge data are served by the Iowa Environmental Mesonet and NOAA NCEI. EF5 is developed by the University of Oklahoma and NOAA National Severe Storms Laboratory.

Notebooks and code are released under the MIT license. Text and figures under CC BY 4.0.
