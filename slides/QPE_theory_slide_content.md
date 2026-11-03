# What is QPE, slide content for the 20 minute opening talk

Module 1 of "Predicting Flash Floods in Working Landscapes", CUAHSI Water Science Exchange 2026.
Phrase based content, one block per slide, with a figure suggestion and a speaker note. Eighteen slides for twenty minutes, about one minute each, with slides 6 to 8 reusable from the Summer Institute 2026 deck "Foundations of QPE" (COMET figures).

Frame of the talk. Low latency, near real time observations. Every source is presented with two numbers, how fine and how fast.

---

## Slide 1. Quantitative Precipitation Estimation for Flash Floods

- Module 1 of three. Rainfall first, then the model, then the evaluation
- One question for the morning. How much rain fell, where, and how soon did we know it
- Case study. Northwest Iowa, night of June 21 to 22, 2024

Figure. Workshop banner (CUAHSI2026_FlashFlood_workshop_banner_1920x1080.png) or the three module figure.

Speaker note. Set the frame in one sentence. Flash flood prediction starts with an estimate of rain that is already falling, so the quality and the delay of that estimate decide what the model can do.

## Slide 2. Why rainfall comes first

- A flash flood model is a converter. Rain in, discharge out
- Errors in the rain do not cancel, they propagate and often amplify
- Two requirements pull against each other. Accuracy and latency
- A perfect estimate that arrives after the crest has no value for a warning

Figure. Simple diagram, rainfall field to basin to hydrograph, with a clock between the first two boxes. Build in PowerPoint, black text.

Speaker note. Mention that Module 3 quantifies the propagation. Today we only look at the input.

## Slide 3. What QPE means

- Quantitative Precipitation Estimation. An estimate of how much precipitation reached the ground, on a grid, over a period
- Estimation, not measurement. Only gauges measure, everything else infers
- Three instrument families. Rain gauges, weather radar, satellites
- A fourth source fills gaps. Numerical weather models
- Operational products blend all four

Figure. The COMET figure with the three tools (Summer Institute deck, slide 3). Source, The COMET Program, UCAR MetEd, "Precipitation Estimates, Part 1, Measurement", used with attribution.

Speaker note. Keep the distinction between measurement and estimation, it returns in the exercise when we treat gauges as the reference.

## Slide 4. Rain gauges, the reference with its own errors

- Tipping bucket. Counts tips of a known volume. Cheap, fast, loses water at high intensity
- Weighing gauge. Weighs the catch. Handles snow and heavy rain, slower response
- Manual gauge. Read once a day. Simple and reliable, no timing
- Error sources. Wind undercatch, splash, evaporation, clogging, siting
- Representativeness. A 4 inch orifice stands for a 1 km grid cell

Figure. Photographs of a tipping bucket, a Geonor weighing gauge in its wind shield (USCRN) and a CoCoRaHS 4 inch gauge. Sources, NOAA NCEI USCRN instruments page, CoCoRaHS. Alternatively the COMET gauge figures.

Speaker note. The Doon gauge in Notebook 2 reads half of the radar value in the heaviest hour. Plant the question here.

## Slide 5. Gauge networks in the United States

- ASOS, about 950 airport stations, NWS, FAA and DoD, reports within minutes
- HADS, thousands of hydrological gauges relayed through GOES, hourly, the main input of MRMS
- USCRN, 114 climate reference stations in the lower 48, weighing gauge with three sensors, 5 min data
- COOP, more than 8,000 volunteers, daily, since the 1890s
- CoCoRaHS, more than 26,000 volunteers, daily 4 inch gauge, largest source of daily totals in the country
- State mesonets and local networks, for example the ISU Soil Moisture Network and the Iowa Flood Center sensors

Figure. Map of hourly gauges used by MRMS, Zhang et al. 2016, Figure 1b. Or the station map produced in Notebook 1, section 6a.

Speaker note. Density is uneven. Rural northwest Iowa has a handful of hourly gauges for a storm that covered several counties.

## Slide 6. What radar sees

Reuse Summer Institute 2026 deck, slides 8 to 13.

- Radar measures reflectivity Z, not rain
- Z depends on the sixth power of drop diameter
- Z to R conversion needs the drop size distribution, which changes with storm type
- Non hydrometeors reflect too. Insects, birds, ground clutter, hail

Figure. COMET figures already in the Summer Institute deck. Source, The COMET Program, UCAR MetEd.

Speaker note. Two minutes maximum for slides 6 to 8 combined. The audience is hydrologists, the point is where radar fails, not how it works.

## Slide 7. Where radar fails

Reuse Summer Institute 2026 deck, slides 15 to 18.

- The beam rises with range. About 1.5 km high at 100 km, more than 5 km at 230 km
- Terrain and buildings block the lowest beam
- Bright band near the melting layer inflates Z
- Hail inflates Z far more than rain
- Attenuation in heavy rain at C and X band
- Network. 158 WSR-88D radars, uneven spacing, large gaps in the West

Figure. CONUS radar coverage map (COMET, in the Summer Institute deck). Source, NWS Radar Operations Center for the radar count.

Speaker note. In Iowa the coverage is good. Keep in mind that the same products are used in the Mountain West where the radar sees almost nothing near the ground.

## Slide 8. Dual polarization changed the rate estimate

- Horizontal and vertical pulses. Differential reflectivity ZDR, specific differential phase KDP, specific attenuation A
- Rain drops flatten as they grow, so shape tells size
- MRMS since 2020. Synthetic rate from R(A) in pure rain, R(KDP) in hail and mixed phase, R(Z) elsewhere
- Less sensitive to calibration and partial blockage

Figure. Schematic of horizontal and vertical polarization with an oblate drop (COMET, Summer Institute deck slide 12). Source for the method, Zhang et al. 2020, Journal of Hydrometeorology.

Speaker note. One sentence on why this matters for the exercise. The radar only product of 2024 is already a dual polarization product.

## Slide 9. Satellites, coverage everywhere, detail nowhere

- Geostationary infrared. GOES every 10 minutes, 2 km. Sees cloud tops, infers rain. SCaMPR algorithm behind the GOES Rainfall Rate product
- Low Earth orbit microwave. GPM constellation, sees hydrometeors, passes a few times a day
- Blends. IMERG at 0.1 degree every 30 minutes. Early run 4 hours, Late run 12 to 14 hours, Final run 3.5 months with gauge adjustment
- Typical errors. Smooth fields, displaced cores, warm rain missed, cirrus mistaken for rain

Figure. Notebook 1, section 7, GOES RRQPE next to MRMS PrecipRate at 04 UTC June 22, 2024. Sources, NOAA TOWR-S GOES RRQPE page, NASA GPM data directory for IMERG latencies.

Speaker note. Most of the world relies on this family. Our Iowa case is a luxury of radar coverage.

## Slide 10. Models as gap fillers, not observations

- HRRR, 3 km, hourly, one hour precipitation from the first forecast hour
- Used inside MRMS where the radar quality index is low, in snow and stratiform rain
- National Water Model forcing. MRMS gauge corrected QPE blended with HRRR and RAP
- AORC. Analysis of Record for Calibration, 1 km hourly since 1979, made with a 10 day lag. The retrospective reference, not a real time product

Figure. The multi sensor decision tree from the NWS Warning Decision Training Division page on Multi-Sensor QPE. Source, https://vlab.noaa.gov/web/wdtd/-/multi-sensor-qpe

Speaker note. The audience will meet AORC again in Module 2 as model forcing. Place it here so the difference between a real time and a retrospective product is clear.

## Slide 11. Multi-sensor blending, the MRMS pipeline

- About 180 radars merged into one 3D reflectivity mosaic, 1 km, every 2 minutes
- Precipitation type at each pixel. Convective, stratiform, tropical, hail, snow
- Dual polarization synthetic rate, then accumulation. Radar only QPE
- Radar quality index per pixel
- Gauge correction. Local bias from about 7,000 hourly gauges, quality controlled against the radar
- Where radar is poor. Mountain Mapper with PRISM climatology, or model QPF
- Domain 20 to 55 N, 130 to 60 W, grid 0.01 degree

Figure. Flowchart of MRMS QPE products, Zhang et al. 2016, Figure 2 or Table 1. Source, Bulletin of the American Meteorological Society, 97, 621 to 638.

Speaker note. Everything participants download this morning comes out of this pipeline. Name the three files they will use, RadarOnly_QPE_01H, MultiSensor_QPE_01H_Pass1, MultiSensor_QPE_01H_Pass2.

## Slide 12. Pass 1 and Pass 2, the price of waiting

- Pass 1. About 20 minutes after the hour, the gauges that reported quickly
- Pass 2. About one hour after the hour, most of the gauges
- Measured in the AWS archive for June 22, 2024. Radar only median 11 minutes, Pass 1 median 18 minutes, Pass 2 median 68 minutes
- The gauge influence index tells where a gauge touched the estimate
- Older documentation says 60 and 120 minutes. That was the first version in 2020

Figure. Notebook 1, section 4, upload latency plot. Sources, NSSL MRMS operational product tables v12.2 for the nominal latencies, the notebook for the measured ones.

Speaker note. The NWS training page also lists the fraction of gauges in each pass, about 10 percent in Pass 1 and about 60 percent in Pass 2. Quote it as approximate.

## Slide 13. Stage IV, the analysis with people in the loop

- Twelve River Forecast Centers build regional radar plus gauge analyses with manual quality control
- NCEP mosaics them. Hourly, 6 hourly, 24 hourly ending 12 UTC
- Grid. HRAP polar stereographic, about 4 km
- First version within about an hour, remade hourly for 23 hours, then at 1, 3, 5 and 7 days
- The product of choice for post event analysis for two decades. MRMS now feeds several of the inputs

Figure. Notebook 1, section 5, MRMS Pass 2 and Stage IV side by side for the same hour. Source, NCEP EMC Stage IV page.

Speaker note. Stress the revision cycle. A Stage IV file downloaded on the day of the flood is not the same file one week later.

## Slide 14. The product landscape in two numbers

Table, fine against fast.

| Product | Resolution | Latency |
|---|---|---|
| MRMS radar only | 1 km, 2 min | minutes |
| GOES RRQPE | 2 km, 10 min | minutes |
| ASOS, HADS, mesonets | points | minutes |
| MRMS Pass 1 | 1 km, hourly | about 20 min |
| MRMS Pass 2 | 1 km, hourly | about 1 h |
| Stage IV first version | 4 km, hourly | about 1 h |
| USCRN | points | about 1 h |
| IMERG Early | 10 km, 30 min | 4 h |
| CoCoRaHS | points | next morning |
| Stage IV final | 4 km | 7 days |
| AORC | 1 km, hourly | retrospective |

Figure. The table itself, large font. No other graphic.

Speaker note. This is the slide to photograph. The notebooks follow the rows from top to bottom.

## Slide 15. The case, northwest Iowa, June 21 to 22, 2024

- Training thunderstorms over wet soils, 150 to 250 mm in a few hours
- Flash Flood Emergency for Rock Valley, 1:56 am CDT June 22, after a levee failure
- Rock River near Rock Valley, 157,000 cubic feet per second, record of 127 years
- Floyd River at Alton, 41,000 cubic feet per second, highest since 1953
- Same event in Module 2 (simulation) and Module 3 (evaluation)

Figure. Notebook 2, section 4, 24 hour storm totals from the three products, or the three module figure from the workshop announcement. Sources, NWS Sioux Falls warning text through the Iowa Environmental Mesonet archive, USGS NWIS sites 06483500 and 06600100.

Speaker note. Note the time. The emergency was issued two hours after the heaviest hour, which is roughly the latency of Pass 2.

## Slide 16. The next 100 minutes

- Notebook 1, 30 minutes. A tour of the sources. MRMS on AWS and at Iowa State, measured latency, Stage IV, four gauge networks, GOES
- Notebook 2, 60 minutes. One storm, three estimates. Radar only, Pass 1, Pass 2 against hourly gauges and CoCoRaHS, basin rainfall for the Floyd River, and the forecaster at 6 am
- Everything downloads live from public archives, a cache in the repository covers a slow network
- Objectives. Sources and their latency, access with Python, latency against accuracy, evaluation against gauges

Figure. The repository README, or a screenshot of the notebook table of contents.

Speaker note. Ask who has run Jupyter before. Pair newcomers with experienced neighbours.

## Slide 17. Key takeaways

- QPE is an estimate. Gauges measure points, radar and satellite infer, models fill
- No single source is enough, operational products blend them
- Faster means fewer gauges. Minutes for radar, about 20 minutes for Pass 1, about an hour for Pass 2, a week for the final Stage IV
- Check every product against gauges the product did not use
- Know the archive. AWS for speed and completeness, Iowa State for simplicity, IEM and NCEI for gauges

## Slide 18. References

- Zhang, J. and coauthors, 2016. Multi-Radar Multi-Sensor (MRMS) Quantitative Precipitation Estimation, Initial Operating Capabilities. Bull. Amer. Meteor. Soc., 97, 621 to 638. https://doi.org/10.1175/BAMS-D-14-00174.1
- Zhang, J., L. Tang, S. Cocks, P. Zhang, A. Ryzhkov, K. Howard, C. Langston and B. Kaney, 2020. A Dual-Polarization Radar Synthetic QPE for Operations. J. Hydrometeor., 21, 2507 to 2521. https://doi.org/10.1175/JHM-D-19-0194.1
- Fulton, R. A., D. J. Seo and J. Breidenbach, 2002. Quantitative Precipitation Estimation in the National Weather Service. AMS Short Course on QPE and QPF, Orlando. (Resources folder, qpe_nws_overview.pdf)
- Kuligowski, R. J., 2002. A Self-Calibrating Real-Time GOES Rainfall Algorithm for Short-Term Rainfall Estimates. J. Hydrometeor., 3, 112 to 130.
- The COMET Program, UCAR MetEd. Precipitation Estimates, Part 1, Measurement. https://www.meted.ucar.edu/
- Hogsett, W., 2023. Weather Radar Principles. WMO RA IV Tropical Meteorology Course. (Resources folder)
- NOAA NSSL, MRMS operational product tables, v12.2. https://nssl.noaa.gov/projects/mrms/operational/tables.php
- NOAA NWS WDTD, Multi-Sensor QPE. https://vlab.noaa.gov/web/wdtd/-/multi-sensor-qpe
- NOAA NCEP EMC, Stage IV. https://www.emc.ncep.noaa.gov/mmb/SREF/pcpanl/
- NOAA TOWR-S, GOES RRQPE. https://vlab.noaa.gov/web/towr-s/goes-rrqpe
- NASA GPM data directory. https://gpm.nasa.gov/data/directory
- Project Pythia MRMS Cookbook. https://projectpythia.org/mrms-cookbook/

---

## Notes for building the deck

- Reuse. Summer Institute 2026 deck "Foundations of QPE" (Precipitation_Measurement_COMET_SI2026.pptx) covers slides 3, 6, 7 and 8 above with COMET figures and the attribution line already in place.
- New figures to export from the notebooks. Latency plot (Notebook 1, section 4), MRMS against Stage IV (Notebook 1, section 5), GOES against MRMS (Notebook 1, section 7), storm totals (Notebook 2, section 4). Export at 200 dpi with `fig.savefig(name, dpi=200, bbox_inches="tight")`.
- Figures from Zhang et al. 2016 (BAMS) are under the AMS copyright. Educational use with citation is customary, do not redistribute the PDF in the repository.
- Numbers to verify before the talk if time allows. The gauge fractions for Pass 1 and Pass 2 (10 and 60 percent on the WDTD page, which also carries older latency figures in its limitations section).
- Garcia, M., 2005, "NOAA-NWS QPE, a NASA perspective" (Resources folder, 101574694.pdf) is historical context on NLDAS and Stage II. Not needed for the talk.
