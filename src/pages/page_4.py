import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Findings · Storm & Quake",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# FINDINGS DATA
# ── Run compute_findings.py in your notebook and paste the output dict here ──
# ══════════════════════════════════════════════════════════════════════════════
FINDINGS_DATA = {
    # ── Global activity ──────────────────────────────────────
    "total_events":         335035,
    "date_min":             "2014-01-01",
    "date_max":             "2025-12-30",
    "avg_per_day":          76.5,
    "avg_per_month":        2327,
    "most_active_year":     '2018',
    "most_active_count":    39000,
    "least_active_year":    '2017',
    "least_active_count":   22521,

    # ── Magnitude split (%) — replace with real values ───────
    "mag_pct": {
        "Minor (<4)":       47.9,
        "Light (4–5)":       47.4,
        "Moderate (5–6)":    4.3,
        "Strong (6–7)":      0.3,
        "Major (7+)":        0.00,
    },

    # ── Depth of moderate+ events ────────────────────────────
    "dom_depth_moderate_plus":     "Shallow (<70km)",
    "dom_depth_moderate_plus_pct": 69.9,

    # ── Latitude zones ───────────────────────────────────────
    "top_lat_zone_moderate_plus":     "Tropics (-23.5° to 23.5°) ",
    "top_lat_zone_moderate_plus_pct": 44.0,

    # ── LST daytime % per latitude zone ─────────────────────
    "lst_by_zone_daytime_pct": {
        "Southern Polar (< -66.5°)":           66.7,
        "Southern Mid-Latitudes (-66.5°–-23.5°)": 48.6,
        "Tropics (-23.5°–23.5°)":              47.5,
        "Northern Mid-Latitudes (23.5°–66.5°)":  50.2,
        "Northern Polar (> 66.5°)":            57.4,
    },
    "peak_lst_hour": 23,

    # ── Kp correlation hints ─────────────────────────────────
    "storm_rate_overall_pct":  2.02,
    "avg_eq_storm_day":        71.9,
    "avg_eq_quiet_day":        77.5,
    "storm_quiet_ratio":       0.928,
    "kp_by_mag_mean": {
        "Minor (<4)":      1.69,
        "Light (4–5)":     1.80,
        "Moderate (5–6)":  1.79,
        "Strong (6–7)":    1.82,
        "Major (7+)":      1.74,
    },
}

# ── Derived shortcuts ─────────────────────────────────────────────────────────
D = FINDINGS_DATA
minor_pct    = D["mag_pct"].get("Minor (<4)", 0)
light_pct    = D["mag_pct"].get("Light (4–5)", 0)
moderate_pct = D["mag_pct"].get("Moderate (5–6)", 0)
strong_pct   = D["mag_pct"].get("Strong (6–7)", 0)
major_pct    = D["mag_pct"].get("Major (7+)", 0)
hazard_pct   = round(moderate_pct + strong_pct + major_pct, 1)

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
    background: radial-gradient(ellipse 80% 60% at 20% -10%, #0d3b2e55 0%, transparent 60%),
                radial-gradient(ellipse 60% 40% at 80% 0%,  #1a1a4e66 0%, transparent 55%),
                linear-gradient(135deg, #060d1a 0%, #04060f 100%);
    border:1px solid #1e3a5f44; border-radius:14px;
    padding:2.2rem 2.8rem 2rem 2.8rem; margin-bottom:2rem;
    position:relative; overflow:hidden;
}
.page-header::before {
    content:''; position:absolute; inset:0;
    background: radial-gradient(ellipse 40% 30% at 15% 40%, #00c49415 0%, transparent 55%),
                radial-gradient(ellipse 50% 25% at 72% 30%, #5b5bff10 0%, transparent 50%);
    animation: aurora-soft 10s ease-in-out infinite alternate;
    pointer-events:none;
}
@keyframes aurora-soft {
    0%   { opacity:0.6; transform:translateY(0px); }
    100% { opacity:1.0; transform:translateY(-6px); }
}
.page-eyebrow { font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.25em; text-transform:uppercase; color:#00c494; margin-bottom:0.7rem; }
.page-title   { font-family:'Satisfy',sans-serif; font-size:2.2rem; font-weight:800; color:#f0f4ff; margin:0 0 0.5rem 0; line-height:1.1; }
.page-title .ag { color:#00c494; }
.page-title .ab { color:#5b8aff; }
.page-desc    { font-size:0.92rem; color:#5a7a9a; line-height:1.75; max-width:780px; }

/* ── Section labels ── */
.section-label { font-family:'Space Mono',monospace; font-size:0.63rem; letter-spacing:0.22em; text-transform:uppercase; color:#00c494; margin-bottom:0.3rem; }
.section-title { font-family:'Satisfy',sans-serif; font-size:1.35rem; font-weight:700; color:#e8eaf0; margin-bottom:0.9rem; }
.section-title .ag { color:#00c494; }
.section-title .ab { color:#5b8aff; }

/* ── Divider ── */
.aurora-divider { height:1px; background:linear-gradient(90deg,transparent,#1e3a5f,#00c49433,#1e3a5f,transparent); margin:2.2rem 0; }

/* ── Hero stat strip ── */
.hero-stats { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin-bottom:1.8rem; }
.hero-stat { background:linear-gradient(135deg,#0b1628 0%,#0d1f3a 100%); border:1px solid #1e3a5f55; border-radius:12px; padding:1.2rem 1rem; text-align:center; transition:border-color 0.2s, transform 0.2s; }
.hero-stat:hover { border-color:#00c49444; transform:translateY(-2px); }
.hs-value { font-family:'Satisfy',sans-serif; font-size:2rem; font-weight:800; line-height:1; margin-bottom:0.3rem; }
.hs-label { font-family:'Space Mono',monospace; font-size:0.58rem; letter-spacing:0.1em; text-transform:uppercase; color:#2a4a6a; line-height:1.4; }
.hs-sub   { font-size:0.72rem; color:#1e3a5f; margin-top:0.2rem; }

/* ── Finding cards ── */
.finding-card {
    background:linear-gradient(135deg,#060f1e 0%,#081428 100%);
    border:1px solid #1e3a5f55; border-radius:12px;
    padding:1.5rem 1.8rem; margin-bottom:1.1rem;
    position:relative; overflow:hidden;
    transition: border-color 0.2s;
}
.finding-card:hover { border-color:#1e3a5f99; }
.finding-card::before {
    content:attr(data-n);
    position:absolute; right:1.4rem; top:0.7rem;
    font-family:'Satisfy',sans-serif; font-size:4rem; font-weight:800;
    color:#ffffff04; line-height:1;
}
.fc-tag { display:inline-block; font-family:'Space Mono',monospace; font-size:0.58rem; letter-spacing:0.12em; text-transform:uppercase; padding:0.18rem 0.55rem; border-radius:4px; margin-bottom:0.65rem; }
.tag-geo  { background:#5b8aff12; border:1px solid #5b8aff33; color:#5b8aff; }
.tag-mag  { background:#f4c54212; border:1px solid #f4c54233; color:#f4c542; }
.tag-dep  { background:#00c49412; border:1px solid #00c49433; color:#00c494; }
.tag-lst  { background:#a78bfa12; border:1px solid #a78bfa33; color:#a78bfa; }
.tag-kp   { background:#e0431312; border:1px solid #e0431333; color:#e04313; }

.fc-title { font-family:'Satisfy',sans-serif; font-size:1.05rem; font-weight:700; color:#e8eaf0; margin-bottom:0.55rem; }
.fc-body  { font-size:0.88rem; color:#6a8aaa; line-height:1.8; }
.fc-body strong { color:#c8e0f0; }
.fc-body em     { color:#00c494; font-style:normal; }
.fc-body .kp    { color:#e04313; }

/* ── Inline highlight numbers ── */
.hl-green  { color:#00c494; font-family:'Satisfy',sans-serif; font-weight:700; }
.hl-blue   { color:#5b8aff; font-family:'Satisfy',sans-serif; font-weight:700; }
.hl-amber  { color:#f4c542; font-family:'Satisfy',sans-serif; font-weight:700; }
.hl-red    { color:#e04313; font-family:'Satisfy',sans-serif; font-weight:700; }

/* ── LST zone mini-bars ── */
.zone-row { display:flex; align-items:center; gap:0.8rem; margin-bottom:0.5rem; }
.zone-name { font-family:'Space Mono',monospace; font-size:0.62rem; color:#3a5a7a; width:280px; flex-shrink:0; letter-spacing:0.04em; }
.zone-bar-wrap { flex:1; height:10px; background:#0b1628; border-radius:5px; overflow:hidden; position:relative; }
.zone-bar { height:100%; border-radius:5px; }
.zone-pct { font-family:'Space Mono',monospace; font-size:0.65rem; color:#4a6a8a; width:40px; text-align:right; flex-shrink:0; }

/* ── Caveat box ── */
.caveat-box { background:#0a0f1e; border:1px solid #1e3a5f55; border-left:3px solid #f4c542; border-radius:8px; padding:1.1rem 1.4rem; margin-top:1rem; }
.caveat-text { font-size:0.82rem; color:#4a6a8a; line-height:1.7; font-style:italic; }
.caveat-text strong { color:#8aaccc; font-style:normal; }

/* ── Footer ── */
.footer { text-align:center; font-family:'Space Mono',monospace; font-size:0.58rem; color:#1a2a3a; letter-spacing:0.12em; padding:2rem 0 0 0; border-top:1px solid #0e1e2e; margin-top:3rem; line-height:2; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="page-header">
  <div class="page-eyebrow">🔬 Page 5 · Summary of Findings</div>
  <div class="page-title">What the <span class="ag">Data</span> Reveals</div>
  <div class="page-desc">
    A summary of the key descriptive findings from my EDA project:
    global seismicity patterns, magnitude and depth distributions,
    local solar time, and the relationship between
    geomagnetic storm activity and earthquake occurrence across
    <strong style="color:#e8eaf0;">{D['total_events']:,} events</strong>
    spanning <strong style="color:#e8eaf0;">{D['date_min']} → {D['date_max']}</strong>.
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HERO STAT STRIP
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero-stats">
  <div class="hero-stat">
    <div class="hs-value" style="color:#5b8aff;">{D['total_events']:,}</div>
    <div class="hs-label">Earthquakes Tracked</div>
    <div class="hs-sub">2014 – 2025 · USGS ComCat</div>
  </div>
  <div class="hero-stat">
    <div class="hs-value" style="color:#00c494;">{D['avg_per_day']}</div>
    <div class="hs-label">Average Events / Day</div>
    <div class="hs-sub">≈ {D['avg_per_month']:,} per month</div>
  </div>
  <div class="hero-stat">
    <div class="hs-value" style="color:#f4c542;">{hazard_pct}%</div>
    <div class="hs-label">Moderate or Above</div>
    <div class="hs-sub">Mw ≥ 5.0 · potential hazard</div>
  </div>
  <div class="hero-stat">
    <div class="hs-value" style="color:#e04313;">{D['storm_quiet_ratio']:.3f}</div>
    <div class="hs-label">Storm / Quiet Day Ratio</div>
    <div class="hs-sub">Avg EQ count · storm vs quiet days</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FINDING 1 — Global Activity
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">Finding 01</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Global <span class="ag">Seismic Activity</span> 2014–2025</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="finding-card" data-n="01">
  <span class="fc-tag tag-geo">Global Activity</span>
  <div class="fc-title">The Earth experiences roughly {D['avg_per_day']} recorded earthquakes every day</div>
  <div class="fc-body">
    Across the full study window from <strong>{D['date_min']}</strong> to <strong>{D['date_max']}</strong>,
    the USGS catalogue logged a total of <em>{D['total_events']:,} seismic events</em> worldwide, 
    an average of <strong>{D['avg_per_day']} earthquakes per day</strong>
    and approximately <strong>{D['avg_per_month']:,} per month</strong>.
    <br><br>
    Annual totals varied considerably: <strong>{D['most_active_year']}</strong> was the most seismically
    active year on record within this window, with <strong>{D['most_active_count']:,} events</strong>,
    while <strong>{D['least_active_year']}</strong> was the quietest at <strong>{D['least_active_count']:,}</strong>.
  </div>
</div>
""", unsafe_allow_html=True)

# ── Mini bar chart: events per year ──────────────────────────────────────────
@st.cache_data
def load_yearly():
    eq = pd.read_csv(
        "/Users/paus/Projects/da_capstone/data/processed/usgs_eq_df1.csv",
        usecols=["start_time"],
        parse_dates=["start_time"],
    )
    return eq["start_time"].dt.year.value_counts().sort_index().reset_index(
        ).rename(columns={"index": "year", "start_time": "count", "count": "count"})

try:
    yearly = load_yearly()
    # handle both old and new pandas column naming
    if "start_time" in yearly.columns:
        yearly = yearly.rename(columns={"start_time": "year_col"})
    yearly.columns = ["year", "count"]

    fig_yr = go.Figure(go.Bar(
        x=yearly["year"], y=yearly["count"],
        marker_color=[
            "#e04313" if y == D["most_active_year"] else
            "#00c494" if y == D["least_active_year"] else "#1e3a5f"
            for y in yearly["year"]
        ],
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Events: %{y:,}<extra></extra>",
    ))
    fig_yr.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(11,22,40,0.5)",
        font=dict(family="Space Mono", color="#4a6a8a", size=9),
        xaxis=dict(showgrid=False, tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor="#1e3a5f33", tickfont=dict(size=9),
                   title="Events", title_font=dict(size=9)),
        margin=dict(l=10, r=10, t=10, b=10), height=180,
        showlegend=False,
    )
    fig_yr.add_annotation(text=f"▲ {D['most_active_year']}", x=D["most_active_year"],
        y=D["most_active_count"], showarrow=False,
        font=dict(color="#e04313", size=9, family="Space Mono"), yshift=10)
    st.plotly_chart(fig_yr, use_container_width=True)
except Exception:
    st.caption(".")


# ══════════════════════════════════════════════════════════════════════════════
# FINDING 2 — Magnitude Distribution
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Finding 02</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title"><span class="ag">Magnitude</span> Distribution</div>', unsafe_allow_html=True)

col_mag_text, col_mag_chart = st.columns([3, 2], gap="large")

with col_mag_text:
    st.markdown(f"""
    <div class="finding-card" data-n="02">
      <span class="fc-tag tag-mag">Magnitude</span>
      <div class="fc-title">The vast majority of earthquakes are imperceptible to humans</div>
      <div class="fc-body">
        Of all tracked events, <em>{minor_pct:.1f}%</em> were <strong>Minor (Mw &lt; 4)</strong>
        and <strong>{light_pct:.1f}%</strong> were <strong>Light (Mw 4–5)</strong> —
        together accounting for <strong>{round(minor_pct+light_pct,1)}%</strong> of the catalogue.
        These events are detectable by instruments but rarely cause damage.
        <br><br>
        Events at <strong>Moderate level or above (Mw ≥ 5)</strong> represent
        <em>{hazard_pct}%</em> of all recorded events —
        roughly <strong>{round(D['total_events'] * hazard_pct / 100):,} earthquakes</strong> over
        the 11-year window.
        Strong events (Mw 6–7) account for <strong>{strong_pct:.1f}%</strong>,
        and major events (Mw ≥ 7) for not even 1% (<em>{major_pct:.1f}%</em>). However, these 129 
        earthquakes represented the bulk of global seismic energy release and humanitarian impact.
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_mag_chart:
    cats   = list(D["mag_pct"].keys())
    pcts   = list(D["mag_pct"].values())
    colors = ["#2f9970", "#c8a020", "#df883d", "#e04313", "#8a0808"]

    fig_mag = go.Figure(go.Bar(
        x=pcts, y=cats,
        orientation="h",
        marker_color=colors,
        marker_line_width=0,
        text=[f"{p:.1f}%" for p in pcts],
        textposition="outside",
        textfont=dict(family="Space Mono", size=9, color="#4a6a8a"),
        hovertemplate="%{y}<br>%{x:.1f}%<extra></extra>",
    ))
    fig_mag.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(11,22,40,0.5)",
        font=dict(family="Space Mono", color="#4a6a8a", size=9),
        xaxis=dict(showgrid=True, gridcolor="rgb(30, 58, 95)", ticksuffix="%",
                   range=[0, max(pcts) * 1.25], tickfont=dict(size=9)),
        yaxis=dict(showgrid=False, tickfont=dict(size=9)),
        margin=dict(l=10, r=60, t=10, b=10), height=220,
        showlegend=False,
    )
    st.plotly_chart(fig_mag, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# FINDING 3 — Depth × Latitude
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Finding 03</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Depth &amp; <span class="ab">Latitude</span> of Hazardous Events</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="finding-card" data-n="03">
  <span class="fc-tag tag-dep">Depth · Tectonic Setting</span>
  <div class="fc-title">Most damaging earthquakes are shallow and concentrated in tropical latitudes</div>
  <div class="fc-body">
    Among <strong>Moderate, Strong, and Major events (Mw ≥ 5)</strong>,
    <em>{D['dom_depth_moderate_plus_pct']:.1f}%</em> occurred in the
    <strong>{D['dom_depth_moderate_plus']}</strong> depth regime, consistent with
    the global dominance of shallow crustal seismicity along plate boundaries.
    Shallow earthquakes release their energy closer to the surface, translating
    into greater ground shaking and infrastructure impact for equivalent magnitudes.
    <br><br>
    Geographically, <em>{D['top_lat_zone_moderate_plus_pct']:.1f}%</em> of moderate-plus
    events occurred within the <strong>{D['top_lat_zone_moderate_plus']}</strong> latitude band,
    reflecting the dense subduction zones and transform faults that encircle the
    Pacific and converge through Southeast Asia and Central America.
  </div>
</div>
""", unsafe_allow_html=True)

# ── Heatmap: depth × latitude zone for moderate+ ─────────────────────────────
@st.cache_data
def load_depth_lat():
    eq = pd.read_csv(
        "/Users/paus/Projects/da_capstone/data/processed/usgs_eq_df1.csv",
        usecols=lambda c: c in ["mag", "mag_category", "depth_km_category",
                                "latitude_zone_5", "latitude_zone"],
    )
    lat_col = "latitude_zone_5" if "latitude_zone_5" in eq.columns else "latitude_zone"
    sub = eq[eq["mag_category"].isin(["Moderate (5–6)", "Strong (6–7)", "Major (7+)"])]
    pivot = sub.groupby([lat_col, "depth_km_category"]).size().unstack(fill_value=0)
    return pivot

try:
    pivot = load_depth_lat()
    fig_heat = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[c.replace(" ", "<br>") for c in pivot.columns],
        y=list(pivot.index),
        colorscale=[
            [0.0, "#04060f"], [0.3, "#256298"],
            [0.6, "#5b6bff"], [0.85, "#00c496"], [1.0, "#f4c242"],
        ],
        hovertemplate="<b>%{y}</b><br>%{x}<br>Count: %{z:,}<extra></extra>",
        showscale=True,
        colorbar=dict(
            title=dict(text="Events", font=dict(color="#4a6a8a", size=9,
                                                family="Space Mono")),
            tickfont=dict(color="#2a4a6a", size=8),
        ),
    ))
    fig_heat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Space Mono", color="#4a6a8a", size=9),
        xaxis=dict(tickfont=dict(size=8), side="bottom"),
        yaxis=dict(tickfont=dict(size=8)),
        margin=dict(l=10, r=10, t=10, b=10), height=260,
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    st.caption("Heatmap: Moderate+ earthquake counts by latitude zone × depth category")
except Exception:
    st.caption("(load data to display depth × latitude heatmap)")


# ══════════════════════════════════════════════════════════════════════════════
# FINDING 4 — Local Solar Time
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Finding 04</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Local Solar Time &amp; <span style="color:#f2ce57;">Diurnal Patterns</span></div>', unsafe_allow_html=True)

col_lst_text, col_lst_bars = st.columns([3, 2], gap="large")

with col_lst_text:
    # Find zone with highest and lowest daytime %
    lst_zones = D["lst_by_zone_daytime_pct"]
    max_zone  = max(lst_zones, key=lst_zones.get)
    min_zone  = min(lst_zones, key=lst_zones.get)

    st.markdown(f"""
    <div class="finding-card" data-n="04">
      <span class="fc-tag tag-lst">Local Solar Time</span>
      <div class="fc-title">Earthquake timing relative to solar position is near-uniform — with subtle polar deviations</div>
      <div class="fc-body">
        Globally, earthquakes occur across all local solar hours without a strong
        dominant peak. The most frequently observed local solar hour is
        <em>{D['peak_lst_hour']:02d}:00 h</em>, but the distribution is
        close to uniform, suggesting that solar-driven thermal or tidal loading is
        not a primary trigger of seismicity at the global scale.
        <br><br>
        By latitude zone, the fraction of events occurring during local daytime
        (06:00–18:00 LST) hovers between <strong>47.5% and 66.7%</strong> for all bands,
        clustering near <strong>~48–50%</strong> with an avergae of about <strong>54%</strong>,
        suggesting the relationship to solar position may not be entirely uniform across bands.
        <strong>{max_zone}</strong> shows the highest daytime proportion at
        <em>{lst_zones[max_zone]:.1f}%</em>, while
        <strong>{min_zone}</strong> shows the lowest at
        <em>{lst_zones[min_zone]:.1f}%</em>.
        The spread across latitude bands is moderate with specific statistical significance variations
        for specific geometries (locations) [refer to Kuiper test results on the Solar Activity page for details].
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_lst_bars:
    st.markdown('<div style="padding-top:0.4rem;">', unsafe_allow_html=True)
    zone_colors = ["#5b8aff", "#00c494", "#f4c542", "#00c494", "#5b8aff"]

    for i, (zone, pct) in enumerate(lst_zones.items()):
        bar_w = pct          # out of 100
        # Shorten zone label
        short = zone.split("(")[0].strip()
        color = zone_colors[i % len(zone_colors)]
        deviation = pct - 50.0
        dev_str = f"+{deviation:.1f}%" if deviation >= 0 else f"{deviation:.1f}%"
        st.markdown(f"""
        <div class="zone-row">
          <div class="zone-name">{short}</div>
          <div class="zone-bar-wrap">
            <div class="zone-bar" style="width:{bar_w}%;background:{color};opacity:0.7;"></div>
            <div style="position:absolute;top:0;left:50%;width:1px;height:100%;
                        background:#e0431344;"></div>
          </div>
          <div class="zone-pct">{pct:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#1e3a5f;
                margin-top:0.5rem;letter-spacing:0.08em;">
      BAR = % DAYTIME (LST 06–18H) · RED LINE = 50% RANDOM BASELINE
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FINDING 5 — Kp × Seismicity
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Finding 05</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Solar Activity &amp; <span style="color:#e04313;">Seismic Correlation</span></div>', unsafe_allow_html=True)

ratio       = D["storm_quiet_ratio"]
ratio_color = "#e04313" if ratio > 1.05 else "#f4c542" if ratio > 1.01 else "#00c494"
ratio_word  = "slightly elevated" if ratio > 1.01 else "essentially identical"

st.markdown(f"""
<div class="finding-card" data-n="05">
  <span class="fc-tag tag-kp">Kp Index · Storm Days</span>
  <div class="fc-title">Earthquake frequency on storm days is {ratio_word} compared to quiet days</div>
  <div class="fc-body">
    Merging each earthquake with its concurrent 3-hourly Kp interval,
    <em>{D['storm_rate_overall_pct']:.2f}%</em> of all recorded earthquakes occurred during
    a geomagnetic storm interval (Kp ≥ 5). On days when Kp ≥ 5 was reached at any point,
    the average number of earthquakes was <strong>{D['avg_eq_storm_day']}</strong>
    compared to <strong>{D['avg_eq_quiet_day']}</strong> on fully quiet days: a ratio of
    <span class="kp" style="color:{ratio_color}; font-weight:700;">{ratio:.3f}</span>.
    <br><br>
    By magnitude class, the mean Kp value at the time of each event shows only a slight variation,
    ranging from <em>{D['kp_by_mag_mean'].get('Minor (<4)', '—')}</em> for minor earthquakes (Mw<4) to
    <em>{D['kp_by_mag_mean'].get('Major (7+)', '—')}</em> for major earthquakes (Mw ≥ 7).
    While this pattern is directionally consistent with a weak positive association,
    the differences are small in magnitude. As such, the relationship cannot be interpreted as causal
    without further control for confounders such as aftershock sequences, solar cycle phase,
    and regional seismicity characteristics.
  </div>
</div>
""", unsafe_allow_html=True)

# ── Mean Kp by magnitude category — horizontal dot chart ─────────────────────
kp_mag_data = D["kp_by_mag_mean"]
fig_kp = go.Figure()

cats   = list(kp_mag_data.keys())
means  = list(kp_mag_data.values())
colors_kp = ["#3a9e6a", "#c8a020", "#df883d", "#e04313", "#8a0808"]

# Reference line at global mean Kp
global_kp_mean = round(sum(means) / len(means), 2)

fig_kp.add_vline(x=global_kp_mean, line_dash="dot", line_color="rgb(255, 255, 255)", line_width=1)
fig_kp.add_annotation(x=global_kp_mean, y=len(cats) - 0.3,
    text=f"mean {global_kp_mean}", showarrow=False,
    font=dict(color="#1e3a5f", size=8, family="Space Mono"), xanchor="left", xshift=4)

for i, (cat, mean, color) in enumerate(zip(cats, means, colors_kp)):
    fig_kp.add_trace(go.Scatter(
        x=[mean], y=[cat],
        mode="markers+text",
        marker=dict(size=14, color=color, line=dict(width=0)),
        text=[f"  {mean:.2f}"],
        textposition="middle right",
        textfont=dict(family="Space Mono", size=9, color=color),
        showlegend=False,
        hovertemplate=f"<b>{cat}</b><br>Mean Kp: {mean}<extra></extra>",
    ))

fig_kp.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(11,22,40,0.5)",
    font=dict(family="Space Mono", color="#4a6a8a", size=9),
    xaxis=dict(title="Mean Kp at time of earthquake", showgrid=True,
               gridcolor="rgb(30, 58, 95)", tickfont=dict(size=9),
               title_font=dict(size=9)),
    yaxis=dict(showgrid=False, tickfont=dict(size=9)),
    margin=dict(l=10, r=80, t=10, b=10), height=200,
    showlegend=False,
)
st.plotly_chart(fig_kp, use_container_width=True)

# ── Caveat ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="caveat-box">
  <div class="caveat-text">
    <strong>Interpretive caution:</strong>
    All findings presented here are descriptive and observational.
    The concurrent Kp assignment does not imply that geomagnetic conditions
    <em>caused</em> any individual earthquake. Aftershock sequences can inflate
    event counts independently of any external driver, and the solar cycle
    introduces a long-period confound that requires multi-cycle data to fully resolve.
    These findings are the starting point for hypothesis-driven testing —
    not conclusions.
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAKEAWAYS SUMMARY BOX
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Summary</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Five <span class="ag">Takeaways</span></div>', unsafe_allow_html=True)

takeaways = [
    ("🌍", "High background rate",
     f"Earth produces roughly {D['avg_per_day']} recorded earthquakes every day."),
    ("📏", "Dominated by small events",
     f"{round(minor_pct + light_pct, 1)}% of all events are Minor or Light (Mw < 5). Only {hazard_pct}% reach a Moderate threshold."),
    ("🕳️", "Shallow & tropical hazard concentration",
     f"{D['dom_depth_moderate_plus_pct']:.0f}% of hazardous events are shallow; {D['top_lat_zone_moderate_plus_pct']:.0f}% occur in {D['top_lat_zone_moderate_plus']}."),
    ("☀️", "No strong diurnal solar signal",
     f"Daytime earthquake fractions hover near 54% across all latitude zones (range: {min(D['lst_by_zone_daytime_pct'].values()):.1f}–{max(D['lst_by_zone_daytime_pct'].values()):.1f}%), near an even split, though with moderate variation between bands."),
    ("🧲", "Weak but present Kp gradient",
     f"Storm days show a lower average earthquake count than quiet days, with a storm-to-quiet ratio of {ratio:.3f} (71.9 vs 77.5 events per day). Mean Kp during Major earthquakes ({D['kp_by_mag_mean'].get('Major (7+)', '—')}) mariginally exceeds that at Minor events ({D['kp_by_mag_mean'].get('Minor (<4)', '—')}). Effect size is small; confounders unresolved."),
]

for icon, title, text in takeaways:
    st.markdown(f"""
    <div style="display:flex;gap:1rem;align-items:flex-start;margin-bottom:0.75rem;
                padding:1rem 1.2rem;background:#0b162888;
                border:1px solid #1e3a5f44;border-radius:10px;">
      <span style="font-size:1.3rem;flex-shrink:0;margin-top:0.05rem;">{icon}</span>
      <div>
        <div style="font-family:'Satisfy',sans-serif;font-size:0.95rem;font-weight:700;
                    color:#e8eaf0;margin-bottom:0.25rem;">{title}</div>
        <div style="font-size:0.87rem;color:#5a7a9a;line-height:1.65;">{text}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER NAV
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
fc1, _, fc3 = st.columns([1, 2, 1])
with fc1:
    if st.button("← Solar Activity"):
        st.switch_page("pages/page_3.py")
with fc3:
    if st.button("ETL & Sources →"):
        st.switch_page("pages/page_5.py")

st.markdown("""
<div class="footer">
  STORM &amp; QUAKE · SUMMARY OF FINDINGS · EDA PROJECT<br>
  DATA: USGS COMCAT (PUBLIC DOMAIN) · GFZ POTSDAM Kp (CC BY 4.0)
</div>
""", unsafe_allow_html=True)