import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# -------------------------
# Load Data
# -------------------------
@st.cache_data
def load_data():
    usgs_eq_df = pd.read_csv("/Users/paus/Projects/da_capstone/data/processed/usgs_eq_df.csv", parse_dates=["start_time"])
    gfz_kp_df = pd.read_csv("/Users/paus/Projects/da_capstone/data/processed/gfz_kp_df.csv", parse_dates=["start_time"])
    return usgs_eq_df, gfz_kp_df

usgs_eq_df, gfz_kp_df = load_data()


# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Storm & Quake · Geomagnetic–Seismic EDA",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    background-color: #04060f;
    color: #e8eaf0;
    font-family: 'Inter', sans-serif;
}
.main { padding-top: 0 !important; }
.block-container { padding: 0 2rem 4rem 2rem !important; max-width: 1200px; }

/* ── Aurora hero ── */
.aurora-bg {
    position: relative;
    width: 100%;
    overflow: hidden;
    padding: 4.5rem 2rem 3.5rem 2rem;
    margin-bottom: 2.5rem;
    background:
        radial-gradient(ellipse 80% 60% at 20% -10%, #0d3b2e55 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 0%,  #1a1a4e66 0%, transparent 55%),
        radial-gradient(ellipse 100% 80% at 50% -30%, #0a2a3f44 0%, transparent 70%),
        linear-gradient(180deg, #04060f 0%, #060d1a 100%);
    border-bottom: 1px solid #1e3a5f33;
}
.aurora-bg::before {
    content: '';
    position: absolute; inset: 0;
    background:
        radial-gradient(ellipse 40% 30% at 15% 40%, #00c49422 0%, transparent 60%),
        radial-gradient(ellipse 50% 25% at 72% 30%, #5b5bff18 0%, transparent 55%),
        radial-gradient(ellipse 30% 20% at 45% 75%, #00b4d820 0%, transparent 50%);
    animation: aurora-pulse 12s ease-in-out infinite alternate;
    pointer-events: none;
}
@keyframes aurora-pulse {
    0%   { opacity: 0.6; transform: translateY(0px) scale(1); }
    100% { opacity: 1.0; transform: translateY(-8px) scale(1.03); }
}
.aurora-bg::after {
    content: '';
    position: absolute; inset: 0;
    background-image:
        radial-gradient(1px 1px at 10% 20%, #ffffff22 0%, transparent 100%),
        radial-gradient(1px 1px at 30% 60%, #ffffff18 0%, transparent 100%),
        radial-gradient(1px 1px at 55% 15%, #ffffff1a 0%, transparent 100%),
        radial-gradient(1px 1px at 75% 50%, #ffffff14 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 80%, #ffffff20 0%, transparent 100%),
        radial-gradient(1px 1px at 20% 85%, #ffffff16 0%, transparent 100%),
        radial-gradient(1px 1px at 65% 75%, #ffffff12 0%, transparent 100%);
    pointer-events: none;
}

/* ── Typography ── */
.hero-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #00c494;
    margin-bottom: 1.1rem;
    position: relative;
}
.hero-title {
    font-family: 'Archivo Black', sans-serif;
    font-size: clamp(2.6rem, 5.5vw, 4.2rem);
    font-weight: 800;
    line-height: 1.08;
    color: #f0f4ff;
    margin: 0 0 0.6rem 0;
    position: relative;
}
.hero-title .accent-storm { color: #00c494; }
.hero-title .accent-quake { color: #5b8aff; }
.hero-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: clamp(0.95rem, 1.8vw, 1.15rem);
    font-weight: 300;
    color: #7a9cc0;
    margin-bottom: 0.3rem;
    max-width: 640px;
    line-height: 1.65;
    position: relative;
}
.hero-meta {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #3a5a7a;
    letter-spacing: 0.12em;
    margin-top: 1.4rem;
    position: relative;
}
.hero-meta span { color: #00c49477; margin: 0 0.4rem; }

/* ── Section labels ── */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #00c494;
    margin-bottom: 0.35rem;
    margin-top: 1.2rem;
}
.section-title {
    font-family: 'Archivo Black', sans-serif;
    font-size: 1.55rem;
    font-weight: 700;
    color: #e8eaf0;
    margin-bottom: 1.3rem;
    line-height: 1.2;
}

/* ── Cards ── */
.card {
    background: linear-gradient(135deg, #0b1628cc 0%, #0d1f3acc 100%);
    border: 1px solid #1e3a5f55;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 0.9rem;
    transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
}
.card:hover {
    border-color: #00c49444;
    transform: translateY(-2px);
    box-shadow: 0 8px 32px #00000033;
}

/* ── Hypothesis box ── */
.hypothesis-box {
    background: linear-gradient(135deg, #051a0f 0%, #081428 100%);
    border: 1px solid #00c49433;
    border-left: 4px solid #00c494;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 0.9rem;
    position: relative;
    overflow: hidden;
}
.hypothesis-box::before {
    content: 'H₀';
    position: absolute;
    right: 1.2rem; top: 0.8rem;
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    color: #00c49410;
    line-height: 1;
}
.hypothesis-text {
    font-family: 'Satisfy', sans-serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: #c8f0e0;
    line-height: 1.55;
}
.hypothesis-note {        
    font-size: 0.8rem;
    color: #56c48c;
    margin-top: 0.6rem;
    font-style: italic;
}

/* ── Nav buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0b1628 0%, #0f2040 100%) !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 10px !important;
    color: #7a9cc0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.8rem 1.2rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    line-height: 1.4 !important;
    text-align: left !important;
}
.stButton > button:hover {
    border-color: #00c49466 !important;
    color: #00c494 !important;
    background: linear-gradient(135deg, #051a10 0%, #08142a 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px #00c49415 !important;
}

/* ── Stat grid ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.8rem;
    margin-bottom: 1rem;
}
.stat-card {
    background: linear-gradient(135deg, #0b1628 0%, #0f2040 100%);
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 1.1rem 0.9rem;
    text-align: center;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.stat-card:hover {
    border-color: #00c49455;
    box-shadow: 0 0 20px #00c49412;
}
.stat-value {
    font-family: 'Satisfy', sans-serif;
    font-size: 1.75rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.25rem;
}
.stat-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #4a6a8a;
    line-height: 1.3;
}
.stat-sub {
    font-size: 0.7rem;
    color: #2a4a6a;
    margin-top: 0.15rem;
}

/* ── Dataset bar ── */
.dataset-bar {
    background: linear-gradient(90deg, #0b1628 0%, #0f2040 100%);
    border-left: 3px solid;
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.3rem;
    margin-bottom: 0.7rem;
}
.dataset-name {
    font-family: 'Permanent Marker', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    color: #e8eaf0;
    margin-bottom: 0.15rem;
}
.dataset-meta {
    font-family: 'Space Mono', monospace;
    font-size: 0.63rem;
    color: #3a5a7a;
    letter-spacing: 0.05em;
}

/* ── Pills ── */
.pill {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    padding: 0.18rem 0.6rem;
    border-radius: 20px;
    margin: 0.15rem 0.1rem;
}
.pill-green { background:#00c49412; border:1px solid #00c49433; color:#00c494; }
.pill-blue  { background:#5b8aff12; border:1px solid #5b8aff33; color:#5b8aff; }

/* ── Objective items ── */
.obj-item {
    display: flex;
    gap: 0.8rem;
    align-items: flex-start;
    margin-bottom: 0.8rem;
    padding: 0.9rem 1rem;
    background: #0b162855;
    border: 1px solid #1e3a5f33;
    border-radius: 8px;
    transition: border-color 0.2s;
}
.obj-item:hover { border-color: #1e3a5f99; }
.obj-num {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    color: #00c494;
    background: #00c49415;
    border: 1px solid #00c49433;
    border-radius: 4px;
    padding: 0.15rem 0.45rem;
    margin-top: 0.1rem;
    flex-shrink: 0;
}
.obj-text { font-size: 0.87rem; color: #7a9cc0; line-height: 1.55; }

/* ── Motivation item ── */
.motiv-item {
    display: flex;
    gap: 0.9rem;
    align-items: flex-start;
    margin-bottom: 0.8rem;
    padding: 0.85rem 1rem;
    background: #0b1628aa;
    border: 1px solid #1e3a5f33;
    border-radius: 8px;
}
.motiv-icon { font-size: 1.2rem; flex-shrink: 0; margin-top: 0.05rem; }
.motiv-text { font-size: 0.87rem; color: #7a9cc0; line-height: 1.6; }

/* ── Divider ── */
.aurora-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e3a5f, #00c49433, #1e3a5f, transparent);
    margin: 2.8rem 0;
}

/* ── Arrow connector ── */
.arrow-connector {
    text-align: center;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #00c494;
    letter-spacing: 0.05em;
    padding: 1rem 0;
}

/* ── Footer ── */
.footer {
    text-align: center;
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    color: #1a2a3a;
    letter-spacing: 0.12em;
    padding: 2rem 0 0 0;
    border-top: 1px solid #0e1e2e;
    margin-top: 3rem;
    line-height: 2;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="aurora-bg">
  <div class="hero-eyebrow">🌌 Paula's Exploratory Data Analysis &nbsp;·&nbsp; 2014 – 2025</div>
  <div class="hero-title">
    Do <span class="accent-storm">Geomagnetic Storms</span><br>
    Correlate with <span class="accent-quake">Earthquakes</span>?
  </div>
  <div class="hero-subtitle">
    The idea that solar activity may influence earthquakes has intrigued scientists for decades. 
    This interactive analysis combines 11 years of USGS earthquake records with geomagnetic Kp-index data, 
    highlighting how openly accessible, near–real-time global datasets enable anyone to explore Earth’s dynamics 
    through time-series and geospatial analysis.
  </div>
  <div class="hero-meta">
    ✦ Author: Paula Herrera
    <span>·</span>
    My Data Analytics Project
    <span>·</span>
    April 2026
    <span>·</span>
    Data: GFZ Potsdam &amp; USGS (2014-2025)
  </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">Explore the project!</div>', unsafe_allow_html=True)

nav1, nav2, nav3, nav4, nav5 = st.columns(5, gap="medium")

with nav1:
    if st.button("📖  Concepts\n& Variables", key="nav_concepts"):
        st.switch_page("pages/page_1.py")
with nav2:
    if st.button("🌍  Earthquake Patterns", key="nav_eq"):
        st.switch_page("pages/page_2.py")
with nav3:
    if st.button("🌐  Solar Activity", key="nav_kpi"):
        st.switch_page("pages/page_3.py")
with nav4:
    if st.button("🔑  Key Takeaways", key="nav_keys"):
        st.switch_page("pages/page_4.py")
with nav5:
    if st.button("🔧  ETL Process\n& Data Sources", key="nav_etl"):
        st.switch_page("pages/page_5.py")

st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# BACKGROUND + MOTIVATION
# ═══════════════════════════════════════════════════════════════════════════════
col_bg, col_motiv = st.columns([3, 2], gap="medium")

with col_bg:
    st.markdown('<div class="section-label">Research Background</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">About This Project</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <p style="color:#8aaccc; line-height:1.75; font-size:0.93rem; margin:0 0 0.9rem 0;">
        For decades, the scientific community has debated whether <strong style="color:#e8eaf0;">space weather
        events</strong>, driven by solar activity, such as geomagnetic storms, might
        influence terrestrial seismicity via <em>Lithosphere-Atmosphere-Ionosphere Coupling (LAIC)</em>.
      </p>
      <p style="color:#8aaccc; line-height:1.75; font-size:0.93rem; margin:0 0 0.9rem 0;">
        This project adopts an intersectional analytical framework to examine
        <strong style="color:#e8eaf0;">overlapping relationships between categories of earthquake characteristics</strong> across
        all geomagnetic disturbance levels (Kp 0–9) and the full global earthquake
        record from 2014 to 2025 as collected and shared by the US Geological Survey.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Research Question</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Correlation or Trigger?</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hypothesis-box">
    <div class="hypothesis-text">
        <b>
        Are geomagnetic disturbances linked to variations in earthquake frequency, magnitude, duration, or depth over time and across regions?</b><br>
    </div>
    <hr style="border: 0; border-top: 1px solid #1e3a5f33; margin:0 0 0.9rem 0;">
    <div class="hypothesis-note">
        <b>Null Hypothesis (H₀):</b> Seismic activity is independent of geomagnetic flux; solely a result of lithospheric processes.<br><br>
        <b>Working Hypotheses:</b>
        <ul style="margin-top: 0.5rem; padding-left: 1.0rem;">
        <li><b>Solar-Time:</b> If solar-driven electromagnetic processes influence seismicity, earthquake patterns should align with <b>Local Solar Time (LST)</b> rather than coordinated universal time (UTC).</li>
        <li><b>Conditional Triggering:</b> Events in the Magnetosphere may only manifest at intersections of high Kp-index events at specific daylight hours (direct solar exposure) and seismic zones.</li>
        </ul>
    </div>
    </div>
    """, unsafe_allow_html=True)


with col_motiv:
    st.markdown('<div class="section-label">Research Motivation</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Why This Matters</div>', unsafe_allow_html=True)

    motivations = [
        ("🛰️", "<b>Cross-Domain Synergy:</b> We have entered a golden age of heliophysics monitoring. This project investigates the untapped potential of space-weather data to provide a more holistic understanding of terrestrial risk and atmospheric coupling."),
        ("🌋", "<b>Personal Roots:</b> As a Mexico City Chilanga, I am well aware of the public need for a better understanding of sesimic activity. Earthquake prediction remains one of the hardest problems in geoscience. Any reproducible precursor signal is worth it!"),
        ("📡", "<b>Open-Science Power:</b> Isn't it incredible that we can now access global, open, high-resolution data from advanced scientific insitutes, such as GFZ and USGS? Why not leverage those skills for my EDA portafolio with a near-to-real-time large-scale cross-domain analysis, right?"),
        ("📐", "<b>Skill Showcasing:</b> This is an observational study. Correlation findings do not imply causation. A goal is to showcase my pattern discovery and hypothesis generation skills while using timestamps and geolocation variables from complex systems."),
    ]
    for icon, text in motivations:
        st.markdown(f"""
        <div class="motiv-item">
          <span class="motiv-icon">{icon}</span>
          <span class="motiv-text">{text}</span>
        </div>
        """, unsafe_allow_html=True)


st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# OBJECTIVES
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">Objectives</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Analyzing Planetary Activity</div>', unsafe_allow_html=True)

oc1, oc2 = st.columns(2, gap="medium")

objs_left = [
    ("01", "Profile global seismicity: magnitude, depth, location, tectonic setting, time-of-day, and duration patterns."),
    ("02", "Profile geomagnetic activity: Kp distribution, storm frequency, solar cycle phase, and temporal clustering."),]
objs_right = [
    ("03", "Investigate time-lag effects: do seismic responses (if any) appear during or after peak geomagnetic disturbance?"),
    ("04", "Explore regional variation: are correlations stronger near subduction zones, mid-ocean ridges, or continental faults?"),
]

with oc1:
    for num, text in objs_left:
        st.markdown(f"""
        <div class="obj-item">
          <span class="obj-num">{num}</span>
          <span class="obj-text">{text}</span>
        </div>
        """, unsafe_allow_html=True)

with oc2:
    for num, text in objs_right:
        st.markdown(f"""
        <div class="obj-item">
          <span class="obj-num">{num}</span>
          <span class="obj-text">{text}</span>
        </div>
        """, unsafe_allow_html=True)


st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# DATA OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">Data Overview</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Two Datasets, One Question</div>', unsafe_allow_html=True)

ds1, ds2 = st.columns(2, gap="medium")

with ds1:
    st.markdown("""
    <div class="dataset-bar" style="border-left-color:#00c494;">
      <div class="dataset-name">🧲 GFZ Potsdam · Kp Index</div>
      <div class="dataset-meta">Geomagnetic Activity &nbsp;·&nbsp; 3-hourly resolution &nbsp;·&nbsp; Global coverage</div>
    </div>
    """, unsafe_allow_html=True)

    kp_stats = [
        (f"{len(gfz_kp_df):,}",           "#00c494", "Total Records",  "3-hr intervals"),
        ("2014–2025", "#00c494", "Date Range",     "study window"),
        (f"{gfz_kp_df['kp'].median():.1f}",         "#00c494", "Median Kp",        "scale 0 – 9"),
        (f"{((gfz_kp_df["kp"] >= 5) & (gfz_kp_df["kp"].shift(fill_value=0) < 7)).sum():,}",           "#00c494", "Storm Events",   "Kp ≥ 5"),
        (f"{((gfz_kp_df["kp"] >= 7) & (gfz_kp_df["kp"].shift(fill_value=0) < 7)).sum():,}",           "#00c494", "Major Storms",   "Kp ≥ 7"),
        ("2",           "#00c494", "Solar Cycles",   "represented"),
    ]
    st.markdown('<div class="stat-grid">', unsafe_allow_html=True)
    for val, color, label, sub in kp_stats:
        st.markdown(f"""
        <div class="stat-card">
          <div class="stat-value" style="color:{color};">{val}</div>
          <div class="stat-label">{label}</div>
          <div class="stat-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:0.6rem;">
      <span class="pill pill-green">kp_intensity_value</span>
      <span class="pill pill-green">kp_category</span>
      <span class="pill pill-green">is_storm</span>
      <span class="pill pill-green">solar_cycle_phase</span>
      <span class="pill pill-green">subsolar_lat / lon</span>
    </div>
    """, unsafe_allow_html=True)

with ds2:
    st.markdown("""
    <div class="dataset-bar" style="border-left-color:#5b8aff;">
      <div class="dataset-name">🌍 USGS · Earthquake Catalogue</div>
      <div class="dataset-meta"> Seismic Activity &nbsp;·&nbsp; Event-level records &nbsp;· Global Coverage &nbsp;</div>
    </div>
    """, unsafe_allow_html=True)

    eq_stats = [
        (f"{len(usgs_eq_df):,}",           "#5b8aff", "Total Events",  "single earthquakes"),
        ("2014–2025", "#5b8aff", "Date Range",    "matched window"),
        (f"{usgs_eq_df['mag'].median():.1f}",         "#5b8aff", "Median Mag.",   "scale 2.5 – 8.8"),
        (f"{(usgs_eq_df["mag"] >= 6).sum():,}"  ,         "#5b8aff", "Major Events", "Mw ≥ 6"),
        (f"{usgs_eq_df['tsunami'].sum():,}",           "#5b8aff", "With Tsunami",  "flagged events"),
        (f"{usgs_eq_df['country'].nunique()}",           "#5b8aff", "Countries",     "represented"),
    ]
    st.markdown('<div class="stat-grid">', unsafe_allow_html=True)
    for val, color, label, sub in eq_stats:
        st.markdown(f"""
        <div class="stat-card" style="border-color:#1e2e5f;">
          <div class="stat-value" style="color:{color};">{val}</div>
          <div class="stat-label">{label}</div>
          <div class="stat-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:0.6rem;">
      <span class="pill pill-blue">mag_category</span>
      <span class="pill pill-blue">depth_km_category</span>
      <span class="pill pill-blue">is_15_sec_or_more</span>
      <span class="pill pill-blue">is_on_tectonic_plate</span>
      <span class="pill pill-blue">local_solar_time</span>
      <span class="pill pill-blue">dist_to_boundary_km</span>
      <span class="pill pill-blue">lat/ lon</span>
      <span class="pill pill-blue">latitude_band</span>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
  STORM &amp; QUAKE · GEOMAGNETIC–SEISMIC EDA · 2014 – 2025<br>
  DATA: GFZ POTSDAM (Kp INDEX) &amp; USGS (EARTHQUAKE CATALOGUE) · BUILT WITH STREAMLIT<br>
  [ Paula Herrera · EDA Capstone Project · 2026 ]
</div>
""", unsafe_allow_html=True)