#  My Capstone Project Setup Documentation 
### Do geomagnetic storms correlate with earthquakes?

## Author

**Paula Herrera** · [LinkedIn](https://www.linkedin.com/in/pshepm/) · [Scientific Articles](https://pubmed.ncbi.nlm.nih.gov/?term=herrera+espejel)
Data Analytics Bootcamp Capstone · [NeueFische](https://www.neuefische.de/) · Nov.2025–Dec.2026

---

An interactive Streamlit dashboard exploring the statistical relationship between
solar-driven geomagnetic activity (GFZ Kp index) and global earthquake patterns (USGS),
built as a data analytics capstone project (2025–2026).

> **Full project brief →** Check my [docs/About.md](docs/About.md)!

> **Product Slide Deck →** Check my [docs/Herrera_EDA_260414.md](docs/presentation/Herrera_EDA_260414.pdf)!

> **Live app demo**

![Storm & Quake dashboard demo](https://github.com/user-attachments/assets/11bd4bca-0eb7-42d8-b72f-a438b4de78d6)

---

## What it does

- Visualises 335,000+ earthquake events and 35,000 Kp intervals across 2014–2025
- Converts UTC timestamps to **Local Solar Time** at each epicentre to test diurnal patterns
- Provides interactive filters by year, country, magnitude, depth, and tectonic zone
- Overlays geomagnetic storm windows on earthquake frequency time series
- Displays polar rose diagrams (Kuiper-tested) of LST distributions by latitude zone

---

## Quickstart

```bash
# 1. Clone the repository
git clone git@github.com:<your-username>/da_capstone.git
cd da_capstone

# 2. Create and activate the Conda environment
conda create -n da_capstone python=3.13
conda activate da_capstone
pip install -r requirements.txt

# 3. Run the app
streamlit run src/app.py
```

> The app loads from `data/processed/`. Full datasets are gitignored.
> Run the demo notebook first to generate a small working sample — see **Demo** below.

---

## Demo (no full dataset required)

Two notebooks run end-to-end on the included sample files
without any API keys or the full dataset:

```bash
# Step 1 — generate sample raw JSON files
python notebooks/00_sample_scripts/01_sample_generator.ipynb

# Step 2 — open either demo notebook
jupyter notebook notebooks/00_sample_scripts/01_sample_generator.ipynb
jupyter notebook notebooks/00_sample_scripts/02_demo_pipeline.ipynb
```

---

## Repository Structure

```
da_capstone/
├── data/
│   ├── raw/                        # sample JSON files (full datasets gitignored)
│   ├── preprocessed/               # flattened JSON → CSV
│   ├── interim/                    # tidied datasets
│   ├── processed/                  # analysis-ready CSVs (gitignored)
│   └── geospatial/                 # tectonic plates + country boundaries (gitignored)
│       ├── tectonic_plates/        # (.shp, .dbf, .json, .prj …)
│       └── ne_110m_admin_0_countries/
├── notebooks/
│   ├── generate_sample_raw.py      # generates mock API responses
│   ├── demo_pipeline.ipynb         # ingestion → cleaning → feature engineering → EDA examples
│   ├── 01_USGS_Earthquakes_data/   # full pipeline (gitignored)
│   ├── 02_GFZ_kpindex_data/        # full pipeline (gitignored)
│   └── 03_NASA_SolarActivity_data/ # full pipeline (gitignored)
├── docs/
│   ├── About.md                    # full project brief & methodology
│   ├── summaries/                  # dataset summary markdown files
│   └── presentation/
│       └── product_slidedeck.pdf
├── src/
│   ├── homepage.py                 # homepage (entry point)
│   ├── pages/                      # page_1 … page_5 (gitignored)
│   ├── imports.py                  # centralised dependency management (gitignored)
│   ├── style.py                    # shared CSS & palette constants (gitignored)
│   └── __init__.py
├── .gitignore
├── requirements.txt
└── README.md
```

**File naming conventions**

| Stage | Pattern | Example |
|---|---|---|
| Raw | `raw_<dataset>.json` | `usgs_eq_raw_S1.json` |
| Preprocessed | `<dataset>_flat.csv` | `usgs_eq_flat.csv` |
| Interim | `<dataset>_clean.csv` | `usgs_eq_clean.csv` |
| Processed | `<dataset>_df.csv` | `usgs_eq_df.csv` |

---

## Data Sources

| Dataset | Provider | Coverage | Format | Access |
|---|---|---|---|---|
| Earthquake Catalogue | USGS ComCat | 2014–2025 · Mw ≥ 2.0 | GeoJSON | Open API · no key |
| Kp Index | GFZ Potsdam | 2014–2025 · 3-hourly | Fixed-width text | Open FTP · CC BY 4.0 |
| Solar Flares / CME / GST | NASA DONKI | 2014–2025 | JSON | API key required |

**NASA API key** — register for free at [api.nasa.gov](https://api.nasa.gov/).
Store your key in a `.env` file at the repo root (already gitignored):

```
NASA_API_KEY=your_key_here
```

---

## Stack

| Layer | Tools |
|---|---|
| Language | Python 3.13 |
| Data wrangling | pandas · numpy · geopandas |
| Statistical analysis | scipy · Kuiper circularity test (custom implementation) |
| Visualisation | Plotly Express · Plotly Graph Objects · Matplotlib · Seaborn |
| Dashboard | Streamlit · custom CSS via `st.markdown` |
| Environment | Conda · pip · VS Code |
| Version control | Git · GitHub (SSH) |

---

## Local Environment Setup

<details>
<summary><strong>macOS — first-time setup</strong></summary>

```bash
# Homebrew (package manager)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Tree utility (optional — for visualising folder structure)
brew install tree && tree -L 2

# Miniconda
cd ~/opt
bash Miniconda3-latest-MacOSX-x86_64.sh
conda activate base
```

</details>

<details>
<summary><strong>GitHub SSH setup (one-time)</strong></summary>

```bash
# Generate SSH key
ssh-keygen -t rsa -b 4096 -C "your@email.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa

# Copy public key → paste into GitHub → Settings → SSH keys
pbcopy < ~/.ssh/id_rsa.pub

# Test connection
ssh -T git@github.com
```

</details>

<details>
<summary><strong>Recreate the Conda environment from scratch</strong></summary>

```bash
conda env create -f environment.yml
conda activate da_capstone
```

</details>

---

## Typical Development Workflow

```bash
git pull                          # sync with remote
conda activate da_capstone        # activate environment
# work in src/ or notebooks/
git add .
git commit -m "descriptive message"
git push
```

---

*All data sourced from open scientific APIs. No personal data collected or processed.
GFZ Kp data: Matzka et al. (2021), CC BY 4.0, doi:10.5880/Kp.0001.*
