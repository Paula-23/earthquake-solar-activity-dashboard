import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Concepts & Variables · Storm & Quake",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700&family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    background-color: #04060f;
    color: #e8eaf0;
    font-family: 'Inter', sans-serif;
}
.main { background-color: #04060f; }
.block-container { padding: 1.5rem 2.5rem 5rem 2.5rem !important; max-width: 1200px; }

/* ── Page header ── */
.page-header {
    background:
        radial-gradient(ellipse 70% 80% at 0% 50%,  #0d3b2e33 0%, transparent 60%),
        radial-gradient(ellipse 50% 60% at 100% 0%, #1a1a4e44 0%, transparent 55%),
        linear-gradient(135deg, #060d1a 0%, #04060f 100%);
    border: 1px solid #1e3a5f44;
    border-radius: 14px;
    padding: 2.2rem 2.8rem 2rem 2.8rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.page-header::before {
    content: '';
    position: absolute; inset: 0;
    background:
        radial-gradient(ellipse 30% 40% at 80% 60%, #5b8aff08 0%, transparent 60%),
        radial-gradient(ellipse 20% 30% at 10% 30%, #00c49408 0%, transparent 55%);
    pointer-events: none;
}
.page-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #5b8aff;
    margin-bottom: 0.7rem;
}
.page-title {
    font-family: 'Satisfy', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #f0f4ff;
    margin: 0 0 0.5rem 0;
    line-height: 1.1;
}
.page-title .accent-blue  { color: #5b8aff; }
.page-title .accent-green { color: #00c494; }
.page-desc {
    font-size: 0.92rem;
    color: #5a7a9a;
    line-height: 1.75;
    max-width: 780px;
}

/* ── Section labels ── */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.63rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #00c494;
    margin-bottom: 0.3rem;
}
.section-title {
    font-family: 'Satisfy', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #e8eaf0;
    margin-bottom: 1.1rem;
    line-height: 1.2;
}
.section-title .acc { color: #00c494; }
.section-title .acc-b { color: #5b8aff; }

/* ── Divider ── */
.aurora-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e3a5f, #00c49433, #1e3a5f, transparent);
    margin: 2.5rem 0;
}

/* ── Timeline ── */
.h-timeline {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    margin: 70px 10px 30px 10px;
    padding: 20px 0;
}
.h-timeline::before {
    content: '';
    position: absolute;
    top: 50%; left: 0;
    width: 100%; height: 2px;
    background: linear-gradient(to right, #1e3a5f, #00c49466, #1e3a5f);
}
.h-item {
    position: relative;
    text-align: center;
    cursor: default;
    flex: 1;
}
.h-dot {
    width: 14px; height: 14px;
    background: #00c494;
    border-radius: 50%;
    margin: 0 auto;
    box-shadow: 0 0 10px #00c49488;
    border: 2px solid #04060f;
    transition: transform 0.2s, box-shadow 0.2s;
}
.h-item:hover .h-dot {
    transform: scale(1.5);
    box-shadow: 0 0 20px #00c494cc;
}
.h-title {
    margin-top: 14px;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #4a6a8a;
    letter-spacing: 0.08em;
}
.h-tooltip {
    position: absolute;
    bottom: 46px;
    left: 50%;
    transform: translateX(-50%) scale(0.92);
    width: 220px;
    background: rgba(8,18,36,0.97);
    color: #8aaccc;
    padding: 14px 16px;
    border-radius: 10px;
    border: 1px solid #1e3a5f;
    font-size: 0.78rem;
    line-height: 1.55;
    opacity: 0;
    pointer-events: none;
    transition: all 0.22s ease;
    z-index: 10;
}
.h-tooltip strong { color: #00c494; }
.h-item:hover .h-tooltip {
    opacity: 1;
    transform: translateX(-50%) scale(1);
}

/* ── LAIC model image ── */
.laic-wrap {
    border: 1px solid #1e3a5f55;
    border-radius: 12px;
    overflow: hidden;
    background: #060d1a;
    padding: 0.5rem;
    margin-bottom: 0.4rem;
}
.laic-caption {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    color: #2a4a6a;
    text-align: center;
    letter-spacing: 0.1em;
    margin-top: 0.3rem;
    padding-bottom: 0.2rem;
}

/* ── Variable definition cards ── */
.var-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);  /* ← fixed 2 columns */
    gap: 1rem;
    margin-bottom: 0.5rem;
}
.var-card {
    background: linear-gradient(135deg, #0b1628 0%, #0d1f3a 100%);
    border: 1px solid #1e3a5f55;
    border-radius: 12px;
    padding: 1.3rem 1.4rem;
    transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
    position: relative;
    overflow: hidden;
}
.var-card:hover {
    border-color: #00c49455;
    transform: translateY(-2px);
    box-shadow: 0 8px 28px #00000033;
}
.var-card::before {
    content: attr(data-icon);
    position: absolute;
    right: 1rem; top: 0.8rem;
    font-size: 1.8rem;
    opacity: 0.10;
}
.var-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.18rem 0.55rem;
    border-radius: 4px;
    margin-bottom: 0.6rem;
    display: inline-block;
}
.var-tag-eq  { background:#5b8aff12; border:1px solid #5b8aff33; color:#5b8aff; }
.var-tag-kp  { background:#00c49412; border:1px solid #00c49433; color:#00c494; }
.var-name {
    font-family: 'Satisfy', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #e8eaf0;
    margin-bottom: 0.15rem;
}
.var-code {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #3a5a7a;
    margin-bottom: 0.6rem;
    letter-spacing: 0.05em;
}
.var-desc {
    font-size: 0.84rem;
    color: #6a8aaa;
    line-height: 1.65;
}
.var-range {
    margin-top: 0.65rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #00c49488;
    border-top: 1px solid #1e3a5f44;
    padding-top: 0.55rem;
}

/* ── Conversion explainer ── */
.formula-box {
    background: linear-gradient(135deg, #060f1e 0%, #081830 100%);
    border: 1px solid #1e3a5f88;
    border-left: 4px solid #00c494;
    border-radius: 10px;
    padding: 1.6rem 2rem;
    margin: 1.2rem 0;
}
.formula-title {
    font-family: 'Satisfy', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #e8eaf0;
    margin-bottom: 0.8rem;
}
.formula-eq {
    font-family: 'Space Mono', monospace;
    font-size: 1rem;
    color: #00c494;
    background: #00c4940d;
    border: 1px solid #00c49422;
    border-radius: 6px;
    padding: 0.7rem 1.2rem;
    margin: 0.7rem 0;
    letter-spacing: 0.04em;
}
.formula-note {
    font-size: 0.82rem;
    color: #4a6a8a;
    line-height: 1.7;
    margin-top: 0.5rem;
}
.formula-note em { color: #00c49499; font-style: normal; }
.formula-note strong { color: #8aaccc; }

/* ── Step cards ── */
.step-row {
    display: flex;
    gap: 1rem;
    margin: 1.1rem 0;
    flex-wrap: wrap;
}
.step-card {
    flex: 1;
    min-width: 180px;
    background: #0b1628;
    border: 1px solid #1e3a5f55;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    position: relative;
}
.step-num {
    font-family: 'Satisfy', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: #00c49418;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.step-head {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #00c494;
    margin-bottom: 0.4rem;
}
.step-body {
    font-size: 0.82rem;
    color: #5a7a9a;
    line-height: 1.6;
}
.step-body code {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #00c494;
    background: #00c4940d;
    padding: 0.1rem 0.3rem;
    border-radius: 3px;
}

/* ── Kp scale bar ── */
.kp-scale {
    display: flex;
    gap: 0;
    border-radius: 8px;
    overflow: hidden;
    margin: 0.8rem 0 0.4rem 0;
    height: 28px;
}
.kp-seg {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    color: #04060f;
}

/* ── Subsolar explainer ── */
.subsolar-box {
    background: linear-gradient(135deg, #060f1e 0%, #081830 100%);
    border: 1px solid #1e3a5f88;
    border-left: 4px solid #5b8aff;
    border-radius: 10px;
    padding: 1.6rem 2rem;
    margin: 1.2rem 0;
}

/* ── Footer ── */
.footer {
    text-align: center;
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    color: #1a2a3a;
    letter-spacing: 0.12em;
    padding: 2rem 0 0 0;
    border-top: 1px solid #0e1e2e;
    margin-top: 3rem;
    line-height: 2;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="page-header">
  <div class="page-eyebrow">📖 Page 1 · Concepts &amp; Variables</div>
  <div class="page-title">
    Earthquakes, <span class="accent-blue">Time</span>
    &amp; the <span class="accent-green">Sky</span>
  </div>
  <div class="page-desc">
    This project explores earthquakes not only as isolated geological events, but as part of a broader
    interconnected Earth system evolving through time. It combines modern data analytics with
    long-standing scientific questions about whether external environmental factors beyond our Atmosphere, 
    such as atmospheric, ionospheric, and solar dynamics, may influence seismic activity.
  </div>
  <div class="page-desc">
    In a creative form, the project applies the <strong style="color:#e8eaf0;">LAIC framework
    (Lithosphere–Atmosphere–Ionosphere Coupling)</strong>, which hypothesises that processes
    in Earth's crust may interact with layers above it, potentially leaving detectable
    signals before or around seismic events.
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — TIMELINE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Historical Context</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">From Ancient Observation to <span class="acc">Modern Multi-System Thinking</span></div>', unsafe_allow_html=True)

st.markdown("""
<div class="h-timeline">

  <div class="h-item">
    <div class="h-dot"></div>
    <div class="h-title">Pre-1500s</div>
    <div class="h-tooltip">
      <strong>Ancient & Mesoamerican Worldviews</strong><br><br>
      Earthquakes were embedded in cosmological narratives: the sky and Earth as one
      holistic living system. Though symbolic, these frameworks intuitively connected seismic
      phenomena with celestial cycles.
    </div>
  </div>

  <div class="h-item">
    <div class="h-dot"></div>
    <div class="h-title">1800s–1900s</div>
    <div class="h-tooltip">
      <strong>Early Scientific Observations</strong><br><br>
      First attempts to record and classify earthquakes. Researchers noted possible
      solar–seismic correlations, but without statistical tools, findings remained
      observational and speculative.
    </div>
  </div>

  <div class="h-item">
    <div class="h-dot"></div>
    <div class="h-title">1950s–1980s</div>
    <div class="h-tooltip">
      <strong>Space Age &amp; Geomagnetism</strong><br><br>
      The satellite era enabled systematic measurement of geomagnetic activity
      via the (planetarische Kennziffer) KP index. First quantitative comparisons with seismicity catalogues
      yielded mixed and inconclusive results.
    </div>
  </div>

  <div class="h-item">
    <div class="h-dot"></div>
    <div class="h-title">1990s–2010s</div>
    <div class="h-tooltip">
      <strong>Statistical &amp; Global Databases Era</strong><br><br>
      Global digitised catalogues (USGS, GFZ) enabled large-scale systematic testing.
      Mostly linear approaches applied — results remained contested, with no broad
      scientific consensus.
    </div>
  </div>

  <div class="h-item">
    <div class="h-dot"></div>
    <div class="h-title">2010s–Present</div>
    <div class="h-tooltip">
      <strong>Modern Analytics &amp; LAIC Framework</strong><br><br>
      High-resolution open data combined with machine learning allows exploration
      of complex, nonlinear Earth-system interactions. The LAIC framework formally
      models coupling between lithosphere, atmosphere, ionosphere, and magnetosphere.
    </div>
  </div>

</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — LAIC MODEL IMAGE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Conceptual Framework</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">The <span class="acc">LAIC</span> Model</div>', unsafe_allow_html=True)

col_laic_text, col_laic_img = st.columns([2, 3], gap="large")

with col_laic_text:
    st.markdown("""
    <div style="padding-top:0.4rem;">
      <p style="font-size:0.91rem; color:#6a8aaa; line-height:1.8; margin-bottom:1rem;">
        The <strong style="color:#e8eaf0;">Lithosphere–Atmosphere–Ionosphere Coupling (LAIC)</strong>
        model describes how disturbances originating deep in Earth's crust may propagate
        upward through successive layers of the atmosphere, eventually reaching the ionosphere
        and magnetosphere, as well as vice versa.
      </p>
      <p style="font-size:0.91rem; color:#6a8aaa; line-height:1.8; margin-bottom:1rem;">
        In this framework, pre-seismic stress in the lithosphere may emit signals that propagate
        <em style="color:#5b8aff;">upward</em> into ionospheric electron density, while 
        a geomagnetic storm driven by solar wind can couple <em style="color:#a64d7e;">downward</em> 
        into the lower atmosphere and crust. Exciting right?
      </p>
      <p style="font-size:0.91rem; color:#6a8aaa; line-height:1.8;">
        This bi-directional coupling is the theoretical foundation for investigating
        whether Kp-index anomalies and earthquake occurrence share any detectable
        patterns or statistical relationships!
      </p>

      <div style="margin-top:1.4rem; display:flex; flex-direction:column; gap:0.6rem;">
        <div style="display:flex; gap:0.8rem; align-items:center;">
          <div style="width:10px;height:10px;border-radius:50%;background:#2c8cbf;flex-shrink:0;box-shadow:0 0 8px #2c8cbf88;"></div>
          <span style="font-family:'Space Mono',monospace;font-size:0.68rem;color:#4a6a8a;letter-spacing:0.05em;">MAGNETOSPHERE · solar wind driver (Kp)</span>
        </div>
        <div style="display:flex; gap:0.8rem; align-items:center;">
          <div style="width:10px;height:10px;border-radius:50%;background:#7dccc4;flex-shrink:0;box-shadow:0 0 8px #7dccc488;"></div>
          <span style="font-family:'Space Mono',monospace;font-size:0.68rem;color:#4a6a8a;letter-spacing:0.05em;">IONOSPHERE · electromagnetic coupling</span>
        </div>
        <div style="display:flex; gap:0.8rem; align-items:center;">
          <div style="width:10px;height:10px;border-radius:50%;background:#fdd49e;flex-shrink:0;box-shadow:0 0 8px #fdd49e88;"></div>
          <span style="font-family:'Space Mono',monospace;font-size:0.68rem;color:#4a6a8a;letter-spacing:0.05em;">ATMOSPHERE · propagation medium</span>
        </div>
        <div style="display:flex; gap:0.8rem; align-items:center;">
          <div style="width:10px;height:10px;border-radius:50%;background:#e04313;flex-shrink:0;box-shadow:0 0 8px #e04313aa;"></div>
          <span style="font-family:'Space Mono',monospace;font-size:0.68rem;color:#4a6a8a;letter-spacing:0.05em;">LITHOSPHERE · seismic source zone</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_laic_img:
    # ── My image path ───────────────────────────────
    try:
        st.markdown('<div class="laic-wrap">', unsafe_allow_html=True)
        st.image(
            "/Users/paus/Projects/da_capstone/docs/figures/laic_model.png",
            use_container_width=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="laic-caption">✦ CONCEPTUAL LAIC MODEL · AN AWSOMELY HANDMADE COLLAGE BY PAULA</div>', unsafe_allow_html=True)
    except Exception:
        st.markdown("""
        <div style="border:1px dashed #1e3a5f; border-radius:10px; padding:3rem 2rem;
                    text-align:center; background:#060d1a; color:#2a4a6a;">
          <div style="font-size:2rem; margin-bottom:0.5rem;">🖼️</div>
          <div style="font-family:'Space Mono',monospace; font-size:0.68rem; letter-spacing:0.1em;">
            LAIC MODEL IMAGE<br>(place your scheme5.png here)
          </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — EARTHQUAKE VARIABLES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Key Variables · Seismicity</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title"><span class="acc-b">Earthquake</span> Variables</div>', unsafe_allow_html=True)

eq_vars = [
    {
        "icon": "⏱️", "tag": "var-tag-eq", "tag_label": "Seismicity",
        "name": "Local Solar Time",
        "code": "local_solar_time  ·  lst_hour",
        "desc": "The time at the earthquake's epicentre expressed relative to solar position, not political timezone. Derived from UTC and longitude. Allows detection of solar-driven diurnal patterns in seismicity independent of arbitrary timezone boundaries.",
        "range": "0 – 23 h (continuous) · 0 = midnight, 12 = solar noon",
    },
    {
        "icon": "📏", "tag": "var-tag-eq", "tag_label": "Seismicity",
        "name": "Magnitude",
        "code": "mag  ·  mag_category",
        "desc": "Moment magnitude (Mw) — a logarithmic measure of the energy released by an earthquake. Each whole-number step represents roughly 32× more energy released. Categorised into Minor, Light, Moderate, Strong, and Major classes.",
        "range": "Mw 2.0 – 9.5 · Minor (<4) → Major (7+)",
    },
    {
        "icon": "🕳️", "tag": "var-tag-eq", "tag_label": "Seismicity",
        "name": "Depth",
        "code": "depth_km  ·  depth_km_category",
        "desc": "Distance (km) from the surface to the earthquake's hypocentre. Depth strongly affects surface damage and the mechanism of rupture. Shallow quakes are most destructive; deep quakes involve different stress regimes and tectonic dynamics.",
        "range": "Shallow (<70 km) · Intermediate (70–300 km) · Deep (>300 km)",
    },
    {
        "icon": "⏳", "tag": "var-tag-eq", "tag_label": "Seismicity",
        "name": "Shaking Duration",
        "code": "duration  ·  duration_category  ·  is_prolonged_shaking",
        "desc": "The estimated duration of ground shaking in seconds. Prolonged shaking (>60 s) is associated with larger rupture areas and greater structural damage. This variable is also used as a proxy for slip length along the fault.",
        "range": "Seconds · Prolonged = >60 s · flagged as boolean",
    },
    {
        "icon": "🌐", "tag": "var-tag-eq", "tag_label": "Seismicity",
        "name": "Latitude Zone",
        "code": "latitude  ·  latitude_zone",
        "desc": "Geographic latitude of the epicentre, binned into three zones reflecting distinct tectonic and solar-loading environments. High latitudes are most sensitive to geomagnetic disturbances; low latitudes receive stronger direct solar radiation.",
        "range": "Low (<30°) · Mid (30–60°) · High (>60°)",
    },
    {
        "icon": "🗺️", "tag": "var-tag-eq", "tag_label": "Seismicity",
        "name": "Tectonic Proxy Zone",
        "code": "tectonic_proxy_zone  ·  dist_to_boundary_km",
        "desc": "Earthquake's tectonic setting, estimated by proximity to plate boundaries from a global polygon dataset. Subduction zones produce the largest and most frequent earthquakes; intraplate events are rarer but can occur far from any boundary.",
        "range": "Subduction · Transform · Mid-Ocean Ridge · Continental Rift · Intraplate",
    },
]

st.markdown('<div class="var-grid">', unsafe_allow_html=True)
for v in eq_vars:
    st.markdown(f"""
    <div class="var-card" data-icon="{v['icon']}">
      <span class="var-tag {v['tag']}">{v['tag_label']}</span>
      <div class="var-name">{v['icon']} {v['name']}</div>
      <div class="var-code">{v['code']}</div>
      <div class="var-desc">{v['desc']}</div>
      <div class="var-range">◈ {v['range']}</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Eq scale visual ─────────────────────────────────────────────────────────

st.markdown("""
<div style="margin: 1.2rem 0 0.4rem 0;">
  <div style="font-family:'Space Mono',monospace;font-size:0.62rem;color:#3a5a7a;
              letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.5rem;">
    Magnitude Scale Reference
  </div>

  <div class="kp-scale">
    <div class="kp-seg" style="background:#3a7a5a;">&lt;4</div>
    <div class="kp-seg" style="background:#c8c020;">5–6</div>
    <div class="kp-seg" style="background:#e07020;">6–7</div>
    <div class="kp-seg" style="background:#c02010;">7+</div>
  </div>

  <div style="display:flex;justify-content:space-between;
              font-family:'Space Mono',monospace;
              font-size:0.58rem;color:#2a3a4a;margin-top:0.3rem;">
    <span>Minor</span>
    <span>Moderate</span>
    <span style="color:#e04313aa;">Strong</span>
    <span style="color:#c02010aa;">Major</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — SOLAR / KP VARIABLES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Key Variables · Space Weather</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title"><span class="acc">Solar Activity</span> Variables</div>', unsafe_allow_html=True)

kp_vars = [
    {
        "icon": "🧲", "tag": "var-tag-kp", "tag_label": "Space Weather",
        "name": "Kp Index",
        "code": "kp  ·  kp_category  ·  kp_diff  ·  kp_abs_change",
        "desc": "The planetary K-index (Kp) is a 3-hourly global measure of geomagnetic disturbance, derived from a network of ground-based magnetometer stations. It quantifies how much Earth's magnetic field deviates from its quiet-day baseline due to solar wind pressure and CMEs.",
        "range": "0 (quiet) → 9 (extreme storm) · quasi-logarithmic scale",
    },
    {
        "icon": "🕐", "tag": "var-tag-kp", "tag_label": "Space Weather",
        "name": "Universal Coordinated Time",
        "code": "start_time (UTC)  ·  hour  ·  year  ·  month",
        "desc": "All GFZ Kp observations are timestamped in UTC — the global atomic time reference with no seasonal offset. The 3-hourly cadence means each day has 8 Kp readings. UTC is the starting point for any solar-local time conversion.",
        "range": "3-hourly intervals · 8 readings per day · anchored at 0° longitude",
    },
    {
        "icon": "☀️", "tag": "var-tag-kp", "tag_label": "Space Weather",
        "name": "Subsolar Latitude",
        "code": "subsolar_lat  ·  subsolar_lon",
        "desc": "The geographic coordinates of the point on Earth's surface where the Sun is directly overhead at any given UTC moment. The subsolar latitude shifts between ±23.5° following Earth's axial tilt across seasons, while longitude tracks the daily rotation.",
        "range": "Lat: −23.5° – +23.5° (seasonal) · Lon: −180° – +180° (daily rotation)",
    },
    {
        "icon": "🌊", "tag": "var-tag-kp", "tag_label": "Space Weather",
        "name": "Auroral Activity Proxy",
        "code": "auroral_activity_proxy",
        "desc": "A derived index approximating auroral energy deposition at high latitudes, estimated from the Kp value. High Kp values expand the auroral oval equatorward, increasing electromagnetic energy input at mid-latitudes — a potential atmospheric coupling pathway.",
        "range": "Derived from Kp · higher values = equatorward auroral expansion",
    },
    {
        "icon": "🔄", "tag": "var-tag-kp", "tag_label": "Space Weather",
        "name": "Solar Cycle Phase",
        "code": "solar_cycle_phase  ·  years_since_start",
        "desc": "The approximate phase of the ~11-year solar cycle at each observation timestamp, estimated from known solar minimum/maximum dates. Solar maximum periods see more frequent and intense geomagnetic storms, making this an important confounding variable.",
        "range": "Solar Cycle 24 & 25 · 2014–2025 · Rising / Maximum / Declining / Minimum",
    },
]

st.markdown('<div class="var-grid">', unsafe_allow_html=True)
for v in kp_vars:
    st.markdown(f"""
    <div class="var-card" data-icon="{v['icon']}">
      <span class="var-tag {v['tag']}">{v['tag_label']}</span>
      <div class="var-name">{v['icon']} {v['name']}</div>
      <div class="var-code">{v['code']}</div>
      <div class="var-desc">{v['desc']}</div>
      <div class="var-range">◈ {v['range']}</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Kp scale visual ─────────────────────────────────────────────────────────
st.markdown("""
<div style="margin: 1.2rem 0 0.4rem 0;">
  <div style="font-family:'Space Mono',monospace;font-size:0.62rem;color:#3a5a7a;
              letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.5rem;">
    Kp Scale Reference
  </div>
  <div class="kp-scale">
    <div class="kp-seg" style="background:#3a7a5a;">Kp 0</div>
    <div class="kp-seg" style="background:#2e9e6a;">Kp 1</div>
    <div class="kp-seg" style="background:#22c278;">Kp 2</div>
    <div class="kp-seg" style="background:#8ab820;">Kp 3</div>
    <div class="kp-seg" style="background:#c8c020;">Kp 4</div>
    <div class="kp-seg" style="background:#e8a020;">Kp 5</div>
    <div class="kp-seg" style="background:#e07020;">Kp 6</div>
    <div class="kp-seg" style="background:#d84020;">Kp 7</div>
    <div class="kp-seg" style="background:#c02010;">Kp 8</div>
    <div class="kp-seg" style="background:#8a0808; color:#ffaaaa;">Kp 9</div>
  </div>
  <div style="display:flex;justify-content:space-between;font-family:'Space Mono',monospace;
              font-size:0.58rem;color:#2a3a4a;margin-top:0.3rem;">
    <span>Quiet</span>
    <span>Unsettled</span>
    <span>Active</span>
    <span style="color:#e04313aa;">Storm threshold (G1)</span>
    <span style="color:#c02010aa;">Severe</span>
    <span style="color:#8a0808aa;">Extreme</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — UTC → LST CONVERSION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)

col_1, col_2 = st.columns([2, 2], gap="medium")

with col_1:
    st.markdown('<div class="section-label">Local Solar Time · Eq Dataset </div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">From <span class="acc-b">UTC</span> to <span class="acc-b">Local Solar Time</span></div>', unsafe_allow_html=True)

    st.markdown("""
    <p style="font-size:0.9rem; color:#6a8aaa; line-height:1.8; margin-bottom:1rem;">
      Earthquake timestamps in the USGS catalogue are recorded in
      <strong style="color:#5b8aff;">UTC (Coordinated Universal Time)</strong> —
      a global reference anchored to 0° longitude that ignores political timezones and
      daylight saving. To study whether solar position at the moment of an earthquake
      matters, we must convert each event's UTC time into the
      <strong style="color:#00c494;">Local Mean Solar Time (LST)</strong> at its epicentre.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
      <div class="formula-title">The Conversion Formula</div>
      <div class="formula-eq">LST (hours) = UTC + ( longitude / 15 )</div>
      <div class="formula-note">
        <strong>Why divide by 15?</strong><br>
        Earth is a 360° sphere that completes one full rotation in 24 hours.
        That means it rotates at exactly <em>15° per hour</em>
        (360° ÷ 24h = 15°/h). Dividing any longitude value by 15 therefore
        converts that angular position directly into an equivalent number of hours
        ahead of (East, +) or behind (West, −) the solar meridian.<br><br>
        A quake at longitude +90° E occurred when the Sun was
        <em>6 hours further along</em> in its arc than at 0°.
        A quake at −75° W occurred <em>5 hours earlier</em> in solar terms.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="step-row">
      <div class="step-card">
        <div class="step-num">01</div>
        <div class="step-head">Record UTC time</div>
        <div class="step-body">
          USGS logs each event with a UTC timestamp.
          e.g. <code>2020-01-15 03:42 UTC</code>
        </div>
      </div>
      <div class="step-card">
        <div class="step-num">02</div>
        <div class="step-head">Get longitude</div>
        <div class="step-body">
          Extract the epicentre longitude from the earthquake record.
          e.g. <code>lon = +141.5° (Japan)</code>
        </div>
      </div>
      <div class="step-card">
        <div class="step-num">03</div>
        <div class="step-head">Compute LST hour</div>
        <div class="step-body">
          <code>LST = 3.7h + (141.5 / 15)</code><br>
          <code>LST = 3.7 + 9.43 = 13.13h</code><br>
          → just after solar noon locally
        </div>
      </div>
      <div class="step-card">
        <div class="step-num">04</div>
        <div class="step-head">Wrap to 0–24h</div>
        <div class="step-body">
          Apply <code>mod 24</code> to keep the result within a valid solar day.
          Negative values wrap to the previous solar day.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_2:
    st.markdown('<div class="section-label">Subsolar Point · Kp Dataset</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><span class="acc">Subsolar Point</span> for Space Weather</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="subsolar-box">
      <div class="formula-title" style="color:#5b8aff;">What is the Subsolar Point?</div>
      <div class="formula-note" style="margin-top:0;">
        The <strong style="color:#e8eaf0;">subsolar point</strong> is the single location on Earth's
        surface where the Sun is directly overhead — where a vertical pole casts no shadow.
        It moves continuously as Earth rotates and orbits the Sun, tracing a path between
        ±23.5° latitude over the year (following the solar declination) and sweeping
        360° of longitude every 24 hours.
        <br><br>
        For the Kp dataset, the subsolar point is estimated at each 3-hour interval
        using two components:
      </div>

      <div style="margin-top:1.1rem;">
        <div class="formula-title" style="font-size:0.9rem; color:#8aaccc;">① Subsolar Longitude (daily rotation)</div>
        <div class="formula-eq" style="font-size:0.88rem;">subsolar_lon = ( UTC_hour × 15 ) − 180   [mod 360, shifted to −180:+180]</div>
        <div class="formula-note">
          At UTC 00:00, the subsolar point sits near 180° W (date line, midnight).
          It advances <em>15° eastward per hour</em> as Earth rotates,
          reaching 0° (Greenwich) at UTC 12:00 (solar noon at 0° lon).
        </div>
      </div>

      <div style="margin-top:1.1rem;">
        <div class="formula-title" style="font-size:0.9rem; color:#8aaccc;">② Subsolar Latitude (seasonal tilt)</div>
        <div class="formula-eq" style="font-size:0.88rem;">subsolar_lat = 23.45 × sin( 360/365 × (day_of_year − 81) )</div>
        <div class="formula-note">
          Earth's axial tilt of ~23.45° means the Sun is directly overhead somewhere
          between the Tropics of Cancer (+23.5°N) and Capricorn (−23.5°S).
          The formula maps day-of-year onto a sinusoidal curve peaking at the June solstice.
          <br><br>
          <strong>Why does this matter for Kp?</strong>
          The subsolar latitude affects where solar radiation is most intense and
          where magnetospheric coupling into the ionosphere is strongest — making it
          a useful contextual variable when comparing geomagnetic activity across seasons.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # st.markdown('<div class="laic-wrap" style="margin-top:1rem;">', unsafe_allow_html=True)
    # st.image("/path/to/earth_subsolar.png", use_container_width=True)
    # st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER NAV
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)

fc1, fc2, fc3 = st.columns([1, 2, 1])
with fc1:
    if st.button("← Back to Home"):
        st.switch_page("app.py")
with fc3:
    if st.button("Earthquake Patterns →"):
        st.switch_page("pages/page_2.py")

st.markdown("""
<div class="footer">
  STORM &amp; QUAKE · ETL PROCESS &amp; DATA SOURCES<br>
  DATA: USGS COMCAT (PUBLIC DOMAIN) · GFZ POTSDAM Kp (CC BY 4.0)<br>
  PLATE BOUNDARIES: BIRD 2003 (CC BY 4.0)<br>
  [ Paula Herrera · EDA Capstone Project · 2026 ]
</div>
""", unsafe_allow_html=True)