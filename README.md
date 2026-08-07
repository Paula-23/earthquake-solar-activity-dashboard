## Capstone Project Setup Documentation 
Paula Herrera 260221. 

### Data Science Fictional Case

A professional scientific institute is interested in organizing different sources of earthquake and solar activity data on their website in the form of a dynamic dashboard mimicking the discovery and inmersive experience of some contemporary museums. The objective of the dashboard is to enable the users to explore earthquake data and contrast it to solar flare activity in the magnetosphere. 

The following Streamlit App is the result of fictional case I invented for myself within the scope of mz data analytics bootcamp. I took the role of a data scientist consultant and developed what I imagine could be a first minimal version of such dashboard and museum-like dashboard.

The principal motivation behind the project was initially to explore the possible link between solar events and earthquakes worlwide. This is one of the most contemporary debates in the geosciences which was already explored in ancient cultures before ours. Now we have the tools-sensors to record and estimate these natural phenomena with precision and as a result have large amounts of granular and by the second data. 

The project is also a great opportunity for me to showcase the whole suit of data management skills and taks I am capable of as a analyst, consultant and researcher. The project demonstrates my ability to 
    (1) identify, extract, transform and load original data sourced from publicly-available scientific APIs as the result of real-time sensor technology and satellites; 
    (2) clean, handle missing values, and create basic summaries;
    (3) bring together different datasets with different formats together;
    (4) select and conduct specific descriptive & advanced statistical analyses;
    (5) handle complex granular geospatial and timestamp variables;
    (6) generate beautiful, colorful and enticing visualizations;
    (7) go beyond static results and create functional dashboards via streamlit.

### Technical Project Overview

This document describes the setup of the da_capstone project, including:

1. Folder structure.   
2. Python environment (Conda).   
3. Git/GitHub setup with SSH.   
4. VS Code configuration.   
5. Tools installed on macOS.   

#### 1. Folder Structure

All projects live in ~/Projects/da_capstone.

_1.1. Folder structure:_

````
. 📁 directory
|____README.md
|____requirements.txt
|____docs
| |____figures
| |____summaries # markdown summary files of datasets
| |____documentation.md
| |____presentation
| | |____Herrera_EDA_14.04.26.pdf
|____data
| |____raw (39 json files) # Original API data
| |____preprocessed # Preprocessed (falttened jsons)
| |____interim # tidied datasets
| |____processed # Ready datasets for analysis
| | |____nasa_cme_df.csv
| | |____usgs_eq_df.csv
| | |____nasa_flr_df.csv
| | |____nasa_gst_df.csv
| | |____gfz_kp_df.csv
| |____geospatial # tectonic_plates data + goepolitical boarders/labels
| | |____tectonic_plates (.dbf, .sbx, .shp, .json, .sbn, .prj)
| | |____ne_110m_admin_0_countries (.dbf, .sbx, .shp, .cpg, .sbn, .prj, .txt)
|____notebooks
| |____01_USGS_Earthquakes_data
| | |____01_eq_data_collection.ipynb
| | |____02_eq_json_flattening.ipynb
| | |____03_eq_csv_tidying.ipynb
| | |____04_eq_dataset_summary.ipynb
| | |____05_earthquake_eda.ipynb
| |____02_GFZ_kpindex_data
| | |____01_jfz_data_collection.ipynb
| | |____02_jfz_data_tidying.ipynb
| | |____03_jfz_data_eda.ipynb
| | |____04_jfz_dataset_summary_wp.ipynb
| |____03_NASA_SolarActivity_data
| | |____01_sa_data_collection.ipynb
| | |____02_sa_json_flattening.ipynb
| | |____03_sa_csv_tidying.ipynb
| | |____04_sa_dataset_summary.ipynb
| | |____05_slr_eda.ipynb
| |____04_correlation_analysis.ipynb
| | |____findings.py
| | |____05_hypothesis_testing.ipynb
| | |____09_correlation_analysis.ipynb
|____src
| |____homepage.py 
| |____pages
| |____style.py # Clean Separation of Concerns
| |____imports.py # Centralized Dependency Management
| |______init__.py
| |______pycache__
| |____notebook_setup.py
├─ .gitignore
├─ .git/
````

_1.2. File naming conventions:_

Raw: raw_<dataset>.csv.   
Cleaned: <dataset>_cleaned.csv.   
Master: master_<dataset1>_<dataset2>.csv. 

#### 2. Python Environment (Conda)

_2.1. Installation of Miniconda (user-specific):_. 

````
cd ~/opt. 
bash Miniconda3-latest-MacOSX-x86_64.sh. 
conda activate base. 
````

_2.2. Project-specific environment:_

````
conda create -n da_capstone python=3.13. 
conda activate da_capstone. 
conda install pandas numpy matplotlib seaborn scikit-learn jupyter dash. 
conda env export > environment.yml
````

_2.3. Recreate environment:_
````
conda env create -f environment.yml. 
````

### 3. Git & GitHub Setup

_3.1. Install Git (if not already):_  
````
git --version
xcode-select --install  # macOS command line tools
````

_3.2. SSH Key for GitHub:_.  
````
ssh-keygen -t rsa -b 4096 -C "email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
pbcopy < ~/.ssh/id_rsa.pub
````

Paste into GitHub → Settings → SSH and GPG keys → New SSH key

_3.3. Test SSH connection:_.  
````
ssh -T git@github.com
````

_3.4. Clone repo:_.  
````
cd ~/Projects
git clone git@github.com:Username/da_capstone.git
cd da_capstone
````

_3.5. Connect Local Repo to GitHub_.  
```
git remote add origin https://github.com/yourusername/repository-name.git.  
git branch -M main.  
git push -u origin main.  
```

_3.6. Typical Git workflow:_. 
````
git pull
git add .
git commit -m "Your commit message"
git push
````

### 4. VS Code Configuration

_4.1. Open project folder:_.  
````
code ~/Projects/da_capstone.  
Select Python interpreter → Conda environment da_capstone
````

Use Explorer & Source Control panes for workflow

### 5. macOS Tools

### 🛠️ macOS Environment Setup

For macOS users looking to run or inspect this project locally, utilize the commands below:

_5.1. Homebrew (package manager):_.  
  ```bash
  /bin/bash -c "\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

_5.2. Directory Visualization (`tree` utility):_
  ```bash
  brew install tree && tree -L 2
  ```
_5.3. Read `requirements.txt` for full list of exact project tools:_
For the complete framework of data analysis libraries, Streamlit dependencies, and versions, please review the `requirements.txt` file.

### 7. Project Workflow
Raw Data → Cleaned Data → Master Dataset → Notebooks → Analysis → Reports/Dashboard

- Pull latest changes: git pull
- Activate environment: conda activate da_capstone
- Work in src/ or notebooks/
- Stage & commit: git add . → git commit -m "message" → git push
- Save processed data in data/master/
- Save plots, dashboards, slides in docs/

### 8. API Key setups
https://api.nasa.gov/
