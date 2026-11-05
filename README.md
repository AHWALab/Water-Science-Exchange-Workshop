# EF5 Event Simulation Workshop — Little Sioux River (June 2024)

This repository contains everything you need to run a flood event simulation with **EF5** (Ensemble Framework For Flash Flood Forecasting) using the **CREST** water-balance model and **kinematic wave (KW)** routing, for USGS gauge **06605000** in the Little Sioux River basin (Iowa).

The workshop has the following steps:

0. **Install Docker Desktop** — before the workshop.
1. **Install the EF5 Docker image and download the data** — no compiling needed.
2. **Generate the model parameters** — Jupyter notebooks in `PARAMETER_GENERATION/`.
3. **Run the event simulation** — `EF5_EVENT_MODEL/`, which already includes all the computed parameters.

> Step 3 does **not** depend on Step 2. If you are short on time, you can go directly from Step 1 to Step 3.


---

## Requirements

| Software | Needed for | Source |
|---|---|---|
| **Docker Desktop** | Steps 1 and 3 | https://www.docker.com/products/docker-desktop/ |
| **Python 3.10+**  | Step 2 | Recommended: Google Colab. Other: Jupyter (e.g. Anaconda/Miniconda) |

---

## Step 0 (before workshop) — Install Docker Desktop

Before the workshop, install Docker Desktop and open it once so it finishes its setup. On Windows it may ask you to enable WSL 2 and restart.

1. **Download** Docker Desktop from the official website: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
2. **Install** Docker Desktop on your computer.
3. **Open** Docker Desktop and wait until it shows *Engine running*.

> **Tip:** avoid spaces and accented characters in the folder where you place this repository (e.g. use `C:\EF5_Workshop`). Paths with spaces need extra quoting in Docker commands.

---

## Step 1 — Install the EF5 Docker image and data download

### 1.1 Install the EF5 image in Docker

The EF5 image is distributed as a single file, `ef5-container.tar` (~110 MB).

1. **Download** `ef5-container.tar`: [download link](https://iowa-my.sharepoint.com/:u:/g/personal/henaogomez_uiowa_edu/IQDKkPISGJB6R47jmfKj5UC5AZ3F6ZW9ZJRnVcqgA7D9maM?e=JQkNZY).
2. **Open Docker Desktop** and wait until it shows *Engine running*.
3. **Load the image.** Open a terminal (PowerShell on Windows, Terminal on macOS/Linux) in the folder where you saved the file:

   ```powershell
   docker load -i ef5-container.tar
   ```

   You should see: `Loaded image: ef5-container:latest`

4. **Check** that it is installed:

   ```powershell
   docker images ef5-container
   ```

Once loaded, you can delete the `.tar` file.

> **Apple Silicon Macs (M1–M4) and ARM Windows laptops:** the image is built for Intel/AMD processors. It still works through emulation (a bit slower). You may see a warning like `The requested image's platform (linux/amd64) does not match the detected host platform`; it is harmless. Adding `--platform linux/amd64` to `docker run` (as in the commands below) silences it.

### 1.2 Get the domain data

#### Option A — Download ZIP

1. **Download** the workshop repository as a ZIP file from GitHub [GitHub repository](https://github.com/AHWALab/Water-Science-Exchange-Workshop/tree/module-2-ef5), and unzip it.
2. **Extract** the ZIP file to a folder on your computer.

#### Option B — Clone from GitHub

1. **Clone** the workshop repository from GitHub:
   ```bash
   git clone https://github.com/AHWALab/Water-Science-Exchange-Workshop/tree/module-2-ef5
   ```
2. **Navigate** to the workshop directory:
   ```bash
   cd EF5-Workshop
   ```

---

## Step 2 — Generate the model parameters

EF5 needs gridded parameters for the water-balance model (CREST) and the routing (KW). This step shows how they are derived from soil and basin data. Ready-made results already exist in `EF5_EVENT_MODEL/parameters/`.

### 2.1 Set up Google Colab

1. Open [Google Colab](https://colab.research.google.com/).
2. Click **File → Upload notebook** and select the notebook you want to run (e.g., `4_Crest_parameters_estimation.ipynb` or `KW_PINN_Predict.ipynb`).
3. Click **Runtime → Run all** to execute the entire notebook.

### 2.2 CREST parameters — `4_Crest_parameters_estimation.ipynb`

This notebook is part of the EF5 parameter generation workflow, from [GitHub repository EF5-builder-toolkit](https://github.com/AHWALab/EF5-builder-toolkit). It computes CREST soil parameters from SoilGrids sand and clay content (7 depths) and depth to bedrock:

| Output (in `parameters/`) | Parameter |
|---|---|
| `crest_Wm.tif` | Maximum soil water capacity (Wm) |
| `crest_b.tif` | Infiltration curve exponent (b) |
| `crest_Fc_Ksat.tif` | Soil saturated hydraulic conductivity (Fc / Ksat) |

Notes:
- **Skip the Google Colab cell if you are running a local version of Python** (`from google.colab import files`) when running on your own computer.
- If the `parameters/` folder does not exist, create it before saving the outputs.

### 2.3 KW routing parameters — `KW_PINN_Predict.ipynb`

Predicts the kinematic-wave rating-curve parameters **α (alpha)** and **β (beta)** with a pre-trained physics-informed neural network (KW-PINN, CONUS model v1.10). It uses basin descriptors in `predictors/` (drainage area, relief ratio, mean annual precipitation and temperature, aridity index, Manning's n). Predictions are made only on channel cells (`FAM > 50`).

| Output (in `parameters/`) | Parameter |
|---|---|
| `KW_alpha.tif` | Channel α |
| `KW_beta.tif` | Channel β |

Run all cells top to bottom. No GPU is needed.

---

## Step 3 — Run the event simulation

### 3.1 About the simulation

The control file `EF5_EVENT_MODEL/outputs_event/Control_file.txt` defines:

| Setting | Value |
|---|---|
| Model / routing | CREST + kinematic wave |
| Gauge | USGS 06605000 (lat 43.1304, lon −95.2113), basin area ≈ 1,064 km² |
| Precipitation | MRMS Pass 2 gauge-corrected QPE, hourly |
| PET | ERA5-adjusted monthly climatology |
| Period | 2024-06-16 00:00 → 2024-06-24 00:00 (hourly time step) |
| Initial states | `states/` (warm start at 2024-06-16 00:00) |

All paths in the control file are **relative to the `EF5_EVENT_MODEL` folder**, so the model must be run from there.

### 3.2 Run EF5

Open a terminal **inside the `EF5_EVENT_MODEL` folder** and run:

**Windows (PowerShell)**

```powershell
cd EF5_EVENT_MODEL
docker run -it --rm --platform linux/amd64 `
  -v "${PWD}:/work" -w /work `
  ef5-container /ef5/bin/ef5 outputs_event/Control_file.txt
```

**macOS / Linux (Terminal)**

```bash
cd EF5_EVENT_MODEL
docker run -it --rm --platform linux/amd64 \
  -v "$(pwd):/work" -w /work \
  ef5-container /ef5/bin/ef5 outputs_event/Control_file.txt
```

What the options do:

| Option | Meaning |
|---|---|
| `-v "${PWD}:/work"` | Makes your `EF5_EVENT_MODEL` folder visible inside the container as `/work` |
| `-w /work` | Runs EF5 from that folder, so the relative paths in the control file work |
| `--rm` | Deletes the container when it finishes (your results are kept) |
| `--platform linux/amd64` | Avoids the platform warning on ARM computers |

The run takes less than a minute on a typical laptop. To stop it early, press **Ctrl + C**. If that does not work, open another terminal and run `docker ps`, then `docker stop <CONTAINER_ID>`.

### 3.3 Outputs

Results are written to `EF5_EVENT_MODEL/outputs_event/`:

| File | Content |
|---|---|
| `ts.06605000.crest.csv` | Simulated and observed discharge time series at the gauge |
| `maxq.YYYYMMDD.HHMMSS.tif` | Maximum streamflow during the event (m³/s) |
| `maxunitq.YYYYMMDD.HHMMSS.tif` | Maximum unit streamflow (m³/s/km²) |
| `qpeaccum.YYYYMMDD.HHMMSS.tif` | Accumulated precipitation over the event (mm) |
| `results.json` | Run summary (run time, missing precipitation files) |

Open the `.tif` grids in QGIS or Python (`rasterio`), and plot the `.csv` to compare simulated vs. observed hydrographs.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `docker: command not found` / not recognized | Docker Desktop is not installed or not running. Open it, then restart your terminal. |
| `Cannot connect to the Docker daemon` | Docker Desktop is still starting. Wait until it shows *Engine running*. |
| `Failed to open configuration file /conf/control.txt` | The control file path was not passed. Use the full command in Step 3.2, including `/ef5/bin/ef5 outputs_event/Control_file.txt`. |
| EF5 cannot find DEM, precipitation or parameter files | You are not inside `EF5_EVENT_MODEL`, or `-w /work` is missing. Paths in the control file are relative to that folder. |
| A folder named like a file (e.g. `my_control.txt/`) appears | Docker creates an empty folder when the file in a `-v` option does not exist. Delete it and check the path. |
| `ModuleNotFoundError` in a notebook | Install the missing package in your environment (Step 2.1) and make sure the notebook kernel is that environment. |
| `ModuleNotFoundError: google.colab` | Skip that cell; it is only for Google Colab. |

---

## Credits
Santiago Henao-Gomez, University of Iowa, santiago-henao-gomez@uiowa.edu.

Humberto Vergara, University of Iowa, humberto-vergaraarrieta@uiowa.edu.

Mohamed Abdelkader, University of Iowa, mohamed-abdelkader@uiowa.edu.

Vanessa Robledo, University of Iowa, vanessa-robledodelgado@uiowa.edu.

Meet the research team: [AHWA Lab](https://ahwa.lab.uiowa.edu/)