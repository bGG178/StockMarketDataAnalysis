
from numpy.ma.core import empty, floor
from requests import get
import json
from datetime import date
from math import ceil

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

def data_process(data : dict) -> dict:
    closingprices =[]
    largestprice = 0
    smallestprice = 99999999

    processeddict = {'min':None,'max':None,'avg':None,'median':None}
    for price in list(data["data"]["tradesTable"]["rows"]):
        pricetoint = float(price["close"].replace('$',''))
        closingprices.append(pricetoint)

        if (pricetoint > largestprice):
            largestprice = pricetoint
        if (pricetoint < smallestprice):
            smallestprice = pricetoint

    #calculate average closing price
    lengthprices = len(closingprices)
    total = 0
    for price in closingprices:
        total += price
    average = (total)/lengthprices
    average = round(average,2)
    processeddict['avg'] = average

    #min and max
    processeddict['min'],processeddict['max'] = smallestprice,largestprice


    #median
    closingprices.sort()
    #Even length for list
    if (lengthprices/2)%2 == 1:
        #print((lengthprices // 2) - 1)
        #print((lengthprices//2))
        #print(closingprices[(lengthprices//2)-1])
        #print(closingprices[(lengthprices//2)])

        medianprice = (closingprices[(lengthprices//2)-1] + closingprices[int((lengthprices // 2))])/2

    #Odd length for list
    else:
        medianprice = closingprices[(lengthprices//2)]

    processeddict['median'] = medianprice
    print(processeddict)

    return processeddict

data = download_data("TSLA")
stockfile = "rawdata.json"
processfile = "stocks.json"

with open(stockfile, "w") as file:
    json.dump(data, file)

postprocess = data_process(data)

with open(processfile, "w") as file:
    json.dump(postprocess,file)