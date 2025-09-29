# Task 4 - Traffic Accident Analysis (US Accidents dataset)
# Analyze patterns related to road conditions, weather, and time of day.
# Visualize accident hotspots and contributing factors.
# Source: https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Configuration
# -----------------------------
# Get the parent directory (task 4)
script_dir = os.path.dirname(os.path.abspath(__file__))

FILE_PATH = "US_Accidents_March23.csv"   # Ensure this file is in the task 4 folder
SAMPLE_N = 200_000
CHUNK_SIZE = 100_000

# Output files in parent (task 4) directory
OUTPUT_CLEANED = os.path.join(script_dir, "task4_sampled_cleaned.csv")
OUT_HOUR = os.path.join(script_dir, "accidents_by_hour.png")
OUT_DAY = os.path.join(script_dir, "accidents_by_dayofweek.png")
OUT_WEATHER = os.path.join(script_dir, "top_weather_conditions.png")
OUT_HOTSPOT = os.path.join(script_dir, "accident_hotspots_kde.png")
OUT_ROAD = os.path.join(script_dir, "road_condition_counts.png")


# -----------------------------
# Helper: read sample from big csv using chunks
# -----------------------------
def sample_from_large_csv(file_path, sample_n=SAMPLE_N, chunk_size=CHUNK_SIZE, random_state=42):
    """
    Read CSV in chunks and accumulate rows until sample_n reached.
    This keeps memory usage controlled.
    """
    collected = []
    collected_n = 0
    rng = np.random.default_rng(random_state)

    for chunk in pd.read_csv(file_path, chunksize=chunk_size, low_memory=True):
        if chunk.empty:
            continue
        if collected_n >= sample_n:
            break
        remaining = sample_n - collected_n
        if len(chunk) <= remaining:
            take = chunk.sample(frac=1.0, random_state=(random_state + collected_n))
            collected.append(take)
            collected_n += len(take)
        else:
            take = chunk.sample(n=remaining, random_state=(random_state + collected_n))
            collected.append(take)
            collected_n += len(take)
            break

    if len(collected) == 0:
        raise RuntimeError("No data read from file. Check file path / file integrity.")
    result = pd.concat(collected, ignore_index=True)
    if len(result) > sample_n:
        result = result.sample(n=sample_n, random_state=random_state).reset_index(drop=True)
    return result

# -----------------------------
# Main processing
# -----------------------------
def main():
    # Ensure file path is absolute (robust to working directory)
    abs_file_path = os.path.join(script_dir, FILE_PATH)
    if not os.path.exists(abs_file_path):
        print(f"ERROR: File not found: {abs_file_path}")
        return

    print("Loading a sampled subset from the large CSV (this may take a while)...")
    try:
        df = sample_from_large_csv(abs_file_path, sample_n=SAMPLE_N, chunk_size=CHUNK_SIZE)
    except Exception as e:
        print("Error during sampling:", e)
        return

    print(f"Sampled dataframe shape: {df.shape}")
    print("Columns available:", list(df.columns)[:40])

    # Normalize column names to lowercase for easier access
    df.columns = [c.strip() for c in df.columns]
    cols_lower = {c.lower(): c for c in df.columns}  # map lowercase -> original

    def col_name(key):
        return cols_lower.get(key.lower())

    start_time_col = col_name("start_time")
    lat_col = col_name("start_lat")
    lng_col = col_name("start_lng")
    weather_col = col_name("weather_condition")
    road_col = col_name("road_condition") or col_name("road_conditions") or col_name("road_surface_conditions")

    # -----------------------------
    # Parse start time -> hour, day of week
    # -----------------------------
    if start_time_col is not None:
        print("Parsing start times...")
        try:
            df['start_time_parsed'] = pd.to_datetime(df[start_time_col], errors='coerce')
        except Exception:
            df['start_time_parsed'] = pd.to_datetime(df[start_time_col].str.slice(0,19), errors='coerce')
        df['hour'] = df['start_time_parsed'].dt.hour
        df['day_of_week'] = df['start_time_parsed'].dt.day_name()
    else:
        print("Warning: Start time column not found. Some time-based analysis will be skipped.")

    # -----------------------------
    # Clean lat/lng
    # -----------------------------
    if lat_col is not None and lng_col is not None:
        df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
        df[lng_col] = pd.to_numeric(df[lng_col], errors='coerce')
    else:
        print("Warning: Latitude/Longitude columns not found. Hotspot mapping will be skipped.")

    # -----------------------------
    # Clean weather column
    # -----------------------------
    if weather_col is not None:
        df[weather_col] = df[weather_col].astype(str).replace('nan', np.nan)
        df['weather_norm'] = df[weather_col].str.lower().str.strip()
    else:
        print("Warning: Weather column not found. Weather-based analysis will be skipped.")

    # -----------------------------
    # Clean road condition column
    # -----------------------------
    if road_col is not None:
        df[road_col] = df[road_col].astype(str).replace('nan', np.nan)
        df['road_norm'] = df[road_col].str.lower().str.strip()
    else:
        print("Warning: Road condition column not found. Road condition analysis will be skipped.")

    # -----------------------------
    # Save cleaned sample
    # -----------------------------
    cleaned = df.copy()
    if lat_col and lng_col:
        cleaned = cleaned[(cleaned[lat_col].between(-90, 90)) & (cleaned[lng_col].between(-180, 180))]
    cleaned.to_csv(OUTPUT_CLEANED, index=False)
    print(f"Saved cleaned sample to {OUTPUT_CLEANED}")

    sns.set_style("whitegrid")

    # -----------------------------
    # Plot: accidents by hour
    # -----------------------------
    if 'hour' in cleaned.columns:
        print("Plotting accidents by hour...")
        hour_counts = cleaned['hour'].value_counts().sort_index()
        plt.figure(figsize=(10,5))
        sns.barplot(x=hour_counts.index, y=hour_counts.values, palette="crest")
        plt.title("Accidents by Hour of Day")
        plt.xlabel("Hour (0-23)")
        plt.ylabel("Number of Accidents (sampled)")
        plt.xticks(range(0,24))
        plt.savefig(OUT_HOUR, bbox_inches='tight')
        plt.close()
        print(f"Saved {OUT_HOUR}")
    else:
        print("Skipping hour plot (no hour data).")

    # -----------------------------
    # Plot: accidents by day of week
    # -----------------------------
    if 'day_of_week' in cleaned.columns:
        print("Plotting accidents by day of week...")
        days_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        day_counts = cleaned['day_of_week'].value_counts().reindex(days_order).fillna(0)
        plt.figure(figsize=(8,5))
        sns.barplot(x=day_counts.index, y=day_counts.values, palette="viridis")
        plt.title("Accidents by Day of Week")
        plt.xlabel("Day of Week")
        plt.ylabel("Number of Accidents (sampled)")
        plt.xticks(rotation=30)
        plt.savefig(OUT_DAY, bbox_inches='tight')
        plt.close()
        print(f"Saved {OUT_DAY}")
    else:
        print("Skipping day-of-week plot (no start time).")

    # -----------------------------
    # Plot: top weather conditions
    # -----------------------------
    if 'weather_norm' in cleaned.columns:
        print("Plotting top weather conditions...")
        top_weather = cleaned['weather_norm'].value_counts().head(15)
        plt.figure(figsize=(10,7))
        sns.barplot(y=top_weather.index, x=top_weather.values, palette="Blues_r")
        plt.xlabel("Number of Accidents (sampled)")
        plt.title("Top Weather Conditions at Accident Time (sampled)")
        plt.savefig(OUT_WEATHER, bbox_inches='tight')
        plt.close()
        print(f"Saved {OUT_WEATHER}")
    else:
        print("Skipping weather plot (no weather column).")

    # -----------------------------
    # Plot: top road conditions
    # -----------------------------
    if 'road_norm' in cleaned.columns:
        print("Plotting top road conditions...")
        top_road = cleaned['road_norm'].value_counts().head(15)
        plt.figure(figsize=(10,6))
        sns.barplot(y=top_road.index, x=top_road.values, palette="mako")
        plt.xlabel("Number of Accidents (sampled)")
        plt.title("Top Road Conditions (sampled)")
        plt.savefig(OUT_ROAD, bbox_inches='tight')
        plt.close()
        print(f"Saved {OUT_ROAD}")
    else:
        print("No dedicated road condition column found — skipping.")

    # -----------------------------
    # Plot: Hotspots using KDE over lat/lng
    # -----------------------------
    if lat_col is not None and lng_col is not None and (cleaned.shape[0] > 100):
        print("Plotting accident hotspots (KDE) ...")
        pts = cleaned[[lat_col, lng_col]].dropna()
        if len(pts) > 100000:
            pts = pts.sample(n=100000, random_state=42)
        plt.figure(figsize=(8,8))
        try:
            plt.hexbin(pts[lng_col], pts[lat_col], gridsize=200, cmap='inferno', mincnt=1)
            plt.colorbar(label='Counts (hexbin)')
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")
            plt.title("Accident Hotspots (hexbin, sampled)")
        except Exception:
            sns.kdeplot(x=pts[lng_col], y=pts[lat_col], fill=True, thresh=0.05)
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")
            plt.title("Accident Hotspots (KDE, sampled)")
        plt.savefig(OUT_HOTSPOT, bbox_inches='tight')
        plt.close()
        print(f"Saved {OUT_HOTSPOT}")
    else:
        print("Skipping hotspots (no lat/lng or too few points).")

    print("All tasks completed. Plots and cleaned CSV saved in current folder.")

if __name__ == "__main__":
    main()