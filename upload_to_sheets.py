import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load your merged CSV
df = pd.read_csv("all_2025_gamelogs.csv")

# Your sheet info
SPREADSHEET_ID = "1X6dMVxb7vPITaONfXdrNVj0sDAKsLmxj0NYpzDfK5Gc"  # your sheet ID
SHEET_RANGE = "Player Logs!A1:N"  # replace with target tab & start cell

# Load credentials
creds = service_account.Credentials.from_service_account_file(
    "credentials.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

# Build the Sheets API service
service = build("sheets", "v4", credentials=creds)

# Step 1: Clear existing data in the range
clear = service.spreadsheets().values().clear(
    spreadsheetId=SPREADSHEET_ID,
    range=SHEET_RANGE,
).execute()

# Step 2: Upload new data
values = [df.columns.tolist()] + df.values.tolist()
body = {"values": values}

update = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range=SHEET_RANGE,
    valueInputOption="RAW",
    body=body
).execute()

print(f"✅ Uploaded {len(df)} rows to Google Sheets.")
