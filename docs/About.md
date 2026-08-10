# Storm & Quake — About This Project

> *Can solar-driven electromagnetic activity influence earthquake patterns on Earth
> or is any apparent overlap just coincidence?*

> This project investigates earthquake and solar activity events through eleven years of open scientific data, interactive visualisations, and a museum-inspired Streamlit dashboard app.

Paula Herrera  | 2026.02.17 (updated 2026.08.08) 🌈⃤. 
---

## The Concept

A fictional professional scientific institute wants to present earthquake and solar-activity data on their website as an immersive, museum-like dashboard: one that lets visitors *explore* rather than simply read. This Streamlit application is the first minimal version of that product, developed as part of my data analytics bootcamp capstone project.

The aim of the project was to design and develop the full pipeline from raw API ingestion to a first polished interactive interface providing key metrics and statistics for exploring earthquakes and solar activity across the world. 

---

## Research Background 🕵️‍♂️

Ancient Mesoamerican cultures believed celestial phenomena influenced events on Earth.
Modern geophysics revisits this intuition with quantitative and sensor-based methodologies: a 2020 hypothesis proposes that
geomagnetic storms may disturb the ionosphere in ways that induce electrical currents
in the Earth's crust, potentially triggering already-stressed tectonic faults and affecting activity in our lithosphere.

This project investigates whether such a relationship is empirically observable using
publicly available data from USGS and GFZ Potsdam!

**Selected literature**

- Marchetti et al. (2020) — *Nature Scientific Reports* · [doi link](https://www.nature.com/articles/s41598-020-67860-3)
- Han et al. (2022) — *Atmosphere* (MDPI) · [doi link](https://www.mdpi.com/2073-4433/13/7/1131)
- Ouzounov et al. (2023) — *Springer* · [doi link](https://link.springer.com/article/10.1007/s44195-023-00042-6)

---

## Hypotheses

> **H1 — Solar-time signal.** If solar electromagnetic forces influence earthquake timing, events should cluster around specific *local solar hours* at the epicentre rather than appearing uniformly distributed across the day.   

H1 requires converting every UTC timestamp to Local Mean Solar Time using the epicentre's longitude.
The formula to calculate local solar time is $LST = \text{UTC} + \frac{\text{Longitude}}{15}$ where longitude is in degrees.


> **H2 — Intersectional filter.** Any solar influence would likely be category-specific. That is, patterns may be visible only when filtering by magnitude class, depth regime, tectonic setting, or latitude zone rather than a global signal across all earthquake types. 

H2 requiered chosing and testing different categories (magintude, depth in km, latitude band, etc.). The aim was to apply intersectional theory to earthquake characteristics and test the conditionality of H1.

---

## Data Sources

### USGS Earthquake Catalogue (ComCat)

| Field | Detail |
|---|---|
| Provider | U.S. Geological Survey (USGS) |
| Endpoint | `https://earthquake.usgs.gov/fdsnws/event/1/query` |
| Access | RESTful HTTPS GET · no authentication required |
| Format | GeoJSON |
| Coverage | 2014 – 2025 · Mw ≥ 2.0 globally |
| Key variables | `start_time`, `mag`, `depth_km`, `latitude`, `longitude`, `duration`, `tsunami` |

The USGS collects data via the Advanced National Seismic System (ANSS) and the Global
Seismographic Network (GSN). When an earthquake occurs, seismic waves are recorded by
multiple stations and transmitted to the National Earthquake Information Center (NEIC)
in Golden, Colorado, where automated systems determine location, depth, and magnitude.

### GFZ Potsdam — Kp Index

| Field | Detail |
|---|---|
| Provider | Helmholtz Centre Potsdam — GFZ German Research Centre |
| Endpoint | `ftp://ftp.gfz-potsdam.de/pub/home/obs/kp-ap/` |
| Access | FTP download · no authentication required |
| Format | Fixed-width text, parsed to CSV |
| Coverage | 2014 – 2025 · 3-hourly resolution (8 readings / day) |
| Key variables | `start_time`, `kp`, `kp_category`, `storm`, `subsolar_lat`, `subsolar_lon` |
| License | CC BY 4.0 — Matzka et al. (2021), doi:10.5880/Kp.0001 |

The Kp index is the standard planetary geomagnetic activity measure, derived from 13
mid-latitude observatories worldwide and published every three hours on a 0–9 scale.

---

## System Architecture & Data Pipeline

```
USGS API (GeoJSON)          GFZ FTP (fixed-width text)
       │                              │
       ▼                              ▼
  01 · API call / download      01 · file fetch
  02 · JSON flattening          02 · parse + tidy
  03 · CSV tidying              03 · dataset summary
  04 · dataset summary          04 · EDA
  05 · EDA                            │
       │                              │
       └──────────────┬───────────────┘
                      ▼
             Feature engineering
             (LST · depth bands · latitude zones ·
              magnitude classes · storm flags ·
              subsolar lat/lon · tectonic proxy zone)
                      │
                      ▼
              data/processed/*.csv
                      │
                      ▼
              Streamlit app  (src/)
              Pages 1–5 · Plotly · custom CSS
```

All stages are documented in numbered Jupyter notebooks under `notebooks/`.  

---

## My Engineering Challenges (What I learned!)

### 1 · UTC to Local Solar Time

**Situation.** USGS and GFZ log every event in UTC. Investigating whether solar position at the moment of an earthquake matters requires converting each timestamp to the *local solar time* at the epicentre (i.e., not the local clock time, which is distorted by political timezone boundaries and daylight saving shifts).

**Action.** Derived Local Mean Solar Time ($\text{LMST}$) analytically:

$$\text{LMST} = \text{UTC} + \frac{\text{Longitude}}{15}$$

*(Note: Longitude is expressed in degrees, where East is positive and West is negative).*

Earth rotates 15° per hour, so dividing longitude by 15 converts geographic position directly to a solar-hour offset. Each earthquake was re-stamped to this solar reference frame, enabling the `lst_hour` (lmst), `is_daylight`, and latitude-zone rose diagrams.

**Result.** Enabled precise circadian analysis on any combination of location, depth,
magnitude class, and tectonic setting to assess Hypothesis 1.

---

### 2 · Temporal Resolution Mismatch (Many-to-One Alignment)

**Situation.** USGS events are timestamped to the millisecond; GFZ Kp intervals are
3-hourly averages. A naive join would produce many-to-one duplicates or lose the
earthquake-level granularity.

**Action.** I used a "time-bucketing" strategy. I floored each earthquake’s UTC timestamp to its corresponding 3-hour boundary before executing a left-join

```python
# Floor timestamps to align millisecond data with 3-hour intervals
eq["kp_interval"] = eq["start_time"].dt.floor("3h")

# Left join to preserve unique earthquake records
merged = eq.merge(kp, left_on="kp_interval", right_on="start_time", how="left")
```

Left join preserves every earthquake; Kp columns (`kp`, `kp_category`, `storm`,
`subsolar_lat/lon`) are appended to each event row reflecting concurrent geomagnetic
conditions.

**Result.** Created a single, analysis-ready table of 335,000 events mapped across 35,000 Kp intervals. Every earthquake record was successfully preserved with zero row loss and zero synthetic duplicates.

---

### 3 · Streamlit UI Customisation ("Vibe Coding" CSS)

**Situation.** Default Streamlit applications share an identical visual language. I am not familiar (or was not) with frontend code. 

**Action.** 
All CSS was developed iteratively ("vibe coded") using Claude as a pair programmer,
as it was my first experience with CSS-in-Python! Very interesting to see how AI can help code a first version of a streamlit app...

**Result.** A minimal version of my museum-like product wrapper that transformed my standard Python script into a consumer-grade dashboard.

---

### 4 · Architectural Paradigm: Shifting from ETL to ELT
**ELT (Extract, Load, Transform)** 
When building data projects, you can either clean the data before saving it (ETL) or after saving it (ELT). I chose the second option (ELT), and here is how it works: 
- Extract & Load (EL): I downloaded the files from the global websites and saved them directly into my project folders in their original, untouched formats.  
- Transform (T): Then, I loaded those original files into Python to clean them, remove noise, create a tidy version, and calculate new variables (like local day vs. night time).  

---

## Skills Demonstrated

| Area | Tools & Techniques |
|---|---|
| **Data engineering** | REST API ingestion · JSON flattening · multi-source merging · temporal alignment |
| **Data wrangling** | pandas · numpy · null handling · dtype casting · deduplication |
| **Geospatial** | geopandas · plate boundary proximity (Bird 2003) · reverse geocoding |
| **Statistical analysis** | Kuiper circularity test · descriptive statistics · storm-window comparison |
| **Visualisation** | Plotly Express + Graph Objects · polar rose diagrams · animated dual-panel world map |
| **Dashboard** | Streamlit multipage app · `@st.cache_data` · custom CSS · interactive sidebar filters |
| **Software practices** | Modular notebook pipeline · `.gitignore` · `requirements.txt` · demo notebooks for reproducibility |

`````
Note: The aim of the project is to demonstrate my ability to 
    (1) identify, extract, transform and load original data sourced from publicly-available scientific APIs as the result of real-time sensor technology and satellites; 
    (2) clean, handle missing values, and create basic summaries;
    (3) bring together different datasets with different formats together;
    (4) select and conduct specific descriptive & advanced statistical analyses;
    (5) handle complex granular geospatial and timestamp variables;
    (6) generate beautiful, colorful and enticing visualizations;
    (7) go beyond static results and create functional dashboards via streamlit.
`````

---

## Project Structure (public repo)

```
da_capstone/
├── data/raw/          # sample JSON files (full datasets gitignored)
│   ├── data/gfz_sample_raw.json      # 
│   └── data/usgs_sample_raw.json     # 
├── notebooks/
│   ├── demo_ETL_pipeline.ipynb       # refactored pipeline slice (runnable)
│   └── demo_dashboard_code.ipynb     # annotated Plotly rose chart snippet
├── docs/
│   ├── About.md                      # this file
│   └── presentation/Herrera_EDA_14.04.26.pdf # Graduation Presentation
└── requirements.txt
└── README.md
```

---

## My Working Datasets 🗂️ (after preprocessing)

#### Earthquake Data (Accessed: 2026-03-11)
<!-- Include the generated summary -->
[View detailed summary](summaries/eq_summary.md)

#### Solar Flare Data (Accessed: 2026-02-22)
<!-- Include the generated summary -->
[View detailed summary](summaries/slr_summary.md)

---

*Project developed as a capstone for a data analytics bootcamp, 2025–2026.
All data sourced from open scientific APIs. No personal data collected or processed.*