import datetime
import time
import yfinance as yf
from prettytable import PrettyTable

def find_options(ticker):
    yf_ticker = yf.Ticker(ticker)
    options_exp = yf_ticker.options

    filtered_options = []

    for exp in options_exp:
        calls = yf_ticker.option_chain(exp).calls
        puts = yf_ticker.option_chain(exp).puts
        options = calls.append(puts, ignore_index=True)
        
        for _, option in options.iterrows():
            if option['volume'] > option['openInterest']:
                option['expiration'] = exp
                filtered_options.append(option)

    if filtered_options:
        table = PrettyTable()
        table.field_names = ["Ticker", "Expiration", "Strike", "Type", "Volume", "Open Interest"]
        
        for option in filtered_options:
            table.add_row([
                ticker, 
                option['expiration'], 
                option['strike'],
                option['contractSymbol'][-9:-6],
                option['volume'],
                option['openInterest']
            ])

        print(f"Filtered options for {ticker}:")
        print(table)
    else:
        print(f"No options match the given criteria for {ticker}.")

def get_watchlist(file_name):
    with open(file_name, 'r') as file:
        tickers = file.read().strip().split(',')
        return [ticker.strip().upper() for ticker in tickers]

if __name__ == "__main__":
    watchlist_file = 'watchlist.txt'
    tickers = get_watchlist(watchlist_file)

    update_interval = 60  # Time interval between updates in seconds, you can adjust this value

    while True:
        for ticker in tickers:
            print(f"Fetching options data for {ticker} at {datetime.datetime.now()}")
            find_options(ticker)
        print(f"Waiting for {update_interval} seconds before updating...\n")
        time.sleep(update_interval)
