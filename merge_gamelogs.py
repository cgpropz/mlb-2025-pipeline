import pandas as pd
import os

gamelogs_dir = "gamelogs"
all_data = []

# Loop through all .csv files in the gamelogs folder
for file in os.listdir(gamelogs_dir):
    if file.endswith("_2025_gamelogs.csv"):
        filepath = os.path.join(gamelogs_dir, file)
        try:
            df = pd.read_csv(filepath)
            # Extract player name from filename
            player_name = file.replace("_2025_gamelogs.csv", "").replace("_", " ").title()
            df.insert(0, "player_name", player_name)
            all_data.append(df)
        except Exception as e:
            print(f"❌ Failed reading {file}: {e}")

# Merge and save
if all_data:
    merged_df = pd.concat(all_data, ignore_index=True)
    merged_df.to_csv("all_2025_gamelogs.csv", index=False)
    print(f"✅ Merged {len(all_data)} players into 'all_2025_gamelogs.csv'")
else:
    print("⚠️ No gamelog files found!")
