import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path
from dotenv import load_dotenv
import os
import pandas as pd
from pyspark.sql import SparkSession

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / 'env' / 'local.env'
load_dotenv(env_path)

# Get values from environment variables
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
WORKSHEET_NAME = os.getenv('WORKSHEET_NAME')
CREDENTIAL_PATH = os.getenv('CREDENTIAL_PATH')
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

def setup_gspread_client():
    creds = Credentials.from_service_account_file(CREDENTIAL_PATH, scopes=SCOPE)
    try:
        client = gspread.authorize(creds)
        print("Gspread client successfully authorized.")
    except Exception as e:
        print(f"Failed to authorize Gspread client: {e}")
        raise
    return client

def setup_spark_session():
    return (
        SparkSession.builder
        .remote("sc://localhost:15002")
        .getOrCreate()
    )

def main():
    spark = setup_spark_session()
    client = setup_gspread_client()
    workbook = client.open_by_key(SPREADSHEET_ID)
    worksheet = workbook.worksheet(WORKSHEET_NAME)
    data = worksheet.get_all_values()

    headers = data[0]
    rows = data[1:]
    df = pd.DataFrame(rows, columns=headers)

    print(df.head(n=20))

if __name__ == "__main__":
  main()