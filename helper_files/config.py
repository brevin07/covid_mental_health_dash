import pandas as pd

# 1) Load the data (parquet preferred; CSV fallback)

df = pd.read_parquet("../data/cleaned_data/hps_combined.parquet")


# 2) Define variables and remove skip codes (–88, –99)
variables = ["ANXIOUS", "DOWN", "INTEREST", "WORRY"]
df_clean = df.loc[~df[variables].isin([-88, -99]).any(axis=1)].copy()

# 3) Dataset #1: time_metrics — weekly means for each symptom variable
time_metrics = (
    df_clean
    .groupby("WEEK")[variables]
    .mean()
    .reset_index()
)


# 4) Dataset #2: corr_with_time — correlation of each variable with WEEK (timeline proxy)
corr_with_time = (
    time_metrics
    .corr()
    .loc["WEEK", variables]
    .reset_index(name="corr_with_week")
    .rename(columns={"index": "variable"})
)

# 5) Dataset #3: extremes_df — min/max week and value for each variable
extremes = []
for var in variables:
    ser = time_metrics[var]
    extremes.append({
        "variable": var,
        "min_week": int(time_metrics.loc[ser.idxmin(), "WEEK"]),
        "min_value": ser.min(),
        "max_week": int(time_metrics.loc[ser.idxmax(), "WEEK"]),
        "max_value": ser.max()
    })
extremes_df = pd.DataFrame(extremes)

# Example outputs:
print("=== time_metrics ===")
print(time_metrics.head())
print("\n=== corr_with_time ===")
print(corr_with_time)
print("\n=== extremes_df ===")
print(extremes_df)

# Melt to long format for easy filtering
time_long = time_metrics.melt(
    id_vars="WEEK",
    value_vars=variables,
    var_name="Symptom",
    value_name="MeanScore"
)

# Static pandemic milestones (mapped to HPS WEEK numbers)
event_weeks = {
    1:  "HPS Begins",
    10: "Summer Surge",
    36: "Pfizer EUA",
    43: "J&J EUA",
    47: "All Adults Eligible",
    52: "Delta Dominant",
    49: "Omicron Emerges",
}

# 6) Overall averages (for KPI cards)
avg_metrics = time_metrics[variables].mean().to_dict()

# 7) Peak weeks (for KPI cards)
peak_info = {}
for var in variables:
    row = extremes_df.query("variable == @var").iloc[0]
    peak_info[var] = {
        "max_value": row["max_value"],
        "max_week": row["max_week"],
        "min_value": row["min_value"],
        "min_week": row["min_week"]
    }


import plotly.express as px

heatmap_fig = px.imshow(
    time_metrics[variables].corr(),
    text_auto=".2f",
    labels={"x":"Symptom", "y":"Symptom"},
    title="Correlation Between Symptoms"
)
heatmap_fig.update_layout(margin=dict(l=40,r=20,t=40,b=40))

# ─── 1) Build state_week DataFrame ──────────────────────────────────────────────
# FIPS → USPS mapping
fips_to_abbrev = {
    1: "AL",  2: "AK",  4: "AZ",  5: "AR",  6: "CA",
    8: "CO",  9: "CT", 10: "DE", 11: "DC", 12: "FL",
   13: "GA", 15: "HI", 16: "ID", 17: "IL", 18: "IN",
   19: "IA", 20: "KS", 21: "KY", 22: "LA", 23: "ME",
   24: "MD", 25: "MA", 26: "MI", 27: "MN", 28: "MS",
   29: "MO", 30: "MT", 31: "NE", 32: "NV", 33: "NH",
   34: "NJ", 35: "NM", 36: "NY", 37: "NC", 38: "ND",
   39: "OH", 40: "OK", 41: "OR", 42: "PA", 44: "RI",
   45: "SC", 46: "SD", 47: "TN", 48: "TX", 49: "UT",
   50: "VT", 51: "VA", 53: "WA", 54: "WV", 55: "WI",
   56: "WY"
}

# Map each respondent’s FIPS to USPS, then compute weekly means by state
df_geo = df_clean.assign(
    state_abbrev = df_clean["EST_ST"].map(fips_to_abbrev)
)

state_week = (
    df_geo
    .groupby(["state_abbrev", "WEEK"])[variables]
    .mean()
    .reset_index()
)

# config.py

# … your existing imports and code …

# 6) New indicators to plot over time

df2 = pd.read_parquet("../data/cleaned_data/hps_.parquet")

misc_var = "CURFOODSUF"

df_clean2 = df2.loc[~df2[misc_var].isin([-88, -99])].copy()

# compute weekly means for each
misc_metrics = (
    df_clean2
      .groupby("WEEK")[misc_var]
      .mean()
      .reset_index()
)


