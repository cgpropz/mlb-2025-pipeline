import requests
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

def dfs_scraper():
    print("[+] Fetching data from PrizePicks API...")
    url = "https://api.prizepicks.com/projections?per_page=1000"
    response = requests.get(url)
    projections = response.json()

    # Prep lookup tables
    player_id_map = {}
    league_map = {}

    for included in projections["included"]:
        if included["type"] == "new_player":
            pid = included["id"]
            name = included["attributes"]["name"]
            player_id_map[pid] = name
        elif included["type"] == "league":
            lid = included["id"]
            league = included["attributes"]["name"]
            league_map[lid] = league

    data = []
    for item in projections["data"]:
        attr = item["attributes"]
        player_id = item["relationships"]["new_player"]["data"]["id"]
        league_id = item["relationships"]["league"]["data"]["id"]
        team = attr.get("team", "N/A")
        stat = attr.get("stat_type", "N/A")
        line = attr.get("line_score", "N/A")
        type_ = attr.get("projection_type", "N/A")

        data.append({
            "Player": player_id_map.get(player_id, "N/A"),
            "League": league_map.get(league_id, "N/A"),
            "Team": team,
            "Stat": stat,
            "Line": line,
            "Type": type_
        })

    return pd.DataFrame(data)

def update_google_sheets(df):
    print("[+] Authenticating and pushing data to Google Sheets...")

    # Set your own sheet ID and tab name here
    SPREADSHEET_ID = "1X6dMVxb7vPITaONfXdrNVj0sDAKsLmxj0NYpzDfK5Gc"
    SHEET_RANGE = "PP_ODDS!A1"

    # Load creds
    creds = service_account.Credentials.from_service_account_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    # Prepare data
    values = [df.columns.tolist()] + df.values.tolist()

    # Clear existing values
    sheet.values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_RANGE
    ).execute()

    # Upload new data
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_RANGE,
        valueInputOption="RAW",
        body={"values": values}
    ).execute()

    print("[+] Sheet successfully updated!")

if __name__ == "__main__":
    df = dfs_scraper()
    update_google_sheets(df)

