"""
compute_findings.py
───────────────────
Run this script (or paste into a notebook cell) to compute every statistic
used in the findings page (page_5.py).

It prints a Python dict literal you can paste directly into page_5.py
under the FINDINGS_DATA block, replacing the placeholder values.
"""

import pandas as pd
import numpy as np

# ── 1. Load data ──────────────────────────────────────────────────────────────
eq = pd.read_csv(
    "/Users/paus/Projects/da_capstone/data/processed/usgs_eq_df1.csv",
)
kp = pd.read_csv(
    "/Users/paus/Projects/da_capstone/data/processed/gfz_kp_df1.csv"
)

print("✓ Data loaded:", len(eq), "EQ rows |", len(kp), "Kp rows")

# ── 2. Global activity ────────────────────────────────────────────────────────
total_events    = len(eq)
date_min        = eq["start_time"].min()
date_max        = eq["start_time"].max()
n_days          = (eq["start_time"].max() - eq["start_time"].min()).days + 1
n_months        = round(n_days / 30.44, 1)
avg_per_day     = round(total_events / n_days, 1)
avg_per_month   = round(total_events / n_months, 0)

# Most active year
by_year = eq.groupby("year").size()
most_active_year   = int(by_year.idxmax())
most_active_count  = int(by_year.max())
least_active_year  = int(by_year.idxmin())
least_active_count = int(by_year.min())

print(f"\n── Global Activity ──")
print(f"  Total events      : {total_events:,}")
print(f"  Date range        : {date_min} → {date_max}")
print(f"  Days covered      : {n_days:,}")
print(f"  Avg per day       : {avg_per_day}")
print(f"  Avg per month     : {avg_per_month:,.0f}")
print(f"  Most active year  : {most_active_year} ({most_active_count:,} events)")
print(f"  Least active year : {least_active_year} ({least_active_count:,} events)")

# ── 3. Magnitude breakdown ────────────────────────────────────────────────────
mag_counts = eq["mag_category"].value_counts()
mag_pct    = (mag_counts / total_events * 100).round(1)

print(f"\n── Magnitude Distribution ──")
for cat, pct in mag_pct.items():
    print(f"  {cat:30s}: {mag_counts[cat]:>7,}  ({pct:.1f}%)")

# ── 4. Depth × Magnitude (moderate + strong only) ────────────────────────────
mid_strong = eq[eq["mag_category"].isin(["Moderate (5–6)", "Strong (6–7)", "Major (7+)"])]
depth_x_mag = (
    mid_strong.groupby(["mag_category", "depth_km_category"])
    .size()
    .reset_index(name="count")
)
depth_x_mag["pct"] = (depth_x_mag["count"] /
                      depth_x_mag.groupby("mag_category")["count"]
                      .transform("sum") * 100).round(1)

print(f"\n── Depth × Magnitude (Moderate+) ──")
print(depth_x_mag.to_string(index=False))

# Dominant depth for moderate+
dom_depth_mod = mid_strong["depth_km_category"].value_counts().idxmax()
dom_depth_pct = round(mid_strong["depth_km_category"].value_counts(normalize=True).max() * 100, 1)
print(f"  → Dominant depth (moderate+): {dom_depth_mod} ({dom_depth_pct}%)")

# ── 5. Latitude zone breakdown (latitude_zone_5) ─────────────────────────────
LAT5_COL = "latitude_zone_5" if "latitude_zone_5" in eq.columns else "latitude_zone"

lat5_counts = eq[LAT5_COL].value_counts().sort_index()
lat5_pct    = (lat5_counts / total_events * 100).round(1)

print(f"\n── Latitude Zone Distribution ({LAT5_COL}) ──")
for zone, pct in lat5_pct.items():
    print(f"  {str(zone):45s}: {lat5_counts[zone]:>7,}  ({pct:.1f}%)")

# Moderate+ by latitude zone
lat5_mod = mid_strong[LAT5_COL].value_counts()
lat5_mod_pct = (lat5_mod / len(mid_strong) * 100).round(1)
top_lat_mod  = lat5_mod.idxmax()
top_lat_mod_pct = float(lat5_mod_pct.max())

print(f"\n── Moderate+ Earthquakes by Latitude Zone ──")
for zone, pct in lat5_mod_pct.items():
    print(f"  {str(zone):45s}: {lat5_mod[zone]:>7,}  ({pct:.1f}%)")
print(f"  → Dominant zone: {top_lat_mod} ({top_lat_mod_pct}%)")

# ── 6. Local Solar Time analysis ──────────────────────────────────────────────
# For each latitude zone: fraction of earthquakes in daytime vs nighttime
print(f"\n── Daytime vs Nighttime by Latitude Zone ({LAT5_COL}) ──")
lst_by_zone = {}
for zone in sorted(eq[LAT5_COL].dropna().unique(), key=lambda z: str(z)):
    sub = eq[eq[LAT5_COL] == zone]
    if "is_daylight" in sub.columns:
        day_pct = round(sub["is_daylight"].mean() * 100, 1)
    else:
        day_pct = round((sub["lst_hour"].between(6, 17)).mean() * 100, 1)
    lst_by_zone[str(zone)] = day_pct
    print(f"  {str(zone):45s}: {day_pct:.1f}% daytime")

# Peak LST hour (globally)
if "lst_hour" in eq.columns:
    peak_lst_hour = int(eq["lst_hour"].value_counts().idxmax())
    lst_uniformity = eq["lst_hour"].value_counts(normalize=True)
    lst_range_pct  = round((lst_uniformity.max() - lst_uniformity.min()) * 100, 2)
    print(f"\n  Global peak LST hour : {peak_lst_hour:02d}:00 h")
    print(f"  Max–min LST spread   : {lst_range_pct}% (deviation from uniform)")

# ── 7. Kp × Seismicity correlation hints ─────────────────────────────────────
# Merge EQ with concurrent Kp interval
eq["kp_interval"] = eq["start_time"].dt.floor("3h")
merged = eq.merge(
    kp[["start_time", "kp", "storm"]].rename(columns={"start_time": "kp_interval"}),
    on="kp_interval", how="left",
)

# Average Kp for events by magnitude category
print(f"\n── Mean Kp at time of earthquake, by magnitude category ──")
kp_by_mag = merged.groupby("mag_category")["kp"].agg(["mean", "median", "count"])
kp_by_mag["mean"]   = kp_by_mag["mean"].round(2)
kp_by_mag["median"] = kp_by_mag["median"].round(2)
print(kp_by_mag.to_string())

# Storm window analysis: % of events during storm (Kp≥5) vs quiet
if "storm" in merged.columns:
    storm_rate_overall = round(merged["storm"].mean() * 100, 2)
    storm_rate_by_mag  = merged.groupby("mag_category")["storm"].mean().mul(100).round(2)
    print(f"\n  Overall % EQ during storm interval : {storm_rate_overall}%")
    print(f"\n── % of earthquakes occurring during a storm (Kp≥5) ──")
    print(storm_rate_by_mag.to_string())

# Kp storm vs quiet: mean daily EQ count
daily_kp = kp.copy()
daily_kp["date"] = daily_kp["start_time"].dt.date
daily_kp["max_kp"] = daily_kp.groupby("date")["kp"].transform("max")
daily_kp["storm_day"] = daily_kp["max_kp"] >= 5

eq["date"] = eq["start_time"].dt.date
daily_eq = eq.groupby("date").size().reset_index(name="n_eq")
daily_merged = daily_eq.merge(
    daily_kp[["date", "storm_day"]].drop_duplicates(), on="date", how="left"
)

avg_eq_storm_day = round(daily_merged[daily_merged["storm_day"] == True]["n_eq"].mean(), 1)
avg_eq_quiet_day = round(daily_merged[daily_merged["storm_day"] == False]["n_eq"].mean(), 1)
ratio = round(avg_eq_storm_day / avg_eq_quiet_day, 3) if avg_eq_quiet_day else 1.0

print(f"\n── Daily EQ count: storm days vs quiet days ──")
print(f"  Avg EQ on storm days  (Kp≥5 at some point): {avg_eq_storm_day}")
print(f"  Avg EQ on quiet days  (Kp<5 all day)       : {avg_eq_quiet_day}")
print(f"  Ratio (storm/quiet)                         : {ratio}")

# ── 8. Print paste-ready dict ─────────────────────────────────────────────────
print("\n" + "="*60)
print("PASTE THIS INTO page_5.py  →  FINDINGS_DATA = { ... }")
print("="*60)
print(f"""
FINDINGS_DATA = {{
    # ── Global activity ──────────────────────────────────────
    "total_events":         {total_events},
    "date_min":             "{date_min}",
    "date_max":             "{date_max}",
    "avg_per_day":          {avg_per_day},
    "avg_per_month":        {int(avg_per_month)},
    "most_active_year":     {most_active_year},
    "most_active_count":    {most_active_count},
    "least_active_year":    {least_active_year},
    "least_active_count":   {least_active_count},

    # ── Magnitude split (%) ──────────────────────────────────
    "mag_pct": {dict(mag_pct)},

    # ── Depth of moderate+ events ────────────────────────────
    "dom_depth_moderate_plus":     "{dom_depth_mod}",
    "dom_depth_moderate_plus_pct": {dom_depth_pct},

    # ── Latitude zones ───────────────────────────────────────
    "top_lat_zone_moderate_plus":     "{top_lat_mod}",
    "top_lat_zone_moderate_plus_pct": {top_lat_mod_pct},

    # ── LST ──────────────────────────────────────────────────
    "lst_by_zone_daytime_pct": {lst_by_zone},
    "peak_lst_hour":           {peak_lst_hour if "lst_hour" in eq.columns else "None"},

    # ── Kp correlation hints ─────────────────────────────────
    "storm_rate_overall_pct":  {storm_rate_overall},
    "avg_eq_storm_day":        {avg_eq_storm_day},
    "avg_eq_quiet_day":        {avg_eq_quiet_day},
    "storm_quiet_ratio":       {ratio},
    "kp_by_mag_mean": {dict(merged.groupby("mag_category")["kp"].mean().round(2))},
}}
""")