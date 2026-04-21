import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("weather_tokyo_data.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Clean + convert numeric values safely
for col in ["year", "day", "temperature", "humidity", "atmospheric pressure"]:
    df[col] = df[col].astype(str).str.replace(r"[^0-9\-\.]", "", regex=True)
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Drop invalid rows
df = df.dropna(subset=["year", "day", "temperature"])

if df.empty:
    print("❌ No valid data after cleaning")
    exit()

# ----------------------------
# 1. OVERALL AVERAGE
# ----------------------------
print("Average Temperature:", df["temperature"].mean())

# ----------------------------
# 2. HOTTEST & COLDEST
# ----------------------------
hottest = df.loc[df["temperature"].idxmax()]
coldest = df.loc[df["temperature"].idxmin()]

print("\nHottest:", hottest["temperature"])
print("Coldest:", coldest["temperature"])

# ----------------------------
# 3. TEMPERATURE TREND
# ----------------------------
df = df.sort_values(by=["year", "day"])

plt.figure(figsize=(12,6))
plt.plot(range(len(df)), df["temperature"], color="orange")

plt.title("Temperature Trend Over Time")
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.grid(True)
plt.tight_layout()
plt.show()

# ----------------------------
# 4. MONTHLY AVERAGE (BAR CHART)
# ----------------------------
df["Month"] = ((df["day"] - 1) % 360) // 30 + 1

monthly_avg = df.groupby("Month")["temperature"].mean()

plt.figure(figsize=(10,5))
bars = plt.bar(monthly_avg.index, monthly_avg.values, color="skyblue")

plt.title("Monthly Average Temperature")
plt.xlabel("Month")
plt.ylabel("Temperature (°C)")
plt.grid(axis="y", linestyle="--", alpha=0.6)

plt.bar_label(bars, fmt="%.2f")
plt.tight_layout()
plt.show()

# ----------------------------
# 5. SEASONS (LINE PLOT - FIXED)
# ----------------------------
def get_season(day):
    if day <= 90:
        return "Winter"
    elif day <= 180:
        return "Spring"
    elif day <= 270:
        return "Summer"
    else:
        return "Fall"

df["Season"] = df["day"].apply(get_season)

season_avg = df.groupby("Season")["temperature"].mean()

print("\nSeasonal Average Temperature:")
print(season_avg)

# Order seasons correctly for line plot
season_order = ["Winter", "Spring", "Summer", "Fall"]
season_avg = season_avg.reindex(season_order)

plt.figure(figsize=(10,6))

plt.plot(season_avg.index, season_avg.values,
         marker="o", linestyle="-", color="green")

plt.title("Average Temperature by Season")
plt.xlabel("Season")
plt.ylabel("Temperature (°C)")
plt.grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.show()