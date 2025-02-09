from requests import get
from urllib.request import urlopen
import yfinance as yf
def download_data(ticker: str) -> dict:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2d")

        return hist.to_dict()
    except Exception as e:
        print(f"Error retrieving information for {ticker}: Error: {e}")
        return


retrieved_data = download_data("AAPL")

dates = list(next(iter(retrieved_data.values())).keys())

for date in dates:
    print(f"\nDate: {date}")
    for key, values in retrieved_data.items():
        print(f"{key}: {values.get(date, 'N/A')}")

try:
    response = get("https://ipinfo.io/json")
    print(response.json())
except Exception as e:
    print(e)


