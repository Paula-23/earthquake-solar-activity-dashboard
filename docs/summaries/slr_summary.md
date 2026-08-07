# Solar Flare Dataset Summary

## Overview
- **Rows:** 2961
- **Columns:** 21
- **Categorical Columns:** id_flr, general_source_location, solar_flare_flux_class, submission_time, start_time_date, peak_time_date, end_time_date, submission_time_date, flare_class_letter, R_scale
- **Numerical Columns:** num_linked_events, start_time_hour_decimal, peak_time_hour_decimal, end_time_hour_decimal, submission_time_hour_decimal, flare_duration_minutes, flare_intensity_numeric

## Unique Values (Categorical)
- **id_flr**: 2961 unique values
- **general_source_location**: 4 unique values
- **solar_flare_flux_class**: 248 unique values
- **submission_time**: 2863 unique values
- **start_time_date**: 1170 unique values
- **peak_time_date**: 1174 unique values
- **end_time_date**: 1141 unique values
- **submission_time_date**: 1120 unique values
- **flare_class_letter**: 5 unique values
- **R_scale**: 3 unique values

## Categorical Details

### id_flr
- Unique values: 2961
- Top 5 values:
  - 2014-01-01T18:40:00-FLR-001: 1
  - 2014-01-02T02:24:00-FLR-001: 1
  - 2014-01-02T22:12:00-FLR-001: 1
  - 2014-01-03T12:41:00-FLR-001: 1
  - 2014-01-03T21:00:00-FLR-001: 1

### general_source_location
- Unique values: 4
- Top 5 values:
  - south-west: 1004
  - south-east: 739
  - north-west: 635
  - north-east: 583

### solar_flare_flux_class
- Unique values: 248
- Top 5 values:
  - M1.0: 310
  - M1.1: 236
  - M1.2: 196
  - M1.3: 162
  - M1.4: 142

### submission_time
- Unique values: 2863
- Top 5 values:
  - 2023-05-18 18:09:00+00:00: 5
  - 2023-07-12 11:28:00+00:00: 5
  - 2023-01-09 11:10:00+00:00: 4
  - 2024-07-10 12:35:00+00:00: 4
  - 2017-09-10 23:36:00+00:00: 3

### start_time_date
- Unique values: 1170
- Top 5 values:
  - 2024-12-29: 22
  - 2024-08-01: 21
  - 2024-05-09: 20
  - 2024-05-08: 18
  - 2024-11-06: 16

### peak_time_date
- Unique values: 1174
- Top 5 values:
  - 2024-12-29: 22
  - 2024-08-01: 21
  - 2024-05-09: 20
  - 2024-05-08: 18
  - 2024-12-30: 16

### end_time_date
- Unique values: 1141
- Top 5 values:
  - 2024-12-29: 22
  - 2024-08-01: 21
  - 2024-05-09: 20
  - 2024-05-08: 18
  - 2024-12-30: 16

### submission_time_date
- Unique values: 1120
- Top 5 values:
  - 2024-05-08: 21
  - 2024-08-02: 21
  - 2024-05-09: 19
  - 2024-05-12: 19
  - 2024-12-30: 19

### flare_class_letter
- Unique values: 5
- Top 5 values:
  - M: 2312
  - C: 489
  - X: 116
  - B: 43
  - A: 1

### R_scale
- Unique values: 3
- Top 5 values:
  - R1: 2104
  - R2: 208
  - R3: 116

## Category Combinations
- Columns used: solar_flare_flux_class, flare_class_letter, R_scale
- Unique combinations: 248

## Datetime Summary

### start_time
- Min: 2014-01-01 18:40:00+00:00
- Max: 2025-12-31 13:12:00+00:00
- Resolution: minute

### peak_time
- Min: 2014-01-01 18:52:00+00:00
- Max: 2025-12-31 13:51:00+00:00
- Resolution: minute

### end_time
- Min: 2014-01-01 19:03:00+00:00
- Max: 2025-12-31 14:11:00+00:00
- Resolution: minute

## Temporal Consistency
- Start ≤ Peak: 99.93%
- Peak ≤ End: 98.24%
