import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Solar Activity · Daytime, Storms & Quakes",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# PALETTE  (mirrors homepage + page_2)
# ══════════════════════════════════════════════════════════════════════════════
C_GREEN  = "#3a9e6af4"
C_BLUE   = "#5b8aff"
C_AMBER  = "#f4c542"
C_RED    = "#e04313"
C_BG     = "#04060f"
C_CARD   = "#0b1628"
C_BORDER = "#1e3a5f"

KP_COLORS = {
    "low":      "#1B2524",   # quiet  (Kp 0–2)
    "elevated": "#d4b13e",   # unsettled/active (Kp 3–4)
    "storm":    "#c54460",   # storm  (Kp ≥ 5)
}

EQ_LINE_COLORS = ["#0c1cfb","#c01909", "#11a641","#e0d614","#f28d08"]

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { background-color: #04060f; color: #e8eaf0; font-family: 'Inter', sans-serif; }
.main { background-color: #04060f; }
.block-container { padding: 1.5rem 2rem 4rem 2rem !important; max-width: 1400px; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060d1a 0%, #04060f 100%);
    border-right: 1px solid #1e3a5f44;
}
section[data-testid="stSidebar"] * { color: #e8eaf0 !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stSlider label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.65rem !important; letter-spacing: 0.15em !important;
    text-transform: uppercase !important; color: #00c494 !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #0b1628 !important; border-color: #1e3a5f !important; border-radius: 8px !important;
}

.page-header {
    background: radial-gradient(ellipse 70% 80% at 0% 50%, #0d3b2e33 0%, transparent 60%),
                radial-gradient(ellipse 50% 60% at 100% 0%, #1a1a4e44 0%, transparent 55%),
                linear-gradient(135deg, #060d1a 0%, #04060f 100%);
    border: 1px solid #1e3a5f44; border-radius: 14px;
    padding: 2rem 2.5rem 1.8rem 2.5rem; margin-bottom: 1.8rem;
    position: relative; overflow: hidden;
}
.page-header::before {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(ellipse 30% 40% at 80% 60%, #00c4940a 0%, transparent 60%),
                radial-gradient(ellipse 20% 30% at 10% 30%, #5b8aff08 0%, transparent 55%);
    pointer-events: none;
}
.page-eyebrow { font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.25em; text-transform:uppercase; color:#00c494; margin-bottom:0.6rem; }
.page-title   { font-family:'Satisfy',sans-serif; font-size:2.1rem; font-weight:800; color:#f0f4ff; margin:0 0 0.4rem 0; line-height:1.1; }
.page-title .acc-g { color:#00c494; }
.page-title .acc-b { color:#5b8aff; }
.page-desc    { font-size:0.9rem; color:#5a7a9a; line-height:1.65; max-width:700px; }

.section-label { font-family:'Space Mono',monospace; font-size:0.62rem; letter-spacing:0.2em; text-transform:uppercase; color:#00c494; margin-bottom:0.3rem; }
.section-title { font-family:'Satisfy',sans-serif; font-size:1.25rem; font-weight:700; color:#e8eaf0; margin-bottom:0.2rem; }

.aurora-divider { height:1px; background:linear-gradient(90deg,transparent,#1e3a5f,#00c49433,#1e3a5f,transparent); margin:2rem 0; }

.narrative-card {
    background: linear-gradient(135deg, #060f1e 0%, #081428 100%);
    border: 1px solid #1e3a5f66; border-left: 4px solid #00c494;
    border-radius: 10px; padding: 1.4rem 1.8rem; margin-bottom: 1.6rem;
    position: relative; overflow: hidden;
}
.narrative-card::before { content:'🌐'; position:absolute; right:1.5rem; top:1rem; font-size:2rem; opacity:0.1; }
.narrative-text { font-family:'Inter',sans-serif; font-size:0.92rem; color:#8aaccc; line-height:1.8; }
.narrative-text strong { color:#00c494; }
.narrative-text em     { color:#5b8aff; font-style:normal; }

.stat-row { display:flex; flex-wrap:wrap; gap:0.7rem; margin-bottom:1.4rem; }
.stat-pill { background:linear-gradient(135deg,#0b1628 0%,#0f2040 100%); border:1px solid #1e3a5f; border-radius:8px; padding:0.7rem 1rem; text-align:center; min-width:120px; flex:1; }
.stat-pill-value { font-family:'Satisfy',sans-serif; font-size:1.4rem; font-weight:800; color:#00c494; line-height:1; margin-bottom:0.2rem; }
.stat-pill-value.blue  { color:#5b8aff; }
.stat-pill-value.amber { color:#f4c542; }
.stat-pill-value.red   { color:#e04313; }
.stat-pill-label { font-family:'Space Mono',monospace; font-size:0.56rem; letter-spacing:0.1em; text-transform:uppercase; color:#3a5a7a; }

.chart-note { font-family:'Space Mono',monospace; font-size:0.68rem; color:#2a4a6a; line-height:1.6; margin:-0.2rem 0 0.8rem 0; }

.sidebar-header { font-family:'Satisfy',sans-serif; font-size:1rem; font-weight:700; color:#e8eaf0; margin-bottom:0.2rem; }
.sidebar-sub    { font-family:'Space Mono',monospace; font-size:0.6rem; color:#3a5a7a; letter-spacing:0.1em; margin-bottom:1.2rem; }

.footer { text-align:center; font-family:'Space Mono',monospace; font-size:0.58rem; color:#1a2a3a;
          letter-spacing:0.12em; padding:2rem 0 0 0; border-top:1px solid #0e1e2e; margin-top:3rem; line-height:2; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DATA LOAD
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    kp = pd.read_csv(
        "/Users/paus/Projects/da_capstone/data/processed/gfz_kp_df1.csv",
        parse_dates=["start_time"],
    )
    eq = pd.read_csv(
        "/Users/paus/Projects/da_capstone/data/processed/usgs_eq_df1.csv",
        parse_dates=["start_time"],
    )
    return kp, eq

gfz_kp_df, usgs_eq_df = load_data()


# ══════════════════════════════════════════════════════════════════════════════
# PREP  — shared derived columns
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def prep_kp(df):
    df = df.copy()
    df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
    df["year"]         = df["start_time"].dt.year
    df["year_month"]   = df["start_time"].dt.to_period("M").astype(str)
    df["year_month_dt"]= pd.to_datetime(df["year_month"])
    # Normalise kp_group labels  (handle variations like 'Storm', 'storm', etc.)
    if "kp_group" not in df.columns:
        # derive from kp column if kp_group is absent
        df["kp_group"] = pd.cut(
            df["kp"],
            bins=[-0.1, 2.9, 4.9, 9.1],
            labels=["low", "elevated", "storm"],
        )
    else:
        mapping = {}
        for raw in df["kp_group"].dropna().unique():
            r = str(raw).strip().lower()
            if any(s in r for s in ["storm", "≥5", ">= 5", "≥ 5"]):
                mapping[raw] = "storm"
            elif any(s in r for s in ["elevated", "active", "unsettled"]):
                mapping[raw] = "elevated"
            else:
                mapping[raw] = "low"
        df["kp_group"] = df["kp_group"].map(mapping).fillna("low")
    df["is_storm"] = df["kp_group"] == "storm"
    df["is_major"] = df["kp"] >= 7 if "kp" in df.columns else False
    return df

@st.cache_data
def prep_eq(df):
    df = df.copy()
    df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
    df["year"]          = df["start_time"].dt.year
    df["year_month"]    = df["start_time"].dt.to_period("M").astype(str)
    df["year_month_dt"] = pd.to_datetime(df["year_month"])
    return df

gfz_kp_df  = prep_kp(gfz_kp_df)
usgs_eq_df = prep_eq(usgs_eq_df)


# ══════════════════════════════════════════════════════════════════════════════
# DAYTIME-STORM FRACTION  — for a given country / global
# For each storm interval (Kp ≥ 5), check whether the subsolar longitude is
# within ±90° of the country's mean longitude → country is in daytime.
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def build_country_lon_lookup(eq_df):
    """Mean longitude per country from the EQ dataset."""
    return (
        eq_df.dropna(subset=["country", "longitude"])
        .groupby("country")["longitude"]
        .mean()
        .to_dict()
    )

country_lon = build_country_lon_lookup(usgs_eq_df)

def daytime_storm_fraction(kp_df, country_name):
    """
    Fraction of storm intervals (Kp ≥ 5) where the given country was in daylight.
    Uses subsolar_lon if present; otherwise estimates from UTC hour.
    """
    storms = kp_df[kp_df["is_storm"]].copy()
    if storms.empty:
        return np.nan

    if country_name == "All Countries":
        return np.nan   # not meaningful globally

    lon = country_lon.get(country_name, None)
    if lon is None:
        return np.nan

    # Subsolar longitude: if pre-computed use it, else derive from UTC hour
    if "subsolar_lon" in storms.columns:
        sub_lon = storms["subsolar_lon"].values
    else:
        utc_hour = storms["start_time"].dt.hour + storms["start_time"].dt.minute / 60
        sub_lon  = (utc_hour * 15 - 180) % 360 - 180   # −180 to +180

    # Angular difference between country longitude and subsolar longitude
    diff = np.abs(((lon - sub_lon) + 180) % 360 - 180)   # 0–180°
    # Country is in daylight if subsolar point is within ±90°
    frac = (diff <= 90).mean()
    return frac


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sidebar-header">🌐 Kp / Storm Filters</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">APPLIED TO ALL CHARTS ON THIS PAGE</div>', unsafe_allow_html=True)

    all_years  = sorted(gfz_kp_df["year"].dropna().unique().astype(int))
    year_range = st.select_slider("YEAR RANGE", options=all_years,
                                  value=(min(all_years), max(all_years)))

    st.markdown("---")

    all_countries   = ["All Countries"] + sorted(usgs_eq_df["country"].dropna().unique())
    selected_country = st.selectbox("COUNTRY (for daytime %)", options=all_countries)

    all_lat_zones    = ["All Zones"] + sorted(
        usgs_eq_df["latitude_zone"].dropna().unique()
        if "latitude_zone" in usgs_eq_df.columns else []
    )
    selected_lat_zone = st.selectbox("LATITUDE ZONE (EQ overlay)", options=all_lat_zones)

    st.markdown("---")
    st.markdown('<div class="section-label" style="margin-bottom:0.6rem;">Chart 1 · Overlay</div>', unsafe_allow_html=True)

    eq_overlay_cat = st.selectbox(
        "EQ OVERLAY CATEGORY",
        options=["mag_category", "depth_km_category", "is_prolonged_shaking"],
        format_func=lambda x: {
            "mag_category":         "Magnitude Category",
            "depth_km_category":    "Depth Category",
            "is_prolonged_shaking": "Shaking Duration",
        }[x],
    )

    st.markdown('<div class="section-label" style="margin:0.8rem 0 0.6rem 0;">Chart 2 · Rose Diagrams</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Space Mono\',monospace;font-size:0.58rem;color:#2a4a6a;margin-bottom:0.6rem;">ONE SUBPLOT PER LATITUDE ZONE</div>', unsafe_allow_html=True)

    all_depths = sorted(usgs_eq_df["depth_km_category"].dropna().unique()) \
        if "depth_km_category" in usgs_eq_df.columns else ["All"]
    rose_depth = st.selectbox("FILTER BY DEPTH", options=["All Depths"] + all_depths)

    rose_color_by = st.selectbox(
        "COLOUR PETALS BY",
        options=["mag_category", "depth_km_category", "tectonic_proxy_zone", "is_prolonged_shaking", "duration_category"],
        format_func=lambda x: x.replace("_", " ").title(),
    )


# ══════════════════════════════════════════════════════════════════════════════
# FILTER  — apply year range to both datasets
# ══════════════════════════════════════════════════════════════════════════════
kp_f  = gfz_kp_df[(gfz_kp_df["year"] >= year_range[0]) & (gfz_kp_df["year"] <= year_range[1])].copy()
eq_f  = usgs_eq_df[(usgs_eq_df["year"] >= year_range[0]) & (usgs_eq_df["year"] <= year_range[1])].copy()

if selected_country != "All Countries" and "country" in eq_f.columns:
    eq_f = eq_f[eq_f["country"] == selected_country]
if selected_lat_zone != "All Zones" and "latitude_zone" in eq_f.columns:
    eq_f = eq_f[eq_f["latitude_zone"] == selected_lat_zone]


# ══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="page-header">
  <div class="page-eyebrow">🌐 Page 3 · Solar Activity</div>
  <div class="page-title">Planetary <span class="acc-g">Kp Index</span> &amp; <span class="acc-b">Storm Patterns</span></div>
  <div class="page-desc">
    Explore the global distribution of geomagnetic activity from 2014 to 2025 — how storms cluster across
    solar cycle phases, seasons, and times of day, and how their timing aligns with concurrent
    seismic patterns. Use the sidebar to filter by year, country, and latitude zone.
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# NARRATIVE + STAT PILLS
# ══════════════════════════════════════════════════════════════════════════════
if kp_f.empty:
    st.warning("No Kp data for the selected year range.")
    st.stop()

total_obs    = len(kp_f)
n_storms     = int(kp_f["is_storm"].sum())
n_major      = int(kp_f["is_major"].sum()) if "is_major" in kp_f.columns else 0
avg_per_year = n_storms / max(len(kp_f["year"].unique()), 1)
most_active  = kp_f[kp_f["is_storm"]].groupby("year").size().idxmax() \
               if n_storms > 0 else "—"

day_frac     = daytime_storm_fraction(kp_f, selected_country)
day_pct_str  = f"{day_frac*100:.0f}%" if not np.isnan(day_frac) else "N/A"
day_pct_note = selected_country if selected_country != "All Countries" else "select a country"

year_label     = f"{year_range[0]}–{year_range[1]}" if year_range[0] != year_range[1] else str(year_range[0])
country_label  = selected_country if selected_country != "All Countries" else "globally"
lat_label      = selected_lat_zone.lower() if selected_lat_zone != "All Zones" else "all latitude zones"

pct_storm = n_storms / total_obs * 100 if total_obs else 0

st.markdown(f"""
<div class="stat-row">
  <div class="stat-pill">
    <div class="stat-pill-value">{total_obs:,}</div>
    <div class="stat-pill-label">Total Kp Intervals</div>
  </div>
  <div class="stat-pill">
    <div class="stat-pill-value red">{n_storms:,}</div>
    <div class="stat-pill-label">Storm Intervals (Kp≥5)</div>
  </div>
  <div class="stat-pill">
    <div class="stat-pill-value red">{n_major:,}</div>
    <div class="stat-pill-label">Major Storms (Kp≥7)</div>
  </div>
  <div class="stat-pill">
    <div class="stat-pill-value amber">{avg_per_year:.0f}</div>
    <div class="stat-pill-label">Avg Storm Intervals / Year</div>
  </div>
  <div class="stat-pill">
    <div class="stat-pill-value blue">{day_pct_str}</div>
    <div class="stat-pill-label">Daytime Storms · {day_pct_note}</div>
  </div>
  <div class="stat-pill">
    <div class="stat-pill-value amber">{most_active}</div>
    <div class="stat-pill-label">Most Active Year</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="narrative-card">
  <div class="narrative-text">
    Between <strong>{year_label}</strong>, the GFZ Kp dataset contains
    <strong>{total_obs:,} three-hourly intervals</strong>, of which
    <strong>{n_storms:,} ({pct_storm:.1f}%)</strong> qualified as geomagnetic storms (Kp&nbsp;≥&nbsp;5)
    and <strong>{n_major:,}</strong> reached major storm level (Kp&nbsp;≥&nbsp;7).
    On average, <strong>{avg_per_year:.0f} storm intervals</strong> were recorded per year,
    with <strong>{most_active}</strong> standing out as the most magnetically disturbed year
    in the selected window — likely reflecting the rising phase of Solar Cycle&nbsp;25.
    <br><br>
    {"For <em>" + selected_country + "</em>, approximately <strong>" + day_pct_str + "</strong> of storm intervals occurred while that location was in daylight — meaning the ionosphere above it was sunlit and more susceptible to solar electromagnetic forcing during those events." if selected_country != "All Countries" else
     "Select a <em>specific country</em> in the sidebar to compute what fraction of storm intervals occurred while that location was in daylight — a key parameter for assessing ionospheric coupling exposure."}
    <br><br>
    The stacked bar chart below contextualises Kp activity month by month,
    while the overlay lines track concurrent seismic frequency —
    making it possible to visually probe whether storm-heavy months show unusual earthquake patterns.
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CHART 1 — Monthly Kp Stacked Bars + EQ Frequency Overlay
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Chart 1</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Monthly Kp Observations vs Earthquake Frequency</div>', unsafe_allow_html=True)
st.markdown(f'<div class="chart-note">Stacked bars = Kp intensity groups (3-hourly counts) · Lines = EQ frequency by {eq_overlay_cat.replace("_"," ").title()} on secondary axis</div>', unsafe_allow_html=True)

# ── Kp stacked bars ──────────────────────────────────────────────────────────
monthly_kp = (
    kp_f.groupby(["year_month_dt", "kp_group"])
    .size()
    .reset_index(name="count")
)
# Ensure all three groups appear even if count is 0
all_months = kp_f["year_month_dt"].unique()
full_idx   = pd.MultiIndex.from_product(
    [all_months, ["low", "elevated", "storm"]], names=["year_month_dt", "kp_group"]
)
monthly_kp = (
    monthly_kp.set_index(["year_month_dt", "kp_group"])
    .reindex(full_idx, fill_value=0)
    .reset_index()
    .sort_values("year_month_dt")
)

fig1 = go.Figure()

for group, color in [("low", KP_COLORS["low"]),
                     ("elevated", KP_COLORS["elevated"]),
                     ("storm", KP_COLORS["storm"])]:
    d = monthly_kp[monthly_kp["kp_group"] == group]
    fig1.add_trace(go.Bar(
        x=d["year_month_dt"],
        y=d["count"],
        name={"low": "Quiet (Kp 0–2)", "elevated": "Active (Kp 3–4)", "storm": "Storm (Kp ≥ 5)"}[group],
        marker_color=color,
        marker_line_width=0,
        opacity=0.85,
        yaxis="y1",
        hovertemplate="%{x|%b %Y}<br>Count: %{y}<extra>%{fullData.name}</extra>",
    ))

# ── EQ frequency overlay ─────────────────────────────────────────────────────
eq_overlay = eq_f.copy()

if eq_overlay_cat in eq_overlay.columns:
    monthly_eq = (
        eq_overlay.groupby(["year_month_dt", eq_overlay_cat])
        .size()
        .reset_index(name="eq_count")
    )
    cats = sorted(monthly_eq[eq_overlay_cat].dropna().unique())

    for idx, cat in enumerate(cats):
        d = monthly_eq[monthly_eq[eq_overlay_cat] == cat].sort_values("year_month_dt")
        color = EQ_LINE_COLORS[idx % len(EQ_LINE_COLORS)]
        fig1.add_trace(go.Scatter(
            x=d["year_month_dt"],
            y=d["eq_count"],
            mode="lines",
            name=f"EQ · {cat}",
            line=dict(color=color, width=1.8, dash="solid"),
            opacity=0.75,
            yaxis="y2",
            hovertemplate="%{x|%b %Y}<br>EQ count: %{y}<extra>EQ · %{fullData.name}</extra>",
        ))

fig1.update_layout(
    barmode="stack",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(11,22,40,0.6)",
    font=dict(family="Space Mono, monospace", color="#8aaccc", size=10),
    xaxis=dict(
        title="Month",
        showgrid=False,
        tickangle=-35,
        tickfont=dict(size=9),
        tickformat="%b %Y",
    ),
    yaxis=dict(
        title="Kp Interval Count",
        showgrid=True,
        gridcolor="rgba(30, 58, 95, 0.27)",
        tickfont=dict(size=9),
        title_font=dict(color="#8aaccc"),
    ),
    yaxis2=dict(
        title="Earthquake Count",
        overlaying="y",
        side="right",
        showgrid=False,
        tickfont=dict(size=9),
        title_font=dict(color=EQ_LINE_COLORS[0]),
        tickcolor=EQ_LINE_COLORS[0],
    ),
    legend=dict(
        bgcolor="rgba(4,6,15,0.85)",
        bordercolor=C_BORDER,
        borderwidth=1,
        font=dict(size=9),
        orientation="h",
        yanchor="bottom",
        y=1.01,
        xanchor="left",
        x=0,
    ),
    hovermode="x unified",
    margin=dict(l=10, r=10, t=40, b=20),
    height=420,
    updatemenus=[dict(
        type="buttons", showactive=False, x=1, y=1.12, xanchor="right",
        buttons=[dict(
            label="Reset Zoom",
            method="relayout",
            args=[{"xaxis.autorange": True, "yaxis.autorange": True, "yaxis2.autorange": True}],
        )],
        bgcolor=C_CARD,
        bordercolor=C_BORDER,
        font=dict(color="#8aaccc", size=9),
    )],
)

st.plotly_chart(fig1, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# CHART 2 — 1 × 5 Polar Rose Subplots (one per latitude_zone_5)
# ══════════════════════════════════════════════════════════════════════════════
from plotly.subplots import make_subplots

st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Chart 2</div>', unsafe_allow_html=True)
depth_label = rose_depth if rose_depth != "All Depths" else "All Depths"
cat_label   = rose_color_by.replace("_", " ").title()
st.markdown(
    f'<div class="section-title">Earthquake Distribution by LST by Latitude Zone'
    f' · <span style="color:#00c494;">{depth_label}</span>'
    f' · coloured by <span style="color:#5b8aff;">{cat_label}</span></div>',
    unsafe_allow_html=True,
)
st.markdown("""
<div class="chart-note">
  Each subplot = one latitude zone (south → north). Petals = 1-hour LST bins.
  Midnight (00h) at top, clockwise. Dashed red line = solar noon (12h).
  Coloured by the selected category values. 
  The p-value shows results for Kuiper’s Test used for detecting significant deviation 
  from a uniform circle—perfect. That is, for identifying multiple windows of activity.
    - Low p-value (< 0.05): The distribution is not random. There is a statistically significant time-of-day bias.-   
    - High p-value: The earthquakes are distributed evenly (randomly) throughout the 24-hour cycle.
</div>
""", unsafe_allow_html=True)

def kuiper_test(hours):
    """Kuiper test for uniformity. Input: array of lst_hour values (0–23)."""
    angles = np.sort((hours / 24 * 2 * np.pi) % (2 * np.pi))
    n = len(angles)
    if n < 10:
        return 1.0
    i   = np.arange(1, n + 1)
    d_p = np.max(i / n - angles / (2 * np.pi))
    d_m = np.max(angles / (2 * np.pi) - (i - 1) / n)
    v   = d_p + d_m
    lam = v * (np.sqrt(n) + 0.155 + 0.24 / np.sqrt(n))
    if lam < 0.4:
        return 1.0
    p = 2 * sum((4 * m**2 * lam**2 - 1) * np.exp(-2 * m**2 * lam**2) for m in range(1, 10))
    return float(np.clip(p, 0, 1))


# ── Determine the 5 latitude zones in south-to-north order ───────────────────
LAT_ZONE_COL = "latitude_zone_5" if "latitude_zone_5" in eq_f.columns else "latitude_zone"

if LAT_ZONE_COL not in eq_f.columns or "lst_hour" not in eq_f.columns:
    st.info(f"Column `{LAT_ZONE_COL}` or `lst_hour` not found in the dataset.")
else:
    # Sort zones geographically S → N (by the first numeric value found in the label)
    raw_zones = eq_f[LAT_ZONE_COL].dropna().unique().tolist()

    def zone_sort_key(z):
        nums = [float(x) for x in __import__("re").findall(r"-?\d+\.?\d*", str(z))]
        return min(nums) if nums else 0

    zones_ordered = sorted(raw_zones, key=zone_sort_key)
    N_ZONES = len(zones_ordered)

    # ── Build subplot figure ──────────────────────────────────────────────────
    specs = [[{"type": "polar"}] * N_ZONES]
    subplot_titles = [str(z) for z in zones_ordered]

    rose_fig = make_subplots(
        rows=1, cols=N_ZONES,
        specs=specs,
        subplot_titles=subplot_titles,
        horizontal_spacing=0.04,
    )

    # Polar axis key: col 1 → "polar", col 2 → "polar2", …
    def polar_key(col):
        return "polar" if col == 1 else f"polar{col}"

    N_BINS        = 24
    BIN_WIDTH_DEG = 360 / N_BINS
    BIN_CENTRES   = np.linspace(0, 360, N_BINS, endpoint=False) + BIN_WIDTH_DEG / 2

    TICK_VALS = [h / 24 * 360 for h in range(0, 24, 3)]
    TICK_TEXT = [f"{h:02d}h" for h in range(0, 24, 3)]

    ROSE_PALETTE = ["#5f79cf","#b52d20", "#3e9b5b","#cfc947","#d38527"]

    # Filter by depth
    eq_rose_base = eq_f.copy()
    if rose_depth != "All Depths" and "depth_km_category" in eq_rose_base.columns:
        eq_rose_base = eq_rose_base[eq_rose_base["depth_km_category"] == rose_depth]

    # Collect all categories once so legend is consistent across subplots
    all_cats = (
        sorted(eq_rose_base[rose_color_by].dropna().unique())
        if rose_color_by in eq_rose_base.columns
        else ["All"]
    )

    # Track which category names have already had a legend entry added
    legend_shown = set()

    for col_idx, zone in enumerate(zones_ordered, start=1):
        pk    = polar_key(col_idx)
        sub   = eq_rose_base[eq_rose_base[LAT_ZONE_COL] == zone]
        n_sub = len(sub)

        # Kuiper p-value for this zone
        p_val      = kuiper_test(sub["lst_hour"].dropna().values) if n_sub >= 10 else 1.0
        is_sig     = p_val < 0.05
        radial_col = "#e04313" if is_sig else C_BORDER   # red ring if significant

        # ── One Barpolar trace per category ──────────────────────────────────
        for cat_idx, cat in enumerate(all_cats):
            cat_sub = (
                sub[sub[rose_color_by] == cat]
                if rose_color_by in sub.columns
                else sub
            )
            counts, _ = np.histogram(
                cat_sub["lst_hour"].dropna(), bins=N_BINS, range=(0, 24)
            )
            color      = ROSE_PALETTE[cat_idx % len(ROSE_PALETTE)]
            show_legend = cat not in legend_shown

            rose_fig.add_trace(
                go.Barpolar(
                    r=counts,
                    theta=BIN_CENTRES,
                    width=BIN_WIDTH_DEG,
                    name=str(cat),
                    marker_color=color,
                    marker_line_color=C_BG,
                    marker_line_width=0.5,
                    opacity=0.80,
                    subplot=pk,
                    showlegend=show_legend,
                    legendgroup=str(cat),
                    hovertemplate=(
                        f"<b>{zone}</b><br>"
                        "Hour: %{theta:.0f}° → "
                        + f"{'{'}theta{'}'}".replace("{theta}", "%{theta}")
                        + "<br>Count: %{r}"
                        + f"<extra>{cat}</extra>"
                    ),
                ),
                row=1, col=col_idx,
            )
            if show_legend:
                legend_shown.add(cat)

        # ── Solar noon dashed line at 180° ────────────────────────────────────
        max_r = sub.groupby("lst_hour").size().max() if n_sub > 0 else 1
        rose_fig.add_trace(
            go.Scatterpolar(
                r=[0, max_r * 1.2],
                theta=[180, 180],
                mode="lines",
                line=dict(color="rgb(224, 67, 19)", width=1.5, dash="dash"),
                subplot=pk,
                showlegend=False,
                hoverinfo="skip",
            ),
            row=1, col=col_idx,
        )

        # ── Annotate n and Kuiper p beneath the subplot title ─────────────────
        sig_marker = "★" if is_sig else "·"
        p_color    = "#e04313" if is_sig else "#2a4a6a"
        rose_fig.add_annotation(
            text=(
                f"<span style='color:{p_color};font-size:9px;'>"
                f"{sig_marker} n={n_sub:,}  p={p_val:.3f}</span>"
            ),
            xref="paper", yref="paper",
            x=(col_idx - 0.5) / N_ZONES,
            y=-0.06,
            showarrow=False,
            font=dict(family="Space Mono", size=8, color=p_color),
            align="center",
        )

        # ── Style each polar axis ─────────────────────────────────────────────
        rose_fig.update_layout(**{
            pk: dict(
                bgcolor="rgba(11,22,40,0.7)",
                angularaxis=dict(
                    tickmode="array",
                    tickvals=TICK_VALS,
                    ticktext=TICK_TEXT,
                    direction="clockwise",
                    rotation=90,
                    gridcolor="rgb(30, 58, 95)",
                    linecolor="rgb(30, 58, 95)",
                    tickfont=dict(family="Space Mono", size=7, color="#2a4a6a"),
                ),
                radialaxis=dict(
                    showticklabels=False,
                    gridcolor="rgb(30, 58, 95)",
                    linecolor="rgb(30, 58, 95)",
                ),
            )
        })

    # ── Global layout ─────────────────────────────────────────────────────────
    rose_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Space Mono", color="#8aaccc", size=9),
        legend=dict(
            bgcolor="rgba(4,6,15,0.88)",
            bordercolor=C_BORDER,
            borderwidth=1,
            font=dict(size=9),
            orientation="h",
            yanchor="bottom",
            y=1.08,
            xanchor="left",
            x=0,
            title=dict(text=cat_label + "  ", font=dict(size=9, color="#4a6a8a")),
        ),
        margin=dict(l=10, r=10, t=80, b=60),
        height=380,
    )

    # Style subplot title font (they're annotations in plotly)
    for ann in rose_fig.layout.annotations:
        if ann.text in subplot_titles:
            ann.update(
                font=dict(family="Space Mono", size=8, color="#4a6a8a"),
                y=ann.y + 0.01,
            )

    st.plotly_chart(rose_fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER NAV
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
fc1, _, fc3 = st.columns([1, 2, 1])
with fc1:
    if st.button("← Back to Home"):
        st.switch_page("app.py")
with fc3:
    if st.button("Takeaways →"):
        st.switch_page("pages/page_4.py")

st.markdown("""
<div class="footer">
  STORM &amp; QUAKE · ETL PROCESS &amp; DATA SOURCES<br>
  DATA: USGS COMCAT (PUBLIC DOMAIN) · GFZ POTSDAM Kp (CC BY 4.0)<br>
  PLATE BOUNDARIES: BIRD 2003 (CC BY 4.0)<br>
  [ Paula Herrera · EDA Capstone Project · 2026 ]
</div>
""", unsafe_allow_html=True)