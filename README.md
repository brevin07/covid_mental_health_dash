# COVID‑19 & Mental Health Dashboard

**Brevin Tating – CS150 Final Project (May 2025)**

An interactive, multi‑tab Dash application that visualizes how U.S. adult mental‑health symptoms (anxiety, depression, loss of interest, and excessive worry) tracked alongside the COVID‑19 pandemic (April 2020–October 2023). The dashboard also maps geographic disparities, shows symptom interrelationships, and highlights related economic and food‑security indicators.

---

## 🚀 Features

1. **Introduction Tab**  
   - Background context, thesis statement, data source overview, and user instructions.

2. **Dashboard Tab**  
   - **Symptom Toggles**: Checklist to show/hide any combination of the four symptom lines.  
   - **Time‑Series Chart**: Weekly mean symptom scores on a 1–4 scale, annotated with COVID‑19 milestones.  
   - **Symptom Heatmap**: Shows how symptoms are correlated to one another.

3. **Geography Tab**  
   - **Choropleth Map**: State‑by‑state weekly mean of a chosen symptom (default: anxiety).  
   - **Range Slider & Play Button**:  
     - Manual two‑handle slider to select any week range.  
     - Play/Animate button steps the upper bound week‑by‑week.  
   - **Context Card**: Markdown explanation of the map’s purpose.


## 📁 File Breakdown

Below is a summary of each file in this project and how it fits into the overall dashboard:

| Filename                   | Purpose                                                                                           |
|----------------------------|---------------------------------------------------------------------------------------------------|
| **`hps_combined.parquet`** | The cleaned, combined Household Pulse Survey data (waves 1–63). Loaded at startup by `config.py`. |
| **`weekly_means.parquet`** | Written out by `config.py`—contains pre‑computed weekly means of the four symptom variables.      |
| **`config.py`**            | • Loads and cleans the original data, excludes skip codes                                         |

                               • Computes correlations (`corr_with_time`) and extremes (`extremes_df`)  
                               • Prepares long‑form tables (`time_long`)  
                               • Builds state‑level weekly data (`state_week`)  
                               • Defines static milestone map (`event_weeks`), and `heatmap_fig` |
| **`cards.py`**               | Factory functions (and pre‑built card instances) that return styled Bootstrap cards:  
                               • `info_card` (overview & navigation)  
                               • `timeline_card` (intro to the time‑series chart)  
                               • `heatmap_card` (correlation heatmap + explanation)  
                               • `geography_card` (map controls + explanation)  
| **`dashboard.py`**           | The heart of the app:  
                               • Instantiates the Dash app and applies a Bootstrap theme  
                               • Defines the four `dcc.Tabs` (“Introduction,” “Timeline,” “Geography,” “Correlation”)  
                               • Lays out each tab by composing cards and `dcc.Graph` placeholders  
                               • Registers all callbacks for:  
                                 – Time‑series chart filtering & annotation  
                                 – Choropleth map updates & play/animate logic  
                                 – Heatmap of symptom correlation|
| **`README.md`**              | This file—provides installation instructions, project overview, data pipeline details,  
                               file descriptions, and key learnings.                                       |

Each file has a single, well‑defined responsibility—data prep in **`config.py`**, UI building blocks in **`cards.py`**, and overall layout + interactivity in **`dashboard.py`**—making the code modular, maintainable, and easy to extend.  

## 🧠 Key Learnings

- **Expectation vs. Reality:** I went into this project expecting large, sustained spikes in anxiety and depression perfectly mirroring COVID‑19 waves.  
- **Actual Trends:** The data showed only modest, short‑lived peaks—smaller and briefer than anticipated.  
- **Lingering Impact:** Even when symptoms dipped after each surge, they never returned to those very low “baseline” levels, suggesting a lasting mental‑health burden beyond the immediate waves.  

## Data Google Drive Link

https://drive.google.com/drive/folders/141tDVTYiOyvT1Gf5x5cJ43yfgQmYqe9L?usp=drive_link

- After downloading this file, please place it in the main repo folder to get the dashboard to work.
---

