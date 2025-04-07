import pandas as pd
import requests
import os
import time
from slugify import slugify  # pip install python-slugify

# Create output directory
os.makedirs("gamelogs", exist_ok=True)

# Load player list
players_df = pd.read_csv("mlb_2025_player_ids.csv")

# Loop through each player
for idx, row in players_df.iterrows():
    player_id = row['id']
    name = row['name']
    slug_name = slugify(name.lower())
    output_path = f"gamelogs/{slug_name}_2025_gamelogs.csv"

    # Skip if already exists
    if os.path.exists(output_path):
        print(f"⚠️ Skipping existing: {name}")
        continue

    # API Request
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=gameLog&season=2025"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract gamelog
        splits = data['stats'][0].get('splits', [])
        if not splits:
            print(f"❌ No gamelogs for {name}")
            continue

        rows = []
        for game in splits:
            stat = game['stat']
            rows.append({
                'date': game['date'],
                'opponent': game['opponent']['name'],
                'atBats': stat.get('atBats', 0),
                'runs': stat.get('runs', 0),
                'hits': stat.get('hits', 0),
                'homeRuns': stat.get('homeRuns', 0),
                'rbi': stat.get('rbi', 0),
                'baseOnBalls': stat.get('baseOnBalls', 0),
                'strikeOuts': stat.get('strikeOuts', 0),
                'avg': stat.get('avg', '0.000'),
                'obp': stat.get('obp', '0.000'),
                'slg': stat.get('slg', '0.000'),
                'ops': stat.get('ops', '0.000'),
            })

        pd.DataFrame(rows).to_csv(output_path, index=False)
        print(f"✅ Saved {len(rows)} logs for {name}")

    except Exception as e:
        print(f"🚨 Error with {name}: {e}")

    time.sleep(0.3)  # be nice to the API
