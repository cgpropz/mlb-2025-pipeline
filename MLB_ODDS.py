import requests
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

def dfs_scraper():
    print("[+] Fetching data from PrizePicks API...")
    url = "https://partner-api.prizepicks.com/projections?per_page=1000"
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

        league = league_map.get(league_id, "N/A")
        if league != "MLB":
            continue  # Only scrape MLB players

        data.append({
            "Player": player_id_map.get(player_id, "N/A"),
            "League": league,
            "Team": attr.get("description", "N/A"),  # ← TEAM comes from `description`
            "Stat": attr.get("stat_type", "N/A"),
            "Line": attr.get("line_score", "N/A"),
            "Type": attr.get("projection_type", "N/A"),
            "Odds_Type": attr.get("odds_type", "N/A"),
        })

    return pd.DataFrame(data)

def update_google_sheets(df):
    print("[+] Authenticating and pushing data to Google Sheets...")

    SPREADSHEET_ID = "1X6dMVxb7vPITaONfXdrNVj0sDAKsLmxj0NYpzDfK5Gc"
    SHEET_RANGE = "PP_ODDS!A1"

    creds = service_account.Credentials.from_service_account_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    values = [df.columns.tolist()] + df.values.tolist()

    sheet.values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_RANGE
    ).execute()

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


