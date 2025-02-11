
from numpy.ma.core import empty
from requests import get
import json
from datetime import date

def download_data(ticker: str) -> dict:
    ticker = ticker.upper()
    today = date.today()
    start = str(today.replace(year=today.year - 1))
    base_url = "https://api.nasdaq.com/"
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit=9999"

    try:
        data = get(base_url + path, headers={"User-Agent": "Mozilla/5.0"})
        data = data.json()
        return data

    except Exception as e:
        print(f"Exception occurred {e}")


data = download_data("TSLA")
stockfile = "stocks.json"

with open(stockfile, "w") as file:
    json.dump(data, file)

for price in list(data["data"]["tradesTable"]["rows"]):
    print("Date: " + price["date"])
    print("Opening: " + price["open"])
    print("Close: " +price["close"])
    print("Highest: " + price["high"])
    print("Lowest: " + price["low"])
    print()
