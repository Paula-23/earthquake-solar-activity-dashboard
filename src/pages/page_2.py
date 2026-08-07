import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Earthquake Patterns",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Shared colour palette (consistent with homepage) ──────────────────────────
PALETTE_GREEN  = "#00c494"
PALETTE_BLUE   = "#5b8aff"
PALETTE_BG     = "#04060f"
PALETTE_CARD   = "#0b1628"
PALETTE_BORDER = "#1e3a5f"

# Category palettes for charts
CAT_PALETTES = {
    "depth_km_category":      ["#5b8aff", "#00c494", "#f4c542", "#e04313"],
    "mag_category":           ["#00c494", "#f4c542", "#df883d", "#e04313"],
    "tectonic_proxy_zone":    ["#5b8aff", "#00c494", "#a78bfa", "#f4c542", "#e04313", "#df883d"],
    "is_prolonged_shaking":   ["#00c494", "#e04313"],
    "latitude_zone":          ["#5b8aff", "#00c494", "#f4c542", "#df883d", "#e04313"],
   # "mag_category":           ["#1daa7b", "#B39416", "#df883d", "#e04313"],
    "duration_category":      ["#5b8aff", "#00c494", "#f4c542"],
}

# ── CSS (mirrors homepage dark/cosmic theme) ───────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700&family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    background-color: #04060f;
    color: #e8eaf0;
    font-family: 'Inter', sans-serif;
}
.main { background-color: #04060f; }
.block-container { padding: 1.5rem 2rem 4rem 2rem !important; max-width: 1400px; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060d1a 0%, #04060f 100%);
    border-right: 1px solid #1e3a5f44;
}
section[data-testid="stSidebar"] * { color: #e8eaf0 !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stSlider label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #00c494 !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #0b1628 !important;
    border-color: #1e3a5f !important;
    border-radius: 8px !important;
}

/* Page header */
.page-header {
    background:
        radial-gradient(ellipse 70% 80% at 0% 50%, #0d3b2e33 0%, transparent 60%),
        radial-gradient(ellipse 50% 60% at 100% 0%, #1a1a4e44 0%, transparent 55%),
        linear-gradient(135deg, #060d1a 0%, #04060f 100%);
    border: 1px solid #1e3a5f44;
    border-radius: 14px;
    padding: 2rem 2.5rem 1.8rem 2.5rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.page-header::before {
    content: '';
    position: absolute; inset: 0;
    background:
        radial-gradient(ellipse 30% 40% at 80% 60%, #5b8aff0a 0%, transparent 60%),
        radial-gradient(ellipse 20% 30% at 10% 30%, #00c4940a 0%, transparent 55%);
    pointer-events: none;
}
.page-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #5b8aff;
    margin-bottom: 0.6rem;
}
.page-title {
    font-family: 'Satisfy', sans-serif;
    font-size: 2.1rem;
    font-weight: 800;
    color: #f0f4ff;
    margin: 0 0 0.4rem 0;
    line-height: 1.1;
}
.page-title .accent { color: #5b8aff; }
.page-desc {
    font-size: 0.9rem;
    color: #5a7a9a;
    line-height: 1.65;
    max-width: 700px;
}

/* Section labels */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #00c494;
    margin-bottom: 0.3rem;
}
.section-title {
    font-family: 'Satisfy', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #e8eaf0;
    margin-bottom: 1rem;
}

/* Narrative card */
.narrative-card {
    background: linear-gradient(135deg, #060f1e 0%, #081428 100%);
    border: 1px solid #1e3a5f66;
    border-left: 4px solid #5b8aff;
    border-radius: 10px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
}
.narrative-card::before {
    position: absolute;
    right: 1.5rem; top: 1rem;
    font-size: 2rem;
    opacity: 0.12;
}
.narrative-text {
    font-family: 'Inter', sans-serif;
    font-size: 0.92rem;
    color: #8aaccc;
    line-height: 1.8;
}
.narrative-text strong { color: #5b8aff; }
.narrative-text em     { color: #00c494; font-style: normal; }

/* Stat pills row */
.stat-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.7rem;
    margin-bottom: 1.4rem;
}
.stat-pill {
    background: linear-gradient(135deg, #0b1628 0%, #0f2040 100%);
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    text-align: center;
    min-width: 120px;
    flex: 1;
}
.stat-pill-value {
    font-family: 'Satisfy', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: #5b8aff;
    line-height: 1;
    margin-bottom: 0.2rem;
}
.stat-pill-value.green { color: #00c494; }
.stat-pill-value.amber { color: #f4c542; }
.stat-pill-value.red   { color: #e04313; }
.stat-pill-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.56rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #3a5a7a;
}

/* Divider */
.aurora-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e3a5f, #00c49433, #1e3a5f, transparent);
    margin: 2rem 0;
}

/* Sidebar header */
.sidebar-header {
    font-family: 'Satisfy', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #e8eaf0;
    margin-bottom: 0.2rem;
}
.sidebar-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #3a5a7a;
    letter-spacing: 0.1em;
    margin-bottom: 1.2rem;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DATA  –  replace this block with your actual load logic
# ══════════════════════════════════════════════════════════════════════════════
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    usgs_eq_df = pd.read_csv("/Users/paus/Projects/da_capstone/data/processed/usgs_eq_df1.csv", parse_dates=["start_time"])
    gfz_kp_df = pd.read_csv("/Users/paus/Projects/da_capstone/data/processed/gfz_kp_df1.csv", parse_dates=["start_time"])
    return usgs_eq_df, gfz_kp_df

df_full, gfz_kp_df = load_data()

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR  –  Global filters (apply to BOTH charts)
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sidebar-header">🌍 Earthquake Filters</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">APPLIED TO ALL CHARTS ON THIS PAGE</div>', unsafe_allow_html=True)

    # Year range
    all_years = sorted(df_full['year'].unique())
    year_range = st.select_slider(
        "YEAR RANGE",
        options=all_years,
        value=(min(all_years), max(all_years)),
    )

    st.markdown("---")

    # Country filter
    all_countries = ["All Countries"] + sorted(df_full['country'].dropna().unique())
    selected_country = st.selectbox("COUNTRY / REGION", options=all_countries)

    # Latitude zone
    all_lat_zones = ["All Zones"] + sorted(df_full['latitude_zone'].dropna().unique())
    selected_lat_zone = st.selectbox("LATITUDE ZONE", options=all_lat_zones)

    st.markdown("---")
    st.markdown('<div class="section-label" style="margin-bottom:0.6rem;">Chart 1 · Time Series</div>', unsafe_allow_html=True)

    # Group / hue for time series chart
    ts_category = st.selectbox(
        "COLOUR SERIES BY",
        options=[
            "depth_km_category",
            "mag_category",
            "tectonic_proxy_zone",
            "is_prolonged_shaking",
            "latitude_zone",
        ],
        format_func=lambda x: {
            "depth_km_category":    "Depth Category",
            "mag_category":         "Magnitude Category",
            "tectonic_proxy_zone":  "Tectonic Zone",
            "is_prolonged_shaking": "Shaking Duration",
            "latitude_zone":        "Latitude Zone",
        }[x],
    )

    st.markdown('<div class="section-label" style="margin:0.8rem 0 0.6rem 0;">Chart 2 · LST Distribution</div>', unsafe_allow_html=True)

    # Depth filter for LST chart
    all_depths = sorted(df_full['depth_km_category'].dropna().unique())
    selected_depth = st.selectbox("DEPTH CATEGORY (LST)", options=["All"] + all_depths)

    # Colour-by for LST chart
    lst_color_by = st.selectbox(
        "COLOUR SERIES BY (LST)",
        options=["mag_category", "duration_category", "tectonic_proxy_zone"],
        format_func=lambda x: x.replace("_", " ").title(),
    )


# ══════════════════════════════════════════════════════════════════════════════
# FILTER APPLICATION
# ══════════════════════════════════════════════════════════════════════════════
df = df_full.copy()
df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
if selected_country != "All Countries":
    df = df[df['country'] == selected_country]
if selected_lat_zone != "All Zones":
    df = df[df['latitude_zone'] == selected_lat_zone]


# ══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="page-header">
  <div class="page-eyebrow">🌍 Page 2 · Earthquake Patterns</div>
  <div class="page-title">Global <span class="accent">Seismicity</span> Patterns</div>
  <div class="page-desc">
    Explore how earthquake frequency, depth, magnitude, and timing vary across years, tectonic
    settings, and latitudes. Use the sidebar to focus on specific countries, zones, and categories.
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DYNAMIC NARRATIVE + STAT PILLS
# ══════════════════════════════════════════════════════════════════════════════
if df.empty:
    st.warning("No earthquakes match the current filter combination. Try broadening your selection.")
    st.stop()

total_eq        = len(df)
day_eq          = df['is_daylight'].sum() if 'is_daylight' in df.columns else 0
night_eq        = total_eq - day_eq
pct_day         = day_eq / total_eq * 100 if total_eq else 0
avg_per_year    = total_eq / max(len(df['year'].unique()), 1)
tsunami_n       = df['tsunami'].sum()
most_active_yr  = df.groupby('year').size().idxmax() if total_eq else "—"
top_country     = df['country'].value_counts().idxmax() if 'country' in df.columns and total_eq else "—"

# Most common magnitude & depth labels
top_mag   = df['mag_category'].value_counts().idxmax()   if 'mag_category'   in df.columns else "—"
top_depth = df['depth_km_category'].value_counts().idxmax() if 'depth_km_category' in df.columns else "—"

year_label    = f"{year_range[0]}–{year_range[1]}" if year_range[0] != year_range[1] else str(year_range[0])
country_label = selected_country if selected_country != "All Countries" else "globally"
lat_label     = selected_lat_zone.lower() if selected_lat_zone != "All Zones" else "across all latitudes"

# Stat pills
st.markdown(f"""
<div class="stat-row">
  <div class="stat-pill">
    <div class="stat-pill-value">{total_eq:,}</div>
    <div class="stat-pill-label">Total Earthquakes</div>
  </div>
  <div class="stat-pill">
    <div class="stat-pill-value green">{avg_per_year:,.0f}</div>
    <div class="stat-pill-label">Avg per Year</div>
  </div>
  <div class="stat-pill">
    <div class="stat-pill-value">{pct_day:.0f}%</div>
    <div class="stat-pill-label">During Daytime (LST)</div>
  </div>
  <div class="stat-pill">
    <div class="stat-pill-value amber">{most_active_yr}</div>
    <div class="stat-pill-label">Most Active Year</div>
  </div>
  <div class="stat-pill">
    <div class="stat-pill-value red">{tsunami_n:,}</div>
    <div class="stat-pill-label">Tsunami Events</div>
  </div>
  <div class="stat-pill">
    <div class="stat-pill-value">{top_country}</div>
    <div class="stat-pill-label">Country</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Dynamic narrative text
st.markdown(f"""
<div class="narrative-card">
  <div class="narrative-text">
    Between <strong>{year_label}</strong>, a total of <strong>{total_eq:,} earthquakes</strong>
    were recorded {country_label}, {lat_label}.
    On average, <strong>{avg_per_year:,.0f} events per year</strong> occurred over this window,
    with <strong>{most_active_yr}</strong> standing out as the most seismically active year
    in the filtered selection.
    <br><br>
    When examined by local solar time, approximately <em>{pct_day:.0f}%</em> of earthquakes
    struck during daytime hours — a ratio that can hint at thermal or tidal loading effects
    depending on tectonic setting and depth regime.
    The dominant magnitude class was <em>{top_mag}</em>,
    and the most frequent depth regime was <em>{top_depth}</em>,
    consistent with the global prevalence of shallow crustal seismicity.
    <br><br>
    Of the recorded events, <strong>{tsunami_n:,} triggered a tsunami warning or observation</strong>
    — underscoring the hazard relevance of tracking seismic depth and coastal proximity alongside
    geomagnetic conditions.
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CHART 1 — Time-Series: Earthquake Frequency Over Time
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Chart 1</div>', unsafe_allow_html=True)

ts_label = {
    "depth_km_category":    "Earthquake Depth",
    "mag_category":         "Magnitude Category",
    "tectonic_proxy_zone":  "Tectonic Zone",
    "is_prolonged_shaking": "Shaking Duration",
    "latitude_zone":        "Latitude Zone",
}[ts_category]

st.markdown(f'<div class="section-title">Earthquake Frequency Over Time · by {ts_label}</div>', unsafe_allow_html=True)

st.markdown("""
<p style="font-size:0.84rem; color:#4a6a8a; margin:-0.5rem 0 1rem 0; font-family:'Space Mono',monospace;">
  Time-series of arthquake frequency from 2012 to 2025, grouped by selected feautures (e.g., depth (km), magnitude, duration, or latitude zones)
  Users can easily compare contributions from each category over time.
</p>
""", unsafe_allow_html=True)

# Aggregate
eq_counts = (
    df.groupby(["year_month", ts_category])
    .size()
    .reset_index(name="count")
)
eq_counts["year_month_dt"] = pd.to_datetime(eq_counts["year_month"].astype(str))

palette = CAT_PALETTES.get(ts_category, px.colors.qualitative.Plotly)

fig_ts = px.line(
    eq_counts,
    x="year_month_dt",
    y="count",
    color=ts_category,
    color_discrete_sequence=palette,
    markers=False,
    labels={
        "year_month_dt": "Date",
        "count": "Earthquake Count",
        ts_category: ts_label,
    },
)

fig_ts.update_traces(line=dict(width=2), opacity=0.9)

fig_ts.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(11,22,40,0.6)",
    font=dict(family="Space Mono, monospace", color="#8aaccc", size=11),
    title=None,
    xaxis=dict(
        title="Year",
        showgrid=True,
        gridcolor="rgba(30, 58, 95, 0.27)",
        zeroline=False,
        tickfont=dict(size=10),
        title_font=dict(size=11),
    ),
    yaxis=dict(
        title="Frequency (Count)",
        showgrid=True,
        gridcolor="rgba(30, 58, 95, 0.27)",
        zeroline=False,
        tickfont=dict(size=10),
        title_font=dict(size=11),
    ),
    legend=dict(
        title=dict(text=ts_label, font=dict(size=10)),
        bgcolor="rgba(4,6,15,0.8)",
        bordercolor="#1e3a5f",
        borderwidth=1,
        font=dict(size=10),
    ),
    margin=dict(l=10, r=10, t=10, b=10),
    hovermode="x unified",
)

st.plotly_chart(fig_ts, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# CHART 2 — LST Distribution Explorer
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Chart 2</div>', unsafe_allow_html=True)

lst_label = lst_color_by.replace("_", " ").title()
st.markdown(f'<div class="section-title">Local Solar Time Distribution · by {lst_label}</div>', unsafe_allow_html=True)

st.markdown("""
<p style="font-size:0.84rem; color:#4a6a8a; margin:-0.5rem 0 1rem 0; font-family:'Space Mono',monospace;">
  Average earthquake variations by exact local mean solar hour at the epicentre.
  Red dashed line = solar noon (12h) · Dotted = midnight (0h).
</p>
""", unsafe_allow_html=True)

# Filter for LST chart (depth on top of global filters)
df_lst = df.copy()
if selected_depth != "All":
    df_lst = df_lst[df_lst["depth_km_category"] == selected_depth]

df_lst["start_time"] = pd.to_datetime(df_lst["start_time"], errors="coerce")
df_lst = df_lst.dropna(subset=["start_time"])

if df_lst.empty:
    st.info("No data for the selected depth category and filters. Try selecting 'All' for depth.")
else:
# --- Prepare time dimension ---
    df_lst["date"] = df_lst["start_time"].dt.date

    # --- Step 1: count earthquakes per day per hour ---
    hourly = (
        df_lst.groupby(["date", "lst_hour", lst_color_by])
        .size()
        .reset_index(name="daily_count")
    )

    # --- Step 2: average across days ---
    lst_grouped = (
        hourly.groupby(["lst_hour", lst_color_by])["daily_count"]
        .mean()
        .reset_index(name="avg_count")
        .sort_values("lst_hour")
    )

    palette_lst = CAT_PALETTES.get(lst_color_by, CAT_PALETTES["mag_category"])

    fig_lst = px.line(
        lst_grouped,
        x="lst_hour",
        y="avg_count",
        color=lst_color_by,
        markers=True,
        color_discrete_sequence=palette_lst,
        labels={
            "lst_hour": "Local Solar Hour",
            "avg_count":    "Earthquake Count",
            lst_color_by: lst_label,
        },
    )

    fig_lst.update_traces(line=dict(width=2.5), marker=dict(size=6))

    # Reference lines
    fig_lst.add_vline(x=12, line_dash="dash",  line_color="rgba(224, 67, 19, 0.5)", line_width=1.5,
                      annotation_text="Noon", annotation_position="top",
                      annotation_font=dict(color="#e04313", size=9))
    fig_lst.add_vline(x=0,  line_dash="dot",   line_color="rgba(91, 138, 255, 0.4)", line_width=1.5,
                      annotation_text="Midnight", annotation_position="top right",
                      annotation_font=dict(color="#5b8aff", size=9))

    fig_lst.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(11,22,40,0.6)",
        font=dict(family="Space Mono, monospace", color="#8aaccc", size=11),
        title=None,
        xaxis=dict(
            title="Local Solar Hour",
            dtick=3,
            range=[-0.5, 23.5],
            showgrid=True,
            gridcolor="rgba(30, 58, 95, 0.27)",
            zeroline=False,
            tickfont=dict(size=10),
        ),
        yaxis=dict(
            title="Avg. Earthquake per Hour",
            showgrid=True,
            gridcolor="rgba(30, 58, 95, 0.27)",
            zeroline=False,
            tickfont=dict(size=10),
        ),
        legend=dict(
            title=dict(text=lst_label, font=dict(size=10)),
            bgcolor="rgba(4,6,15,0.8)",
            bordercolor="#1e3a5f",
            borderwidth=1,
            font=dict(size=10),
        ),
        margin=dict(l=10, r=10, t=20, b=10),
        hovermode="x unified",
    )

    st.plotly_chart(fig_lst, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER NAV
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)

fc1, fc2, fc3 = st.columns([1, 2, 1])
with fc1:
    if st.button("← Back to Home"):
        st.switch_page("app.py")
with fc3:
    if st.button("Solar Activity →"):
        st.switch_page("pages/page_3.py")

st.markdown("""
<div class="footer">
  STORM &amp; QUAKE · ETL PROCESS &amp; DATA SOURCES<br>
  DATA: USGS COMCAT (PUBLIC DOMAIN) · GFZ POTSDAM Kp (CC BY 4.0)<br>
  PLATE BOUNDARIES: BIRD 2003 (CC BY 4.0)<br>
  [ Paula Herrera · EDA Capstone Project · 2026 ]
</div>
""", unsafe_allow_html=True)