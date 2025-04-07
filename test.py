import requests
import pandas as pd

# Aaron Judge's MLB ID
player_id = 592450
season = 2025
url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=gameLog&season={season}"

# Send request
response = requests.get(url)
data = response.json()

# Extract gamelogs
game_logs = data['stats'][0]['splits']

# Parse into structured rows
rows = []
for game in game_logs:
    stat = game['stat']
    row = {
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
    }
    rows.append(row)

# Convert to DataFrame
df = pd.DataFrame(rows)

# Save to CSV
df.to_csv('aaron_judge_2025_gamelogs.csv', index=False)
print("✅ Gamelogs saved to 'aaron_judge_2025_gamelogs.csv'")
