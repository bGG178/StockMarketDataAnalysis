"""
Grant Bowers
stocks.py
2/10/25
"""
import os
from requests import get
import json
from datetime import date
import sys

"""
    :purpose:
        To practice fetching data from the web
    :Help:
        Used AI to help learning how to sort through the dictionaries, I am not a fan of dictionaries within dictionaries
        despite how useful they are for storing and organizing information.
        Worked closely with classmates to figure out the download_data function (lots of trial and error happened)
    :Functions:
        :download_data:
            Fetches data using the Requests module and returns them as a dictionary for processing 
        :process_data:
            Manipulates dictionary returned by download_data function
        
"""


def download_data(ticker: str) -> dict:
    """
    Purpose:
        To fetch data using requests module
    Parameters:
        Ticker -> Passed in ticker for the stock to fetch from the API (ie. AAPL, MSFT, etc)
    Returns:
        dictionary -> data or None to throw an error
    """
    ticker = ticker.upper()
    today = date.today()
    start = str(today.replace(year=today.year - 5))
    base_url = "https://api.nasdaq.com/"
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit=9999"

    #Setting up requests and returning the retrieved data
    try:
        data = get(base_url + path, headers={"User-Agent": "Mozilla/5.0"})
        data = data.json()
        return data

    #Passes exception if there is an error and returns None
    except Exception as e:
        print(f"Exception encountered {e}")
        return None

def data_process(data : dict, ticker : str) -> dict:
    """
    Purpose:
        To initialize the base class
    Parameters:
        Data -> Passes the dictionary fetched from download_data
        Ticker -> Passed in ticker for the stock to be documented (ie. AAPL, MSFT, etc)
    Returns:
        Dictionary -> Returns the dictionary containing information of the ticker, min, max, average, and median
    """
    closingprices =[]
    largestprice = 0
    smallestprice = 99999999

    #Template for the dictionary that will be returned
    processeddict = {'ticker':None,'min':None,'max':None,'avg':None,'median':None}

    #Adds the ticker to the processed dictionary
    processeddict['ticker'] = ticker.upper()

    #Keep track of the largest and smallest price
    #Places all closing prices into a list and makes them floating numbers
    for price in list(data["data"]["tradesTable"]["rows"]):
        pricetoint = float(price["close"].replace('$',''))
        closingprices.append(pricetoint)

        if (pricetoint > largestprice):
            largestprice = pricetoint
        if (pricetoint < smallestprice):
            smallestprice = pricetoint

    #calculate average closing price and sending them to dictionary
    lengthprices = len(closingprices)
    total = 0
    for price in closingprices:
        total += price
    average = (total)/lengthprices
    average = round(average,2)
    processeddict['avg'] = average

    #Sending min and max to dictionary
    processeddict['min'],processeddict['max'] = smallestprice,largestprice


    #Median calculation
    closingprices.sort()
    #Even length for list
    if (lengthprices/2)%2 == 1:
        medianprice = (closingprices[(lengthprices//2)-1] + closingprices[int((lengthprices // 2))])/2

    #Odd length for list
    else:
        medianprice = closingprices[(lengthprices//2)]

    processeddict['median'] = round(medianprice,2)

    return processeddict


#Uses a file for the raw data as well as a file for the stocks
stockfile = "rawdata.json"
processfile = "stocks.json"

#Clear the processed file if it exists
if os.path.exists(processfile):
    os.remove(processfile)

#Allows arguments when "python stocks.py stock1 stock2 etc" ran in terminal
if __name__ == "__main__":
    tickers = []
    for ticker in sys.argv[1:]:
        tickers.append(ticker)

    for ticker in tickers:
        data = download_data(ticker)

        if data["data"] is not None:

            with open(stockfile, "w") as file:
                json.dump(data, file)

            postprocess = data_process(data,ticker)

            with open(processfile, "a") as file:
                json.dump(postprocess,file, indent=4)

        else:
            print(f"Error, invalid Ticker '{ticker.upper()}' or No Data Available!")
