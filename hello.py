from preswald import connect, get_df
from preswald import query
from preswald import table, text
from preswald import plotly
from preswald import sidebar

import plotly.express as px
import pandas as pd
import re

sidebar(
    defaultopen=True,
    name="PicklePaddle Insights"
)


# 1. Load the dataset
my_dataset = "pickleball_paddles"
connect()
df = get_df(my_dataset)

# 2. Query or manipulate the data
sql = f'SELECT * FROM {my_dataset} WHERE CAST("Price" AS DOUBLE) > 100'
filtered_df = query(sql, my_dataset)

# Parse and clean weight column
def parse_weight(w):
    if pd.isna(w):
        return None
    w = str(w).replace('"', '').replace('oz', '').strip()
    if '-' in w:
        try:
            parts = re.findall(r"[\d.]+", w)
            return (float(parts[0]) + float(parts[1])) / 2
        except:
            return None
    else:
        try:
            return float(w)
        except:
            return None
            
# Parse and clean swing and twist weight column
def parse_twist_swing_weight(w):
    if pd.isna(w):
        return None
    w = str(w).replace('g', '').strip()
    try:
        return float(w)
    except:
        return None

# Parse and clean RPM column
def parse_rpm(rpm):
    if pd.isna(rpm):
        return None
    rpm = str(rpm).replace('RPM', '').strip()
    try:
        return float(rpm)
    except:
        return None

filtered_df["Weight (oz)"] = filtered_df["Weight"].apply(parse_weight)
filtered_df["Swing Weight (g)"] = filtered_df["Swing weight"].apply(parse_twist_swing_weight)
filtered_df["Twist Weight (g)"] = filtered_df["Twist weight"].apply(parse_twist_swing_weight)
filtered_df["RPM"] = filtered_df["RPM"].apply(parse_rpm)

# Drop invalid values
filtered_df = filtered_df.dropna(subset=["Weight (oz)"])
filtered_df = filtered_df.dropna(subset=["Swing Weight (g)"])
filtered_df = filtered_df.dropna(subset=["Twist Weight (g)"])
filtered_df = filtered_df.dropna(subset=["RPM"])

# Sort price ascending
filtered_df = filtered_df.sort_values("Price", ascending=True)

# 3. Build an interactive UI
text("# PicklePaddle Insights")
important_cols = ["Paddle", "Price", "Weight (oz)", "Swing Weight (g)", "Twist Weight (g)", "RPM"]
table(filtered_df[important_cols], title="Filtered Paddle Data")

# 4.1 Create a visualization for Price vs Weight
fig = px.scatter(
    filtered_df,
    x="Weight (oz)",
    y="Price",
    color="Paddle Tier",
    hover_data=["Paddle", "Company"],
    title="Price vs Weight of Paddles (by Tier)"
)
text("## Price vs Paddle Weight Analysis")
plotly(fig)

# 4.2 Create a visualization for Price vs Swing Weight
fig2 = px.scatter(
    filtered_df,
    x="Swing Weight (g)",
    y="Price",
    color="Paddle Tier",
    hover_data=["Paddle", "Company"],
    title="Price vs Swing Weight of Paddles (by Tier)"
)
text("## Price vs Swing Weight Analysis")
plotly(fig2)

# 4.3 Create a visualization for Price vs Twist Weight
fig3 = px.scatter(
    filtered_df,
    x="Twist Weight (g)",
    y="Price",
    color="Paddle Tier",
    hover_data=["Paddle", "Company"],
    title="Price vs Twist Weight of Paddles (by Tier)"
)
text("## Price vs Twist Weight Analysis")
plotly(fig3)

# 4.4 Create a visualization for Price vs RPM
fig4 = px.scatter(
    filtered_df,
    x="RPM",
    y="Price",
    color="Paddle Tier",
    hover_data=["Paddle", "Company"],
    title="Price vs RPM of Paddles (by Tier)"
)
text("## Price vs RPM Analysis")
plotly(fig4)

