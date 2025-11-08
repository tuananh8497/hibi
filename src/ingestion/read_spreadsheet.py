import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path
from dotenv import load_dotenv
import os
import pandas as pd

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / 'env' / 'local.env'
load_dotenv(env_path)

# Get values from environment variables
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
WORKSHEET_NAME = os.getenv('WORKSHEET_NAME')

def setup_gspread_client():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("env/credentials.json", scopes=scopes)
    try:
        client = gspread.authorize(creds)
        print("Gspread client successfully authorized.")
    except Exception as e:
        print(f"Failed to authorize Gspread client: {e}")
        raise
    return client

def main():
    client = setup_gspread_client()
    workbook = client.open_by_key(SPREADSHEET_ID)
    worksheet = workbook.worksheet(WORKSHEET_NAME)
    data = worksheet.get_all_values()

    headers = data[0]
    rows = data[1:]
    df = pd.DataFrame(rows, columns=headers)

    print(df.head())

if __name__ == "__main__":
  main()