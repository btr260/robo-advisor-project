# app/robo_advisor.py


import requests
import dotenv
import json

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
response = requests.get(request_url)
#print(type(response))  # > <class 'requests.models.Response'>
#print(response.status_code) # > 200
#print(type(response.text)) # > <class 'str'>
#print(response.text) # > STRING variable (shown below).  Need to parse into process into dictionary using json module.

#{
#"Meta Data": {
#    "1. Information": "Daily Prices (open, high, low, close) and Volumes",
#    "2. Symbol": "IBM",
#    "3. Last Refreshed": "2020-06-12",
#    "4. Output Size": "Compact",
#    "5. Time Zone": "US/Eastern"
#},
#"Time Series (Daily)": {
#    "2020-06-12": {
#        "1. open": "121.2500",
#        "2. high": "123.1200",
#        "3. low": "119.2800",
#        "4. close": "121.9100",
#        "5. volume": "6218003"
#    }, ...


parsed_response=json.loads(response.text)
print(type(parsed_response)) # > <class 'dict'>


breakpoint()

quit()






print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: 2018-02-20")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
