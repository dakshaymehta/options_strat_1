from flask import Flask, render_template
import datetime
import time
import yfinance as yf
from prettytable import PrettyTable

app = Flask(__name__)

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

        return table.get_html_string()
    else:
        return f"No options match the given criteria for {ticker}."

def get_watchlist(file_name):
    with open(file_name, 'r') as file:
        tickers = file.read().strip().split(',')
        return [ticker.strip().upper() for ticker in tickers]

@app.route('/')
def index():
    watchlist_file = 'watchlist.txt'
    tickers = get_watchlist(watchlist_file)

    tables = []
    for ticker in tickers:
        table = find_options(ticker)
        tables.append(table)

    return render_template('index.html', options=options if options else [])


if __name__ == "__main__":
    app.run(debug=True)
