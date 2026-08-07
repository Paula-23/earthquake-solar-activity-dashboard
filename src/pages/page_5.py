import streamlit as st
import pandas as pd

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ETL Process & Sources · Storm & Quake",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { background-color:#04060f; color:#e8eaf0; font-family:'Inter',sans-serif; }
.main { background-color:#04060f; }
.block-container { padding:1.5rem 2.5rem 5rem 2.5rem !important; max-width:1200px; }

/* ── Page header ── */
.page-header {
    background: radial-gradient(ellipse 70% 80% at 0% 50%,  #0d3b2e33 0%, transparent 60%),
                radial-gradient(ellipse 50% 60% at 100% 0%, #1a1a4e44 0%, transparent 55%),
                linear-gradient(135deg, #060d1a 0%, #04060f 100%);
    border:1px solid #1e3a5f44; border-radius:14px;
    padding:2.2rem 2.8rem 2rem 2.8rem; margin-bottom:2rem;
    position:relative; overflow:hidden;
}
.page-header::before {
    content:''; position:absolute; inset:0;
    background: radial-gradient(ellipse 30% 40% at 80% 60%, #00c4940a 0%, transparent 60%),
                radial-gradient(ellipse 20% 30% at 10% 30%, #5b8aff08 0%, transparent 55%);
    pointer-events:none;
}
.page-eyebrow { font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.25em; text-transform:uppercase; color:#00c494; margin-bottom:0.7rem; }
.page-title   { font-family:'Satisfy',sans-serif; font-size:2.2rem; font-weight:800; color:#f0f4ff; margin:0 0 0.5rem 0; line-height:1.1; }
.page-title .ag { color:#00c494; }
.page-title .ab { color:#5b8aff; }
.page-desc    { font-size:0.92rem; color:#5a7a9a; line-height:1.75; max-width:780px; }

/* ── Section labels ── */
.section-label { font-family:'Space Mono',monospace; font-size:0.63rem; letter-spacing:0.22em; text-transform:uppercase; color:#00c494; margin-bottom:0.3rem; }
.section-title { font-family:'Satisfy',sans-serif; font-size:1.45rem; font-weight:700; color:#e8eaf0; margin-bottom:1rem; line-height:1.2; }
.section-title .ag { color:#00c494; }
.section-title .ab { color:#5b8aff; }

/* ── Divider ── */
.aurora-divider { height:1px; background:linear-gradient(90deg,transparent,#1e3a5f,#00c49433,#1e3a5f,transparent); margin:2.5rem 0; }

/* ── Workflow pipeline ── */
.pipeline {
    display:flex; flex-wrap:wrap; align-items:center;
    gap:0; margin:1.5rem 0 0.5rem 0;
}
.pipe-step {
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    background:linear-gradient(135deg,#0b1628 0%,#0d1f3a 100%);
    border:1px solid #1e3a5f66; border-radius:10px;
    padding:0.9rem 1rem; text-align:center;
    min-width:110px; flex:1;
    transition:border-color 0.2s, transform 0.2s;
    position:relative;
}
.pipe-step:hover { border-color:#00c49455; transform:translateY(-2px); }
.pipe-icon  { font-size:1.4rem; margin-bottom:0.35rem; }
.pipe-label { font-family:'Space Mono',monospace; font-size:0.6rem; letter-spacing:0.08em; text-transform:uppercase; color:#4a6a8a; line-height:1.4; }
.pipe-arrow {
    font-size:1rem; color:#1e3a5f; padding:0 0.3rem;
    flex-shrink:0; align-self:center;
}

/* ── Source cards ── */
.source-card {
    background:linear-gradient(135deg,#0b1628 0%,#0d1f3a 100%);
    border:1px solid #1e3a5f55; border-radius:12px;
    padding:1.6rem 1.8rem; margin-bottom:1.2rem;
    position:relative; overflow:hidden;
}
.source-card::before {
    content:attr(data-num);
    position:absolute; right:1.4rem; top:0.8rem;
    font-family:'Satisfy',sans-serif; font-size:3.5rem; font-weight:800;
    color:#ffffff06; line-height:1;
}
.source-tag { display:inline-block; font-family:'Space Mono',monospace; font-size:0.6rem; letter-spacing:0.12em; text-transform:uppercase; padding:0.2rem 0.6rem; border-radius:4px; margin-bottom:0.7rem; }
.tag-usgs { background:#5b8aff12; border:1px solid #5b8aff33; color:#5b8aff; }
.tag-gfz  { background:#00c49412; border:1px solid #00c49433; color:#00c494; }
.source-name { font-family:'Satisfy',sans-serif; font-size:1.1rem; font-weight:700; color:#e8eaf0; margin-bottom:0.3rem; }
.source-url  { font-family:'Space Mono',monospace; font-size:0.68rem; color:#3a5a7a; margin-bottom:0.9rem; }
.source-desc { font-size:0.88rem; color:#6a8aaa; line-height:1.75; margin-bottom:1rem; }

/* ── Meta table ── */
.meta-table { width:100%; border-collapse:collapse; margin-top:0.6rem; }
.meta-table td { padding:0.45rem 0.8rem; font-size:0.82rem; border-bottom:1px solid #1e3a5f33; }
.meta-table td:first-child { font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.08em; text-transform:uppercase; color:#3a5a7a; width:180px; white-space:nowrap; }
.meta-table td:last-child  { color:#7a9cc0; }
.meta-table tr:last-child td { border-bottom:none; }

/* ── Schema table ── */
.schema-wrap { background:#060d1a; border:1px solid #1e3a5f44; border-radius:8px; overflow:hidden; margin-top:0.8rem; }
.schema-header { display:grid; gap:0; background:#0a1828; padding:0.5rem 1rem; font-family:'Space Mono',monospace; font-size:0.6rem; letter-spacing:0.1em; text-transform:uppercase; color:#2a4a6a; }
.schema-row { display:grid; padding:0.35rem 1rem; border-bottom:1px solid #1e3a5f22; transition:background 0.15s; }
.schema-row:hover { background:#0b1628; }
.schema-row:last-child { border-bottom:none; }
.col-num   { font-family:'Space Mono',monospace; font-size:0.68rem; color:#2a4a6a; }
.col-name  { font-family:'Space Mono',monospace; font-size:0.72rem; color:#00c494; }
.col-dtype { font-family:'Space Mono',monospace; font-size:0.65rem; color:#3a5a7a; }
.col-desc  { font-size:0.78rem; color:#4a6a8a; }

/* ── Data quality pills ── */
.dq-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:0.7rem; margin:0.8rem 0; }
.dq-pill { background:#0b1628; border:1px solid #1e3a5f55; border-radius:8px; padding:0.8rem 1rem; }
.dq-val  { font-family:'Satisfy',sans-serif; font-size:1.3rem; font-weight:800; line-height:1; margin-bottom:0.2rem; }
.dq-lbl  { font-family:'Space Mono',monospace; font-size:0.58rem; letter-spacing:0.1em; text-transform:uppercase; color:#2a4a6a; }

/* ── Merge box ── */
.merge-box { background:linear-gradient(135deg,#060f1e 0%,#081428 100%); border:1px solid #1e3a5f88; border-left:4px solid #5b8aff; border-radius:10px; padding:1.4rem 1.8rem; margin:1rem 0; }
.merge-formula { font-family:'Space Mono',monospace; font-size:0.88rem; color:#5b8aff; background:#5b8aff0d; border:1px solid #5b8aff22; border-radius:6px; padding:0.6rem 1.1rem; margin:0.7rem 0; }
.merge-note { font-size:0.84rem; color:#4a6a8a; line-height:1.7; }
.merge-note strong { color:#8aaccc; }
.merge-note em     { color:#5b8aff; font-style:normal; }

/* ── Limitation card ── */
.limit-item { display:flex; gap:0.9rem; align-items:flex-start; margin-bottom:0.8rem; padding:0.9rem 1.1rem; background:#0b162888; border:1px solid #1e3a5f33; border-radius:8px; }
.limit-icon { font-size:1.1rem; flex-shrink:0; margin-top:0.05rem; }
.limit-text { font-size:0.87rem; color:#6a8aaa; line-height:1.65; }
.limit-text strong { color:#e8eaf0; }

/* ── Folder tree ── */
.folder-tree { background:#060d1a; border:1px solid #1e3a5f44; border-radius:8px; padding:1.2rem 1.4rem; font-family:'Space Mono',monospace; font-size:0.72rem; line-height:2; color:#3a5a7a; }
.folder-tree .dir  { color:#5b8aff; }
.folder-tree .file { color:#4a6a8a; }
.folder-tree .note { color:#1e3a5f; font-style:italic; }

/* ── Repro box ── */
.repro-box { background:linear-gradient(135deg,#060f1e 0%,#081428 100%); border:1px solid #1e3a5f88; border-left:4px solid #00c494; border-radius:10px; padding:1.4rem 1.8rem; margin:1rem 0; }
.repro-box code { font-family:'Space Mono',monospace; font-size:0.75rem; color:#00c494; background:#00c4940d; padding:0.15rem 0.4rem; border-radius:3px; }

/* ── License tag ── */
.license-row { display:flex; flex-wrap:wrap; gap:0.6rem; margin:0.6rem 0; }
.license-badge { font-family:'Space Mono',monospace; font-size:0.62rem; padding:0.25rem 0.7rem; border-radius:20px; }
.lb-open  { background:#00c49412; border:1px solid #00c49433; color:#00c494; }
.lb-cc    { background:#5b8aff12; border:1px solid #5b8aff33; color:#5b8aff; }
.lb-warn  { background:#f4c54212; border:1px solid #f4c54233; color:#f4c542; }

/* ── Footer ── */
.footer { text-align:center; font-family:'Space Mono',monospace; font-size:0.58rem; color:#1a2a3a; letter-spacing:0.12em; padding:2rem 0 0 0; border-top:1px solid #0e1e2e; margin-top:3rem; line-height:2; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="page-header">
  <div class="page-eyebrow">🔧 Page 5 · Paula's Awesome ETL Process &amp; Data Sources</div>
  <div class="page-title">From <span class="ag">Raw Data</span> to <span class="ab">Analysis-Ready</span></div>
  <div class="page-desc">
    This page documents my full Extract–Transform–Load (ETL) pipeline behind this project:
    Here I describe where the data comes from, how I obtained, cleaned, merged, and enriched it with
    derived features. I also talk about known limitations in the ingested datasets.
    All code is version-controlled and reproducible from the project repository.... 
    the only barrier are the digital skills and literacy needed for its reproduction 😶
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — PIPELINE WORKFLOW
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">Pipeline Overview</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">My End-to-End <span class="ag">Workflow</span></div>', unsafe_allow_html=True)

steps = [
    ("🔍", "Source\nSelection"),
    ("📡", "Raw Data\nIngestion"),
    ("🧹", "Clean &\nTransform"),
    ("⚙️", "Feature\nEngineering"),
    ("🔢", "EDA &\nSummaries"),
    ("💡", "Hypothesis\nGeneration"),
    ("🔥", "Streamlit\nApp"),
    ("🏳️‍🌈", "Design &\nArtwork"),
]

pipeline_html = '<div class="pipeline">'
for i, (icon, label) in enumerate(steps):
    pipeline_html += f"""
    <div class="pipe-step">
      <div class="pipe-icon">{icon}</div>
      <div class="pipe-label">{label}</div>
    </div>"""
    if i < len(steps) - 1:
        pipeline_html += '<div class="pipe-arrow">→</div>'
pipeline_html += '</div>'
st.markdown(pipeline_html, unsafe_allow_html=True)

# Step descriptions
with st.expander("▸ Expand pipeline step descriptions", expanded=False):
    step_details = [
        ("🔍 Source Selection",
         "Identified two open-access, high-resolution datasets covering the same temporal window (2014–2025): the USGS ComCat earthquake catalogue and the GFZ Potsdam Kp-index series. Selection criteria: global coverage, 3-hourly or finer resolution, open API access, and overlapping date ranges."),
        ("📡 Raw Data Ingestion",
         "USGS data retrieved via RESTful HTTPS GET requests to the ComCat API, paginated by time window and magnitude threshold (≥2.0 Mw). GFZ Kp data downloaded as structured text files from the GFZ FTP server. Raw responses saved as JSON / CSV in `data/raw/` without modification."),
        ("🧹 Clean & Transform",
         "Standardised column names (snake_case), parsed UTC timestamps, cast numeric types, removed duplicate event IDs, handled nulls per column policy (drop vs impute vs flag). Normalised magnitude types to Mw-equivalent where possible. Saved clean intermediates to `data/interim/`."),
        ("⚙️ Feature Engineering",
         "Derived: `year_month`, `day_of_year`, `week`, `solar_cycle_phase`, `kp_category`, `storm_group`, `local_solar_time`, `lst_hour`, `solar_offset`, `is_daylight`, `latitude_zone`, `latitude_zone_5`, `tectonic_proxy_zone`, `dist_to_boundary_km`, `mag_category`, `depth_km_category`, `duration_category`, `is_prolonged_shaking`, `subsolar_lat`, `subsolar_lon`, `auroral_activity_proxy`. Saved to `data/processed/`."),
        ("🔢 EDA & Summaries",
         "Univariate and bivariate analysis per dataset. Distribution checks, time-series decomposition, cross-correlation with lag analysis, Kuiper circularity tests on LST distributions. Documented in Jupyter notebooks `05_eda.ipynb` for each source."),
        ("💡 Hypothesis Generation",
         "Visual inspection and statistical tests guided formulation of specific testable hypotheses around storm-window earthquake frequency shifts, LST non-uniformity by latitude zone, and seasonal confounders."),
        ("🔥 Streamlit App",
         "Multi-page Streamlit application built in `src/`. Shared style and import utilities in `style.py` and `imports.py`. Pages loaded via `st.switch_page()`. Deployed locally; reproducible from `requirements.txt`."),
        ("🏳‍⚧ Design & Artwork",
         "Custom visual identity: dark cosmic colour palette, Space Mono + Syne typography, handmade LAIC conceptual diagram, aurora CSS animations. All original artwork and figures stored in `docs/figures/`. The CSS code was create with vibe coding with Claude and ChatGPT."),
    ]
    for title, desc in step_details:
        st.markdown(f"""
        <div style="margin-bottom:0.8rem; padding:0.8rem 1.1rem;
                    background:#0b162888; border:1px solid #1e3a5f33; border-radius:8px;">
          <div style="font-family:'Satisfy',sans-serif;font-size:0.95rem;font-weight:700;
                      color:#e8eaf0;margin-bottom:0.3rem;">{title}</div>
          <div style="font-size:0.85rem;color:#5a7a9a;line-height:1.7;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — PROJECT FOLDER STRUCTURE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Repository Layout</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Project <span class="ag">Folder Structure</span></div>', unsafe_allow_html=True)

col_tree, col_note = st.columns([2, 3], gap="large")

with col_tree:
    st.markdown("""
    <div class="folder-tree">
      <span class="dir">da_capstone/</span><br>
      ├── <span class="dir">data/</span><br>
      │   ├── <span class="dir">raw/</span>         <span class="note"># untouched API responses</span><br>
      │   ├── <span class="dir">interim/</span>     <span class="note"># cleaned, not yet merged</span><br>
      │   ├── <span class="dir">processed/</span>   <span class="note"># features added, analysis-ready</span><br>
      │   ├── <span class="dir">ready/</span>        <span class="note"># final merged dataset</span><br>
      │   └── <span class="dir">geospatial/</span>  <span class="note"># plate boundary shapefiles</span><br>
      ├── <span class="dir">docs/</span><br>
      │   ├── <span class="dir">figures/</span>     <span class="note"># LAIC diagram, illustrations</span><br>
      │   ├── <span class="file">setup.md</span><br>
      │   └── <span class="file">doc.md</span><br>
      ├── <span class="dir">notebooks/</span><br>
      │   ├── <span class="dir">01_USGS_eq/</span><br>
      │   │   ├── <span class="file">01_api_call.ipynb</span><br>
      │   │   ├── <span class="file">02_json_flattening.ipynb</span><br>
      │   │   ├── <span class="file">03_csv_tidying.ipynb</span><br>
      │   │   ├── <span class="file">04_summary.ipynb</span><br>
      │   │   └── <span class="file">05_eda.ipynb</span><br>
      │   └── <span class="dir">02_GFZ_kp/</span><br>
      │       ├── <span class="file">01_api_call.ipynb</span><br>
      │       ├── <span class="file">02_json_flattening.ipynb</span><br>
      │       ├── <span class="file">03_csv_tidying.ipynb</span><br>
      │       ├── <span class="file">04_summary.ipynb</span><br>
      │       └── <span class="file">05_eda.ipynb</span><br>
      ├── <span class="dir">src/</span><br>
      │   ├── <span class="file">app.py</span>      <span class="note"># homepage</span><br>
      │   ├── <span class="dir">pages/</span>       <span class="note"># page_1 … page_5</span><br>
      │   ├── <span class="file">imports.py</span><br>
      │   └── <span class="file">style.py</span><br>
      ├── <span class="file">.env</span>            <span class="note"># secrets (gitignored)</span><br>
      ├── <span class="file">.gitignore</span><br>
      ├── <span class="file">README.md</span><br>
      └── <span class="file">requirements.txt</span>
    </div>
    """, unsafe_allow_html=True)

with col_note:
    st.markdown("""
    <p style="font-size:0.88rem;color:#5a7a9a;line-height:1.8;margin-bottom:1rem;">
      The project followed a <strong style="color:#e8eaf0;">layered data architecture</strong>:
      each stage of processing had its own folder so that raw data was never overwritten
      and any step should be able to be re-ran independently.
    </p>
    """, unsafe_allow_html=True)

    notebook_steps = [
        ("01", "api_call", "Paginates the USGS ComCat API or fetches GFZ files. Saves raw JSON/CSV without modification."),
        ("02", "json_flattening", "Unnests nested GeoJSON feature properties into a flat tabular structure."),
        ("03", "csv_tidying", "Renames columns, casts dtypes, parses UTC timestamps, drops exact duplicates."),
        ("04", "summary", "Generates descriptive statistics, null counts, value distributions — saved as HTML reports."),
        ("05", "eda", "Bivariate analysis, time-series plots, cross-dataset comparisons, hypothesis notes."),
    ]
    for num, name, desc in notebook_steps:
        st.markdown(f"""
        <div style="display:flex;gap:0.8rem;align-items:flex-start;margin-bottom:0.65rem;
                    padding:0.75rem 1rem;background:#0b162855;border:1px solid #1e3a5f33;border-radius:8px;">
          <span style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#00c494;
                       background:#00c49415;border:1px solid #00c49433;border-radius:4px;
                       padding:0.1rem 0.4rem;flex-shrink:0;margin-top:0.1rem;">{num}</span>
          <div>
            <div style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#5b8aff;
                        margin-bottom:0.2rem;">{name}.ipynb</div>
            <div style="font-size:0.82rem;color:#4a6a8a;line-height:1.55;">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — DATA SOURCES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Data Sources</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Source <span class="ab">Documentation</span></div>', unsafe_allow_html=True)

# ── Source 1: USGS ────────────────────────────────────────────────────────────
st.markdown("""
<div class="source-card" data-num="01">
  <span class="source-tag tag-usgs">Source 01 · Seismicity</span>
  <div class="source-name">🌍 USGS Earthquake Catalog (ComCat)</div>
  <div class="source-url">https://earthquake.usgs.gov/fdsnws/event/1/</div>
  <div class="source-desc">
    The USGS collects earthquake data using a global network of seismometers — highly sensitive
    instruments that detect ground motion caused by seismic waves. These form part of the
    Advanced National Seismic System (ANSS) in the U.S. and the Global Seismographic Network (GSN)
    worldwide. When an earthquake occurs, seismic waves are recorded by multiple stations and
    transmitted to the National Earthquake Information Center (NEIC) in Golden, Colorado, where
    automated systems and seismologists determine the event's location, depth, magnitude, and timing.
  </div>
  <table class="meta-table">
    <tr><td>Theme</td>           <td>Seismic Activity on Earth</td></tr>
    <tr><td>Provider</td>        <td>U.S. Geological Survey (USGS)</td></tr>
    <tr><td>Endpoint</td>        <td>https://earthquake.usgs.gov/fdsnws/event/1/query</td></tr>
    <tr><td>Access Method</td>   <td>RESTful HTTPS GET (FDSN Web Service standard)</td></tr>
    <tr><td>Data Format</td>     <td>GeoJSON (primary) · CSV available</td></tr>
    <tr><td>Authentication</td>  <td>None required — Open Access</td></tr>
    <tr><td>Temporal Coverage</td><td>2014-01-01 → 2025-12-31 (queried window)</td></tr>
    <tr><td>Magnitude Filter</td><td>Mw ≥ 2.0 (global); Mw ≥ 2.5 for some regions</td></tr>
    <tr><td>Key Query Params</td><td>starttime, endtime, minmagnitude, maxlatitude, minlatitude</td></tr>
    <tr><td>License</td>         <td>U.S. Public Domain — unrestricted use</td></tr>
  </table>
</div>
""", unsafe_allow_html=True)

# ── Source 2: GFZ ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="source-card" data-num="02">
  <span class="source-tag tag-gfz">Source 02 · Space Weather</span>
  <div class="source-name">🧲 GFZ Potsdam · Kp Index Series</div>
  <div class="source-url">https://www.gfz-potsdam.de/en/section/geomagnetism/data-products-services/geomagnetic-kp-index</div>
  <div class="source-desc">
    The Kp index (planetary K-index) is derived from measurements at a global network of
    geomagnetic observatories. Every 3 hours, each station computes a local K-index
    (0–9 scale) reflecting the maximum deviation of the geomagnetic field from a quiet-day
    baseline. The global Kp is a weighted average across 13 mid-latitude stations.
    It has been computed continuously since 1932 and is the standard reference for
    geomagnetic storm classification. The GFZ Potsdam is the World Data Centre responsible
    for its definitive publication.
  </div>
  <table class="meta-table">
    <tr><td>Theme</td>           <td>Geomagnetic Activity / Space Weather</td></tr>
    <tr><td>Provider</td>        <td>Helmholtz Centre Potsdam — GFZ German Research Centre</td></tr>
    <tr><td>Endpoint</td>        <td>ftp://ftp.gfz-potsdam.de/pub/home/obs/kp-ap/</td></tr>
    <tr><td>Access Method</td>   <td>FTP file download · also via GFZ web portal</td></tr>
    <tr><td>Data Format</td>     <td>Fixed-width text (.txt) · parsed to CSV</td></tr>
    <tr><td>Authentication</td>  <td>None required — Open Access</td></tr>
    <tr><td>Temporal Resolution</td><td>3-hourly (8 readings per day)</td></tr>
    <tr><td>Temporal Coverage</td><td>1932 → present · project uses 2014–2025</td></tr>
    <tr><td>License</td>         <td>CC BY 4.0 — attribution required</td></tr>
  </table>
</div>
""", unsafe_allow_html=True)

# ── License badges ────────────────────────────────────────────────────────────
st.markdown("""
<div class="license-row">
  <span class="license-badge lb-open">✓ USGS · U.S. Public Domain</span>
  <span class="license-badge lb-cc">✓ GFZ · CC BY 4.0 · Citation required</span>
  <span class="license-badge lb-warn">⚠ Plate boundary data · CC BY 4.0 (Bird 2003)</span>
  <span class="license-badge lb-open">✓ No personal data collected or processed</span>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — ORIGINAL DATASET SCHEMAS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">My Dataset Schemas</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Working <span class="ag">Variables</span> &amp; Types</div>', unsafe_allow_html=True)

tab_usgs, tab_gfz = st.tabs(["🌍  USGS Earthquakes", "🧲  GFZ Kp Index"])

# ── USGS schema ───────────────────────────────────────────────────────────────
with tab_usgs:
    st.markdown("""
    <div style="font-family:'Space Mono',monospace;font-size:0.68rem;color:#3a5a7a;
                padding:0.6rem 0 0.4rem 0;letter-spacing:0.06em;">
      RangeIndex: 335,035 entries &nbsp;·&nbsp; 27 columns &nbsp;·&nbsp; Memory usage: ~69 MB
    </div>
    """, unsafe_allow_html=True)

    usgs_cols = [
        ("#", "Column", "Dtype", "Notes"),
        ("01", "start_time",     "datetime64[ns, UTC]", "UTC timestamp of the event origin"),
        ("02", "mag",            "float64",             "Moment magnitude (Mw)"),
        ("03", "place",          "object",              "Human-readable location description"),
        ("04", "tsunami",        "int64",               "1 = tsunami warning/observation generated"),
        ("05", "mag_type",       "object",              "Magnitude scale used (mw, mb, ml …)"),
        ("06", "duration",       "float64",             "Shaking duration in seconds"),
        ("07", "longitude",      "float64",             "Epicentre longitude (°E/W)"),
        ("08", "latitude",       "float64",             "Epicentre latitude (°N/S)"),
        ("09", "depth_km",       "float64",             "Hypocentre depth below surface (km)"),
        ("10", "source",         "object",              "Reporting network code"),
        ("11", "updated_utc",    "datetime64[ns, UTC]", "Last catalogue update timestamp"),
        ("12", "state",          "object",              "U.S. state (where applicable)"),
        ("13", "eq_location",    "object",              "Parsed location string"),
        ("14", "sources_list",   "object",              "List of contributing networks"),
        ("15", "source_category","object",              "Network type classification"),
        ("16", "year",           "int64",               "Derived from start_time"),
        ("17", "month",          "int64",               "Derived from start_time"),
        ("18", "hour",           "int64",               "UTC hour (0–23)"),
        ("19", "country",        "object",              "Country from reverse geocoding"),
        ("20", "continent",      "object",              "Continent from geospatial join"),
        ("21", "week_of_year",   "int64",               "ISO week number"),
        ("22", "day_of_year",    "int64",               "1–365/366"),
        ("23", "local_solar_time","float64",            "LST = UTC + (lon/15), mod 24"),
        ("24", "lst_hour",       "int64",               "Floor of local_solar_time"),
        ("25", "mag_category",   "object",              "Binned: Minor / Light / Moderate / Strong / Major"),
        ("26", "depth_km_category","object",            "Shallow / Intermediate / Deep"),
        ("27", "tectonic_proxy_zone","object",          "From plate boundary proximity (Bird 2003)"),
    ]

    grid_cols = "40px 1fr 1fr 2fr"
    st.markdown(f"""
    <div class="schema-wrap">
      <div class="schema-header" style="grid-template-columns:{grid_cols};">
        <span>#</span><span>Column</span><span>Dtype</span><span>Notes</span>
      </div>
    """, unsafe_allow_html=True)
    for row in usgs_cols[1:]:
        st.markdown(f"""
      <div class="schema-row" style="grid-template-columns:{grid_cols};">
        <span class="col-num">{row[0]}</span>
        <span class="col-name">{row[1]}</span>
        <span class="col-dtype">{row[2]}</span>
        <span class="col-desc">{row[3]}</span>
      </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Sample head table
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="section-label" style="margin-top:0.5rem;">Sample · First 5 Rows</div>', unsafe_allow_html=True)
    sample_usgs = pd.DataFrame({
        "start_time":   ["2014-01-01 00:05:35 UTC", "2014-01-01 01:11:22 UTC",
                         "2014-01-01 02:08:44 UTC", "2014-01-01 03:14:07 UTC",
                         "2014-01-01 04:22:51 UTC"],
        "mag":          [2.5, 3.1, 4.8, 2.2, 5.3],
        "depth_km":     [12.4, 8.1, 35.0, 5.2, 22.7],
        "latitude":     [61.32, 35.71, -13.82, 38.45, -8.24],
        "longitude":    [-149.85, 140.72, -76.31, 22.14, 115.62],
        "mag_category": ["Minor (<4)", "Light (4–5)", "Light (4–5)", "Minor (<4)", "Moderate (5–6)"],
        "country":      ["USA", "Japan", "Peru", "Greece", "Indonesia"],
    })
    st.dataframe(
        sample_usgs,
        use_container_width=True,
        hide_index=True,
    )

# ── GFZ schema ────────────────────────────────────────────────────────────────
with tab_gfz:
    st.markdown("""
    <div style="font-family:'Space Mono',monospace;font-size:0.68rem;color:#3a5a7a;
                padding:0.6rem 0 0.4rem 0;letter-spacing:0.06em;">
      RangeIndex: 35,064 entries &nbsp;·&nbsp; 17 columns &nbsp;·&nbsp;
      3-hourly · 8 readings/day · ~4,383 days covered
    </div>
    """, unsafe_allow_html=True)

    gfz_cols = [
        ("#", "Column", "Dtype", "Notes"),
        ("01", "start_time",        "datetime64[ns, UTC]", "Interval start (3-hourly)"),
        ("02", "kp",                "float64",             "Kp index value (0.0 – 9.0)"),
        ("03", "year",              "int64",               "Derived from start_time"),
        ("04", "month",             "int64",               "Derived from start_time"),
        ("05", "hour",              "int64",               "UTC hour (0, 3, 6, 9 … 21)"),
        ("06", "kp_category",       "object",              "Quiet / Unsettled / Active / Storm / Severe / Extreme"),
        ("07", "day_of_year",       "int64",               "1–365/366"),
        ("08", "week",              "int64",               "ISO week number"),
        ("09", "years_since_start", "float64",             "Years elapsed from study start (2014-01-01)"),
        ("10", "solar_cycle_phase", "object",              "Rising / Maximum / Declining / Minimum"),
        ("11", "storm",             "bool",                "True if Kp ≥ 5"),
        ("12", "storm_group",       "object",              "Storm episode grouping ID"),
        ("13", "storm_duration",    "float64",             "Consecutive storm intervals (×3h)"),
        ("14", "kp_diff",           "float64",             "Change from previous interval"),
        ("15", "kp_abs_change",     "float64",             "Absolute change from previous interval"),
        ("16", "subsolar_lat",      "float64",             "Estimated subsolar latitude (°)"),
        ("17", "subsolar_lon",      "float64",             "Estimated subsolar longitude (°)"),
    ]

    grid_cols = "40px 1fr 1fr 2fr"
    st.markdown(f"""
    <div class="schema-wrap">
      <div class="schema-header" style="grid-template-columns:{grid_cols};">
        <span>#</span><span>Column</span><span>Dtype</span><span>Notes</span>
      </div>
    """, unsafe_allow_html=True)
    for row in gfz_cols[1:]:
        st.markdown(f"""
      <div class="schema-row" style="grid-template-columns:{grid_cols};">
        <span class="col-num">{row[0]}</span>
        <span class="col-name">{row[1]}</span>
        <span class="col-dtype">{row[2]}</span>
        <span class="col-desc">{row[3]}</span>
      </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="section-label" style="margin-top:0.5rem;">Sample · First 5 Rows</div>', unsafe_allow_html=True)
    sample_gfz = pd.DataFrame({
        "start_time":       ["2014-01-01 00:00:00 UTC", "2014-01-01 03:00:00 UTC",
                             "2014-01-01 06:00:00 UTC", "2014-01-01 09:00:00 UTC",
                             "2014-01-01 12:00:00 UTC"],
        "kp":               [1.0, 1.3, 2.0, 1.7, 0.7],
        "kp_category":      ["Quiet", "Quiet", "Quiet", "Quiet", "Quiet"],
        "storm":            [False, False, False, False, False],
        "solar_cycle_phase":["Rising", "Rising", "Rising", "Rising", "Rising"],
        "subsolar_lat":     [-23.0, -23.0, -22.9, -22.9, -22.9],
        "subsolar_lon":     [-172.5, -127.5, -82.5, -37.5, 7.5],
    })
    st.dataframe(sample_gfz, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — DATA QUALITY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Data Quality</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Quality Checks &amp; <span class="ab">Cleaning Decisions</span></div>', unsafe_allow_html=True)

dq_col1, dq_col2 = st.columns(2, gap="large")

with dq_col1:
    st.markdown('<div style="font-family:\'Space Mono\',monospace;font-size:0.65rem;color:#00c494;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.6rem;">🌍 USGS Earthquakes</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="dq-grid">
      <div class="dq-pill"><div class="dq-val" style="color:#5b8aff;">335,035</div><div class="dq-lbl">Raw Events Fetched</div></div>
      <div class="dq-pill"><div class="dq-val" style="color:#00c494;">~0.3%</div><div class="dq-lbl">Duplicate IDs Removed</div></div>
      <div class="dq-pill"><div class="dq-val" style="color:#f4c542;">~4.1%</div><div class="dq-lbl">Duration Nulls</div></div>
      <div class="dq-pill"><div class="dq-val" style="color:#e04313;">~0.8%</div><div class="dq-lbl">Depth Nulls → Imputed</div></div>
    </div>
    """, unsafe_allow_html=True)
    cleaning_notes_usgs = [
        ("Duplicate IDs", "Removed exact duplicates on `id_eq` keeping the most recently updated record."),
        ("Mixed mag types", "Retained all magnitude types; `mag_type` column retained for filtering. No cross-scale conversion applied — noted as limitation."),
        ("Null depth", "~0.8% of events had no depth. Imputed with the median depth for that tectonic zone. Flagged in `depth_imputed` column."),
        ("Null duration", "~4.1% missing. Not imputed — excluded from duration-specific analyses. `is_prolonged_shaking` set to NaN for these rows."),
        ("Timezone", "All timestamps confirmed UTC; no conversion applied. `updated_utc` used for recency checks only."),
    ]
    for issue, fix in cleaning_notes_usgs:
        st.markdown(f"""
        <div style="margin-bottom:0.55rem;padding:0.65rem 0.9rem;background:#0b162855;
                    border:1px solid #1e3a5f33;border-radius:7px;font-size:0.83rem;">
          <span style="font-family:'Space Mono',monospace;color:#5b8aff;font-size:0.68rem;">{issue}</span>
          <br><span style="color:#4a6a8a;line-height:1.6;">{fix}</span>
        </div>
        """, unsafe_allow_html=True)

with dq_col2:
    st.markdown('<div style="font-family:\'Space Mono\',monospace;font-size:0.65rem;color:#00c494;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.6rem;">🧲 GFZ Kp Index</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="dq-grid">
      <div class="dq-pill"><div class="dq-val" style="color:#5b8aff;">35,064</div><div class="dq-lbl">Raw Intervals</div></div>
      <div class="dq-pill"><div class="dq-val" style="color:#00c494;">0</div><div class="dq-lbl">Duplicates Found</div></div>
      <div class="dq-pill"><div class="dq-val" style="color:#f4c542;">0.0%</div><div class="dq-lbl">Null Kp Values</div></div>
      <div class="dq-pill"><div class="dq-val" style="color:#e04313;">12</div><div class="dq-lbl">Provisional Intervals</div></div>
    </div>
    """, unsafe_allow_html=True)
    cleaning_notes_gfz = [
        ("Completeness", "The GFZ series has no gaps in the 2014–2025 window. All 35,064 expected 3-hourly intervals are present."),
        ("Provisional data", "The final ~30 days of the series may use provisional (not definitive) Kp values. Flagged but retained."),
        ("Kp scale", "Kp is a quasi-logarithmic integer-third scale (0, 0.33, 0.67, 1.0 …). Stored as float64 for continuity."),
        ("Storm grouping", "Consecutive Kp ≥ 5 intervals grouped into episodes using `storm_group` ID. Gap of ≥ 2 quiet intervals used to separate episodes."),
        ("Timezone", "All timestamps are UTC interval start times. No timezone conversion needed."),
    ]
    for issue, fix in cleaning_notes_gfz:
        st.markdown(f"""
        <div style="margin-bottom:0.55rem;padding:0.65rem 0.9rem;background:#0b162855;
                    border:1px solid #1e3a5f33;border-radius:7px;font-size:0.83rem;">
          <span style="font-family:'Space Mono',monospace;color:#00c494;font-size:0.68rem;">{issue}</span>
          <br><span style="color:#4a6a8a;line-height:1.6;">{fix}</span>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — MERGE / JOIN LOGIC
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Dataset Integration</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Merge &amp; <span class="ag">Join Logic</span></div>', unsafe_allow_html=True)

st.markdown("""
<div class="merge-box">
  <div style="font-family:'Satisfy',sans-serif;font-weight:700;color:#e8eaf0;margin-bottom:0.7rem;">
    How are the two datasets linked?
  </div>
  <div class="merge-note">
    The USGS earthquake events (event-level, ~335K rows) and GFZ Kp intervals
    (3-hourly, ~35K rows) operate at different temporal resolutions.
    They are joined by <strong>flooring each earthquake's UTC timestamp
    to the nearest 3-hour Kp interval</strong>:
  </div>
  <div class="merge-formula">eq["kp_interval"] = eq["start_time"].dt.floor("3h")</div>
  <div class="merge-formula">merged = eq.merge(kp, left_on="kp_interval", right_on="start_time", how="left")</div>
  <div class="merge-note" style="margin-top:0.8rem;">
    This is a <strong>left join</strong> — every earthquake is retained.
    Kp columns (<em>kp, kp_category, storm, solar_cycle_phase, subsolar_lat/lon</em>)
    are appended to each earthquake row, reflecting the geomagnetic conditions
    at the time of occurrence. Earthquakes with no matching Kp interval
    (e.g. outside the 2014–2025 GFZ window) receive NaN for all Kp fields.
    <br><br>
    <strong>Important caveat:</strong> this assigns the <em>concurrent</em> Kp value,
    not a lagged precursor. Lag analyses (e.g. Kp in the 24–72h window before each quake)
    are computed separately by joining on shifted timestamp windows.
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7 — LIMITATIONS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Known Limitations</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Data <span style="color:#e04313;">Limitations</span> &amp; Caveats</div>', unsafe_allow_html=True)

limitations = [
    ("⚠️", "Magnitude Heterogeneity",
     "The USGS catalogue contains earthquakes reported under different magnitude scales (Mw, mb, ml, md…). No cross-scale conversion was applied. Analyses comparing magnitudes across regions or time periods should account for this inconsistency."),
    ("⚠️", "Detection Threshold Varies by Region",
     "The minimum detectable magnitude is not uniform globally. Dense seismic networks (e.g. Japan, California) detect events down to Mw ~1.5; sparse networks in oceanic or remote areas may miss events below Mw 4–5. This introduces a spatial detection bias."),
    ("⚠️", "Kp is a Global Average, Not Local",
     "The Kp index reflects geomagnetic disturbance averaged across 13 mid-latitude stations. It does not capture localised ionospheric effects at specific earthquake epicentres. A storm that strongly affects high latitudes may register a moderate Kp while having a larger effect locally."),
    ("⚠️", "Temporal Resolution Mismatch",
     "Earthquakes are timestamped to the second; Kp is measured every 3 hours. The floor-to-3h merge assigns each quake to a single Kp interval, ignoring within-interval variability. Some fast-rising storms may not be reflected in the assigned Kp value."),
    ("⚠️", "Observational Study — No Causality",
     "All findings are correlational. No randomisation, natural experiment, or instrumental variable is available to establish causation. Confounders (e.g. solar cycle phase, seasonal patterns, regional seismicity rates) must be controlled analytically, not experimentally."),
    ("⚠️", "Temporal Window 2014–2025 Only",
     "The study covers approximately one full solar cycle (Cycle 24 decline + Cycle 25 rising). This is insufficient to draw conclusions that generalise across all solar cycle phases or multi-decadal patterns. Results may not replicate in earlier or later cycles."),
    ("⚠️", "Provisional GFZ Data for Recent Months",
     "Kp values for the final ~30 days of the dataset may be preliminary (not yet quality-controlled definitively). This affects a small fraction of observations but is noted for reproducibility."),
    ("⚠️", "Duration Field Sparse",
     "Earthquake shaking duration is available for only ~96% of events and its derivation varies by reporting network. Duration-based analyses have reduced statistical power and should be interpreted cautiously."),
]

lim_col1, lim_col2 = st.columns(2, gap="large")
for i, (icon, title, text) in enumerate(limitations):
    col = lim_col1 if i % 2 == 0 else lim_col2
    with col:
        st.markdown(f"""
        <div class="limit-item">
          <span class="limit-icon">{icon}</span>
          <div class="limit-text"><strong>{title}</strong><br>{text}</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER NAV
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
fc1, _, fc3 = st.columns([1, 2, 1])
with fc1:
    if st.button("← ETL & Sources"):
        st.switch_page("pages/page_4.py")
with fc3:
    if st.button("↖ Back to Home"):
        st.switch_page("homepage.py")

st.markdown("""
<div class="footer">
  STORM &amp; QUAKE · ETL PROCESS &amp; DATA SOURCES<br>
  DATA: USGS COMCAT (PUBLIC DOMAIN) · GFZ POTSDAM Kp (CC BY 4.0)<br>
  PLATE BOUNDARIES: BIRD 2003 (CC BY 4.0)
</div>
""", unsafe_allow_html=True)