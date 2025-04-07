import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Constants
TODAY = datetime.today().strftime('%Y-%m-%d')
ROSTER_DIR = 'rosters'
INJURY_DIR = 'injuries'
SPREADSHEET_ID = '1X6dMVxb7vPITaONfXdrNVj0sDAKsLmxj0NYpzDfK5Gc'

mlb_team_abbrs = [
    'angels', 'astros', 'athletics', 'bluejays', 'braves', 'brewers',
    'cardinals', 'cubs', 'dbacks', 'dodgers', 'giants', 'guardians',
    'mariners', 'marlins', 'mets', 'nationals', 'orioles', 'padres',
    'phillies', 'pirates', 'rangers', 'rays', 'reds', 'redsox',
    'rockies', 'royals', 'tigers', 'twins', 'whitesox', 'yankees'
]

os.makedirs(ROSTER_DIR, exist_ok=True)
os.makedirs(INJURY_DIR, exist_ok=True)

def get_sheets_service():
    with open('credentials.json') as f:
        creds_info = json.load(f)
    creds = service_account.Credentials.from_service_account_info(
        creds_info,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return build('sheets', 'v4', credentials=creds)

def get_injuries_from_mlb():
    all_injuries = []
    for team in mlb_team_abbrs:
        url = f'https://www.mlb.com/{team}/injuries'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        if not table:
            print(f"[!] No injury table found for {team}")
            continue
        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                all_injuries.append({
                    'Player': cols[0].text.strip(),
                    'Team': team.upper(),
                    'Injury': cols[1].text.strip(),
                    'Status': cols[2].text.strip(),
                    'Date': TODAY
                })
    df = pd.DataFrame(all_injuries)
    df.to_csv(f'{INJURY_DIR}/{TODAY}.csv', index=False)
    return df

def get_team_roster(team_abbr):
    url = f'https://www.mlb.com/{team_abbr}/roster'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    roster_table = soup.find('table')
    if not roster_table:
        return pd.DataFrame()
    rows = roster_table.find_all('tr')[1:]
    players = []
    for row in rows:
        name = row.find('td')
        if name:
            players.append(name.text.strip())
    return pd.DataFrame({'Player': players})

def compare_rosters(old_df, new_df):
    added = new_df[~new_df['Player'].isin(old_df['Player'])].copy()
    removed = old_df[~old_df['Player'].isin(new_df['Player'])].copy()
    added['Change Type'] = 'Added'
    removed['Change Type'] = 'Removed'
    return pd.concat([added, removed])

def update_google_sheets(changes_df, injury_df):
    service = get_sheets_service()
    sheet = service.spreadsheets()

    sheet.values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range='Roster Changes!A2:E'
    ).execute()
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range='Roster Changes!A2',
        valueInputOption='RAW',
        body={"values": changes_df.values.tolist()}
    ).execute()

    sheet.values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range='Injuries!A2:F'
    ).execute()
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range='Injuries!A2',
        valueInputOption='RAW',
        body={"values": injury_df.values.tolist()}
    ).execute()

def main():
    all_changes = []

    for team in mlb_team_abbrs:
        print(f"Processing {team}...")
        roster_path = f'{ROSTER_DIR}/{team}_{TODAY}.csv'
        current = get_team_roster(team)
        current.to_csv(roster_path, index=False)

        try:
            all_files = sorted([f for f in os.listdir(ROSTER_DIR) if f.startswith(team)])
            prev_file = [f for f in all_files if f < f'{team}_{TODAY}.csv'][-1]
            previous = pd.read_csv(f'{ROSTER_DIR}/{prev_file}')
        except Exception:
            previous = pd.DataFrame(columns=['Player'])

        diff_df = compare_rosters(previous, current)
        diff_df['Date'] = TODAY
        diff_df['Team'] = team.upper()
        all_changes.append(diff_df)

    all_changes_df = pd.concat(all_changes, ignore_index=True) if all_changes else pd.DataFrame()
    injuries = get_injuries_from_mlb()
    update_google_sheets(all_changes_df, injuries)

if __name__ == '__main__':
    main()
