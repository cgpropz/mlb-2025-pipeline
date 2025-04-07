import requests
import pandas as pd

# List of all MLB team IDs
team_ids = [
    109, 144, 110, 111, 112, 113, 114, 115, 116, 117,
    118, 119, 120, 121, 133, 134, 135, 136, 137, 138,
    139, 140, 141, 142, 143, 145, 146, 147, 158, 159
]

base_url = "https://statsapi.mlb.com/api/v1/teams/{}/roster?rosterType=active"

players = []

for team_id in team_ids:
    url = base_url.format(team_id)
    res = requests.get(url)
    roster_data = res.json()
    
    for player in roster_data.get('roster', []):
        player_info = player['person']
        players.append({
            'id': player_info['id'],
            'name': player_info['fullName'],
            'team_id': team_id,
            'position': player.get('position', {}).get('abbreviation', '')
        })

# Save to CSV
df = pd.DataFrame(players)
df.drop_duplicates(subset='id', inplace=True)
df.to_csv('mlb_2025_player_ids.csv', index=False)

print(f"✅ Saved {len(df)} unique player IDs to 'mlb_2025_player_ids.csv'")

