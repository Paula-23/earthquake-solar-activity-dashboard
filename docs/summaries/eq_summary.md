# Earthquake Dataset Summary

## Overview
- **Rows:** 335035
- **Columns:** 27
- **Categorical Columns:** id_eq, place, mag_type, source, start_time, updated_utc, state, eq_location, sources_list, source_category, month_name, day_name, year_month, geometry, country, continent
- **Numerical Columns:** mag, duration, longitude, latitude, depth_km, year, month, dayofweek, hour, index_right

## Unique Values (Categorical)
- **id_eq**: 335035 unique values
- **place**: 140753 unique values
- **mag_type**: 21 unique values
- **source**: 24 unique values
- **start_time**: 335017 unique values
- **updated_utc**: 123843 unique values
- **state**: 621 unique values
- **eq_location**: 11104 unique values
- **sources_list**: 833 unique values
- **source_category**: 1 unique values
- **month_name**: 12 unique values
- **day_name**: 7 unique values
- **year_month**: 144 unique values
- **geometry**: 333540 unique values
- **country**: 139 unique values
- **continent**: 9 unique values

## Categorical Details

### id_eq
- Unique values: 335035
- Top 5 values:
  - us6000kqqb: 1
  - us6000knzw: 1
  - us6000kqiw: 1
  - pr2023180001: 1
  - us6000kqiu: 1

### place
- Unique values: 140753
- Top 5 values:
  - South Sandwich Islands region: 5053
  - south of the Fiji Islands: 4163
  - Rat Islands, Aleutian Islands, Alaska: 3356
  - Kermadec Islands region: 2985
  - Fiji region: 2905

### mag_type
- Unique values: 21
- Top 5 values:
  - mb: 167967
  - ml: 107437
  - md: 28637
  - mww: 12126
  - Md: 7486

### source
- Unique values: 24
- Top 5 values:
  - usgs_eq_raw_S9: 19500
  - usgs_eq_raw_S10: 19500
  - usgs_eq_raw_S13: 17290
  - usgs_eq_raw_S24: 16077
  - usgs_eq_raw_S12: 14747

### start_time
- Unique values: 335017
- Top 5 values:
  - 2025-02-10 08:50:48.710: 2
  - 2021-02-27 18:59:25.296: 2
  - 2022-12-10 05:47:27.240: 2
  - 2020-02-09 21:39:14.140: 2
  - 2018-06-14 11:33:57.160: 2

### updated_utc
- Unique values: 123843
- Top 5 values:
  - 2025-10-17 22:51:42.040000+00:00: 1771
  - 2023-12-16 22:13:10.040000+00:00: 85
  - 2023-10-17 22:01:29.040000+00:00: 85
  - 2023-11-18 22:29:35.040000+00:00: 83
  - 2023-12-16 22:13:09.040000+00:00: 79

### state
- Unique values: 621
- Top 5 values:
  - Alaska: 65603
  - Puerto Rico: 20701
  - Indonesia: 19653
  - Hawaii: 16398
  - CA: 11991

### eq_location
- Unique values: 11104
- Top 5 values:
  - Volcano: 11239
  - Adak: 9622
  - Chiniak: 6132
  - Sand Point: 5315
  - South Sandwich Islands region: 5053

### sources_list
- Unique values: 833
- Top 5 values:
  - ['us']: 176718
  - ['ak', 'us']: 26108
  - ['pr']: 12433
  - ['ak', 'ak', 'us']: 11987
  - ['us', 'ak']: 10373

### source_category
- Unique values: 1
- Top 5 values:
  - Other_Regional: 335035

### month_name
- Unique values: 12
- Top 5 values:
  - Jul: 35282
  - Jan: 29326
  - Jun: 28888
  - Aug: 28767
  - May: 28340

### day_name
- Unique values: 7
- Top 5 values:
  - Tue: 48569
  - Sun: 48343
  - Mon: 48051
  - Sat: 47991
  - Fri: 47923

### year_month
- Unique values: 144
- Top 5 values:
  - 2018-06: 6509
  - 2018-07: 6253
  - 2019-07: 4368
  - 2020-01: 4250
  - 2025-07: 4158

### geometry
- Unique values: 333540
- Top 5 values:
  - POINT (-104.19 31.672): 5
  - POINT (-155.274166666667 19.3981666666667): 5
  - POINT (-155.274833333333 19.4153333333333): 5
  - POINT (-155.273166666667 19.3981666666667): 5
  - POINT (-155.262666666667 19.4093333333333): 5

### country
- Unique values: 139
- Top 5 values:
  - Ocean: 218646
  - United States of America: 65278
  - Chile: 4083
  - Indonesia: 3673
  - Puerto Rico: 3653

### continent
- Unique values: 9
- Top 5 values:
  - Ocean: 218646
  - North America: 75136
  - Asia: 20535
  - South America: 11674
  - Oceania: 4223

## Category Combinations
- Columns used: country, state, eq_location
- Unique combinations: 13213

## Datetime Summary

### start_time
- Min: 2014-01-01 00:01:16.610000
- Max: 2025-12-30 23:51:36.674000
- Resolution: microsecond

### updated_utc
- Min: 2014-01-13 13:44:20.715000+00:00
- Max: 2026-03-10 12:06:29.367000+00:00
- Resolution: microsecond

## Geospatial Summary
- Latitude precision (max decimals): 15
- Longitude precision (max decimals): 14
- Unique countries: 139
- Unique states: 621
- Unique continents: 9
- Unique coordinate pairs: 333540
