import requests
import pandas as pd
import zipfile
import io
import os
from datetime import datetime, timedelta

def download_daily_klines(symbol, date_str):
    """
    Download 1-minute klines for a specific symbol and date
    
    Args:
        symbol (str): Trading pair symbol (e.g., 'BTCUSDT')
        date_str (str): Date in YYYY-MM-DD format
    """
    # Construct the URL for daily klines data
    base_url = "https://data.binance.vision/data/spot/daily/klines"
    url = f"{base_url}/{symbol}/1m/{symbol}-1m-{date_str}.zip"
    
    try:
        # Download the zip file
        response = requests.get(url)
        response.raise_for_status()
        
        # Create a zip file object from the downloaded content
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            csv_filename = zip_file.namelist()[0]
            
            # Read the CSV data
            with zip_file.open(csv_filename) as csv_file:
                columns = [
                    'Open time', 'Open', 'High', 'Low', 'Adj Close', 'Volume',
                    'Close time', 'Quote asset volume', 'Number of trades',
                    'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'
                ]
                
                df = pd.read_csv(csv_file, names=columns)
                
                # Convert timestamp to datetime
                df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
                df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
                
                return df
                
    except requests.exceptions.RequestException as e:
        print(f"Error downloading data for {date_str}: {e}")
        return None
    except zipfile.BadZipFile:
        print(f"Error: Downloaded file for {date_str} is not a valid zip file")
        return None
    except Exception as e:
        print(f"An error occurred for {date_str}: {e}")
        return None

def download_date_range(symbol, start_date, end_date):
    """
    Download and combine data for a range of dates
    
    Args:
        symbol (str): Trading pair symbol
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
    """
    # Convert string dates to datetime objects
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    # List to store dataframes
    dfs = []
    
    # Download data for each date
    current_date = start
    while current_date <= end:
        date_str = current_date.strftime('%Y-%m-%d')
        print(f"Downloading data for {date_str}...")
        
        df = download_daily_klines(symbol, date_str)
        if df is not None:
            dfs.append(df)
        
        current_date += timedelta(days=1)
    
    # Combine all dataframes
    if dfs:
        combined_df = pd.concat(dfs, axis=0, ignore_index=True)
        
        # Sort by timestamp
        combined_df = combined_df.sort_values('Open time')
        
        # Save to CSV
        output_filename = f"{symbol}_1m_{start_date}_to_{end_date}.csv"
        combined_df.to_csv(output_filename, index=False)
        print(f"\nData saved to {output_filename}")
        return combined_df
    else:
        print("No data was downloaded successfully")
        return None

# Example usage
symbol = "BTCUSDT"
start_date = "2024-12-01"
end_date = "2024-12-10"
combined_df = download_date_range(symbol, start_date, end_date)