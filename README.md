# Module 3. Event based evaluation and forecast skill

Hands-on materials for the third two-hour module of **Predicting Flash Floods in Working Landscapes**, a one day workshop at the CUAHSI Water Science Exchange 2026, *Water in Working Landscapes*, University of Missouri, Columbia, Missouri. This branch, `module-3-evaluation`, holds Module 3. The other modules are on `module-1-qpe` (rainfall estimation) and `module-2-ef5` (distributed simulation).

A flood forecast is only useful if we can say how good it is. In this module participants build a small ensemble of streamflow simulations, turn it into a probability of flooding, and then verify that probability the way forecast centres do, with the contingency table, the ROC curve, the Brier score, the reliability diagram, the rank histogram and the CRPS. The last step turns the diagnosis into a better forecast. Everything runs in Google Colab with no installation, or on any computer with numpy and matplotlib.

## Workshop at a glance

| | |
|---|---|
| Event | [CUAHSI Water Science Exchange 2026, Water in Working Landscapes](https://www.cuahsi.org/events/cuahsi-water-science-exchange-water-in-working-landscapes), University of Missouri, November 12 to 14, 2026 |
| Session | Saturday, November 14, 2026, Module 3 of 3 (two hours) |
| Format | Hands on, four notebooks in Google Colab or on your own computer |
| Leads | Humberto Vergara and Mohamed Abdelkader, IIHR Hydroscience and Engineering, University of Iowa, with Santiago Henao Gomez |
| Capacity | 30 participants |
| Audience | Graduate students, postdoctoral researchers and early career professionals with hydrologic training |

## Quick start

1. Open notebook 1 with the badge below and run the cells from top to bottom. Continue with notebooks 2, 3 and 4.
2. The first cell of every notebook copies this branch to the Colab machine. No account is needed, the repository is public.
3. Each notebook ends with a short block marked `Your Code Goes Here`. The activity of each notebook is solved in a short separate notebook, `N1_solution` to `N4_solution`, and the `_solution` notebooks hold the full notebooks executed with every output.

## The notebooks

Run them in order. Each one rebuilds what it needs from the previous ones in a few seconds, so a notebook can also be opened on its own.

| | Notebook | What happens | Time | Open |
|---|---|---|---|---|
| 1 | The model and the control run | Load 40 years of Leaf River data, read the HyMOD model one function at a time, calibrate a control run, see how parameters and rainfall move the peak | 25 min | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AHWALab/Water-Science-Exchange-Workshop/blob/module-3-evaluation/notebooks/01_model_and_control_run.ipynb) |
| 2 | From an ensemble to a probability | Build 100 members by perturbing rainfall and parameters, spaghetti and band plots, probability of exceeding the flood threshold, what drives the spread | 25 min | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AHWALab/Water-Science-Exchange-Workshop/blob/module-3-evaluation/notebooks/02_ensemble_to_probability.ipynb) |
| 3 | Did we call the event | Contingency table, POD, FAR, POFD and CSI, decision thresholds, the ROC curve and its area, the performance diagram | 30 min | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AHWALab/Water-Science-Exchange-Workshop/blob/module-3-evaluation/notebooks/03_did_we_call_the_event.ipynb) |
| 4 | Are the probabilities trustworthy | Brier score and skill score, reliability diagram, rank histogram, CRPS, and a recalibrated ensemble that fixes what the scores found | 30 min | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AHWALab/Water-Science-Exchange-Workshop/blob/module-3-evaluation/notebooks/04_are_the_probabilities_trustworthy.ipynb) |

Activity solutions, short notebooks that rebuild only what the activity needs and run on their own in seconds

| | Activity solved | Open |
|---|---|---|
| N1 | Sweep the split parameter Alp and report how far the peak moves | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AHWALab/Water-Science-Exchange-Workshop/blob/module-3-evaluation/notebooks/N1_solution.ipynb) |
| N2 | Probability of exceedance from 20 members against 100 members | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AHWALab/Water-Science-Exchange-Workshop/blob/module-3-evaluation/notebooks/N2_solution.ipynb) |
| N3 | The decision threshold with the best CSI and its full set of scores | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AHWALab/Water-Science-Exchange-Workshop/blob/module-3-evaluation/notebooks/N3_solution.ipynb) |
| N4 | The control run scored as a 0 or 1 probability forecast against both ensembles | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AHWALab/Water-Science-Exchange-Workshop/blob/module-3-evaluation/notebooks/N4_solution.ipynb) |

Full notebooks executed with every output: [notebook 1](notebooks/01_model_and_control_run_solution.ipynb), [notebook 2](notebooks/02_ensemble_to_probability_solution.ipynb), [notebook 3](notebooks/03_did_we_call_the_event_solution.ipynb), [notebook 4](notebooks/04_are_the_probabilities_trustworthy_solution.ipynb).

## Learning objectives

By the end of the module participants will be able to

1. explain why a single model run hides forecast uncertainty, and how an ensemble represents it;
2. turn an ensemble of simulations into a probability of exceeding a flood threshold;
3. verify event forecasts with the contingency table, categorical scores and the ROC curve;
4. verify probabilistic forecasts with the Brier score, the reliability diagram, the rank histogram and the CRPS, and use the diagnosis to improve the ensemble.

## Session plan

| Time | Part | Material |
|---|---|---|
| 0:00 | Why verify, and the experiment of the afternoon | Slides |
| 0:10 | The model and the control run | Notebook 1 |
| 0:35 | From an ensemble to a probability | Notebook 2 |
| 1:00 | Did we call the event | Notebook 3 |
| 1:30 | Are the probabilities trustworthy | Notebook 4 |
| 1:55 | Back to the June 2024 flood of Module 2, discussion | |

## The experiment

- Catchment. Leaf River, Mississippi, about 1,944 square kilometres, 40 years of daily precipitation, potential evapotranspiration and streamflow in `notebooks/LeafCatch.dat`, all in millimetres per day. A classic test case for conceptual models.
- Model. HyMOD, a probability distributed soil store feeding a quick and a slow routing path, six parameters, in `notebooks/hymod_tools.py`. Ported from the MATLAB tutorial of H. V. Gupta (HWR 521, University of Arizona, 2005).
- Forecast. A 100 member ensemble over the first five years, from a random rainfall multiplier and random parameters. The ensemble is deliberately imperfect so that the verification tools have something to find.
- Event. A day counts as a flood when flow reaches one quarter of the mean annual maximum, 5.0 mm per day, which happens on 115 of the 1,825 days.

What the default run produces

| | |
|---|---|
| Control run | NSE 0.78, RMSE 1.51 mm per day, KGE 0.76 over the five year window |
| Raw ensemble | ROC area 0.68, Brier skill score 0.0, CRPS 0.97 mm per day, observation above every member on 119 days |
| Recalibrated ensemble | Brier skill score 0.52, CRPS 0.50 mm per day, below the absolute error of the control run (0.75) |

## Repository layout

```
README.md                  this page
requirements.txt           numpy and matplotlib, nothing else
notebooks/
  01_model_and_control_run.ipynb               participant version
  01_model_and_control_run_solution.ipynb      executed, with the completed activity
  02_ensemble_to_probability.ipynb             and its _solution
  03_did_we_call_the_event.ipynb               and its _solution
  04_are_the_probabilities_trustworthy.ipynb   and its _solution
  N1_solution.ipynb to N4_solution.ipynb       the four activities, solved, each runs on its own
  hymod_tools.py           the model, the scores and the ensemble generator, meant to be read
  nb_style.py              one plotting style for the four notebooks
  LeafCatch.dat            the Leaf River data
tools/
  make_workshop_version.py builds the participant and solution notebooks from a marked source
```

### Running outside Colab

```
git clone -b module-3-evaluation https://github.com/AHWALab/Water-Science-Exchange-Workshop.git
cd Water-Science-Exchange-Workshop
pip install -r requirements.txt
jupyter lab notebooks
```

Python 3.9 or newer. The setup cell detects that the helper files are already there and does nothing else.

## Notes for instructors

- The notebooks clone this branch from GitHub, so changes must be pushed before participants open the badges, and the repository must be public for the badges to work without a GitHub login.
- A Colab session opened before a push keeps the old code. Choose Runtime, Disconnect and delete runtime, then open the badge again.
- Every notebook rebuilds the ensemble from the same seed in about four seconds, so a participant who joins late can start at notebook 3.
- The raw ensemble never issues a probability above 15 percent. That is intended, it is a dry ensemble, and notebook 4 section 6 shows the repair. Decision thresholds in notebook 3 are therefore low.
- If time is short, notebook 4 can stop after the rank histogram (section 4); the recalibration of section 6 is the natural closing figure if it fits.

## Credits and license

The notebooks are adapted from the Ensemble Forecast Evaluation series prepared by Humberto Vergara and Mohamed Abdelkader for the CIROH Summer Institute 2026. The HyMOD code follows the MATLAB tutorial of H. V. Gupta, and the Leaf River data are the classic test set distributed with it.

Key references. Wilks, D. S., 2019, Statistical Methods in the Atmospheric Sciences, 4th edition, chapter 9. Hersbach, H., 2000, Weather and Forecasting, 15, 559 to 570 (CRPS). Hamill, T. M., 2001, Monthly Weather Review, 129, 550 to 560 (rank histograms). Roebber, P. J., 2009, Weather and Forecasting, 24, 601 to 608 (performance diagram). Murphy, A. H., 1973, Journal of Applied Meteorology, 12, 595 to 600 (Brier score decomposition).

Code in this branch is released under the MIT license, text and figures under CC BY 4.0.

## Contact

Humberto Vergara, humberto-vergaraarrieta@uiowa.edu, and Mohamed Abdelkader, mohamed-abdelkader@uiowa.edu, IIHR Hydroscience and Engineering, University of Iowa.
