# Solar Activity and Earthquakes: Coincidence or Trigger? 🚀

🌈⃤. Paula Herrera  
    17.02.2026

---------

## 1. My Working Topic 🕵️‍♂️

#### **1.1 Research Narrative**  
 Ancient Mesoamerican cultures such as the Aztecs believed celestial phenomena influenced events on Earth. While these ideas were mythological, they raise one of the most intriguing modern scientific questions: Is there any observable temporal or statistical relationship between solar flare activity and global earthquake frequency or magnitude?

#### **1.2. Research Context**   
A recent 2020 scientific research hypothesis proposes that solar storms may disturb the ionosphere in ways that induce electrical currents in the Earth’s crust, potentially “nudging” already stressed tectonic faults and triggering seismic activity.

Literature Review:   
https://www.nature.com/articles/s41598-020-67860-3
https://www.mdpi.com/2073-4433/13/7/1131 
https://www.sciencedirect.com/science/article/pii/S2211714825000901 
https://link.springer.com/article/10.1007/s44195-023-00042-6
https://www.scirp.org/journal/paperinformation?paperid=5319 

#### **1.3. Research Hypothesis**  
Building on this premise, I aim to investigate whether such relationships can be empirically observed using publicly available data from NASA and USGS. Through descriptive and time-series analysis of solar and seismic indicators, I will explore not only potential correlations between heightened solar activity and earthquakes, but also the less examined hypothesis that periods of low or absent solar activity may be associated with increased seismic events. This approach seeks to critically assess both the presence and absence of solar forcing as potential triggers within complex geophysical systems.

#### **1.4 Research Purpose**   
This is a curiosity-driven project with a twofold purpose:

- First, to showcase my preprocessing and exploratory data analyticals skills, particularly in handling temporal (timestamp) and geospatial variables, as well as in visualizing information in a dynamic dashboard.

- Second, to explore one of the most recent hypotheses in geophysics concerning the relationship between space weather and seismic activity.

#### **1.5 Research Relevance**  
By examining how solar phenomena may be associated with processes within the Earth’s environment, this project also aims to highlight the broader relevance of such analyses for population-based services and logistics, including emergency preparedness, earthquake risk assessment, and environmental health intelligence.

#### **1.6 Research Motivation**   
Exploring space weather is inherently fascinating, not only because of its scientific complexity but also because it represents a rare domain where high-quality, real-world data are openly accessible. The availability of public datasets from organizations such as NASA and USGS is particularly unique, as few global public data commons offer this level of granularity, continuity, and accessibility for independent analysis.   

------
## 2. My Data Sources 📥

### 2.1 Source 1: USGS Earthquake Catalog (ComCat)

| Theme                  | Seismic Activity on Earth                                  |
|------------------------|---------------------------------------------------         |
| Provider               | U.S. Geological Survey (USGS)                              |
| Endpoint               | [https://earthquake.usgs.gov](https://earthquake.usgs.gov) |
| Access Method          | RESTful HTTPS GET                                          |
| Data Format            | GeoJSON (Primary)                                          |
| Authentication         | None required (Open Access)                                |
| Key Variables          | starttime, endtime, minmagnitude, latitude, longitude      |


**Note on Data Collection**.  
The USGS collects earthquake data using a global network of seismometers, which are highly sensitive instruments that detect ground motion caused by seismic waves. These seismometers are part of systems like the Advanced National Seismic System (ANSS) in the U.S. and the Global Seismographic Network (GSN) worldwide. When an earthquake occurs, the seismic waves are recorded by multiple stations, and the data is rapidly transmitted to the National Earthquake Information Center (NEIC) in Golden, Colorado. There, automated systems and seismologists analyze the waveforms to determine the earthquake’s location, depth, magnitude, and other key parameters.

### 2.2 Source 2: NASA DONKI   

| Theme                  | Solar Activity in Space                                    |
|------------------------|---------------------------------------------------         |
| Provider               | National Aeronautics and Space Administration (NASA)       |
| Endpoint               | [https://api.nasa.gov](https://api.nasa.gov)               |
| Access Method          | RESTful HTTPS GET                                          |
| Data Format            | JSON                                                       |
| Authentication         | API Key required with personal account and purpose of use  |
| Key Variables          | startDate, endDate                                         |


**Note on Data Collection**  
NASA’s DONKI system collects solar flare data primarily using space-based instruments, such as those on the GOES (Geostationary Operational Environmental Satellites) and SDO (Solar Dynamics Observatory) satellites. These instruments measure X-ray and extreme ultraviolet (EUV) radiation emitted during solar flares. The data is analyzed by the Moon-to-Mars Space Weather Analysis Office and other teams, who catalog events like solar flares, coronal mass ejections, and related space weather phenomena. 


--------
### 3. My Working Datasets 🗂️ (after preprocessing)

----

#### Earthquake Data (Accessed: 2026-03-11)
<!-- Include the generated summary -->
[View detailed summary](summaries/eq_summary.md)



#### Solar Flare Data (Accessed: 2026-02-22)
<!-- Include the generated summary -->
[View detailed summary](summaries/slr_summary.md)




