# Predicting Flash Floods in Working Landscapes

Workshop materials for the CUAHSI Water Science Exchange 2026, *Water in Working Landscapes*, University of Missouri, Columbia, Missouri. Full day workshop on Saturday, November 14, 2026, with a lunch break.

Instructors. Santiago Henao Gomez, Mohamed Abdelkader and Humberto Vergara, University of Iowa, IIHR Hydroscience and Engineering and the Iowa Flood Center.

## One repository, one branch per module

The workshop has three two hour modules. Each module lives on its own branch, with its own README, so that participants open exactly what they need for the session in front of them. Select the branch at the top left of this page, or follow the links below.

| Module | Branch | Content | How it runs |
|---|---|---|---|
| 1. Quantitative Precipitation Estimation | [`module-1-qpe`](https://github.com/AHWALab/Water-Science-Exchange-Workshop/tree/module-1-qpe) | Where precipitation estimates come from, access to MRMS, Stage IV, gauge networks and satellite products with Python, and the June 2024 northwest Iowa flood seen as radar only, Pass 1 and Pass 2 | Two notebooks in Google Colab, badges in the branch README |
| 2. Distributed flash flood simulation | [`module-2-ef5`](https://github.com/AHWALab/Water-Science-Exchange-Workshop/tree/module-2-ef5) | The EF5 model with CREST and kinematic wave routing in a prepared Docker image, the Little Sioux River at Smithland for the June 2024 event, parameter generation notebooks | Docker Desktop on your laptop, notebooks in Colab |
| 3. Event based evaluation and forecast skill | [`module-3-evaluation`](https://github.com/AHWALab/Water-Science-Exchange-Workshop/tree/module-3-evaluation) | From one model run to an ensemble and a probability of flooding, then verification with the contingency table, ROC, Brier score, reliability diagram, rank histogram and CRPS | Four notebooks in Google Colab, badges in the branch README |

Clone one module

```
git clone -b module-1-qpe https://github.com/AHWALab/Water-Science-Exchange-Workshop.git
```

Clone everything and switch between modules

```
git clone https://github.com/AHWALab/Water-Science-Exchange-Workshop.git
cd Water-Science-Exchange-Workshop
git checkout module-1-qpe
```

## The case study

Flash flood of June 21 to 22, 2024, in northwest Iowa, southeast South Dakota and southwest Minnesota. Training thunderstorms dropped 150 to 250 mm in a few hours. The Rock River near Rock Valley (USGS 06483500) set a record of 157,000 cubic feet per second in 127 years of observations, the Floyd River at Alton (USGS 06600100) reached its highest flow since 1953, and the Little Sioux River at Smithland (USGS 06605000) is the basin simulated in Module 2. Module 1 estimates the rain, Module 2 turns it into streamflow, Module 3 asks how good a forecast is and how to tell.

## Before you arrive

- Python and Jupyter basics, an introductory hydrology background
- A Google account for Google Colab (Modules 1 and 3 run there, nothing to install)
- Docker Desktop installed and tested before the workshop, with administrator rights on your laptop and about 10 GB of free disk (Module 2 ships the model as a prepared container image, see the `module-2-ef5` README)
- A laptop with a current browser and a charger

A GitHub account is not needed. The repository is public and the notebooks copy it without a login.

## Credits

Data access patterns in Module 1 follow the Project Pythia MRMS Cookbook (CC BY 4.0). MRMS is produced by NOAA National Severe Storms Laboratory and NCEP. Gauge data are served by the Iowa Environmental Mesonet and NOAA NCEI. EF5 is developed by the University of Oklahoma and NOAA National Severe Storms Laboratory. The Module 3 notebooks are adapted from the ensemble forecast evaluation series of the CIROH Summer Institute 2026.

Notebooks and code are released under the MIT license unless a branch states otherwise. Text and figures under CC BY 4.0.
