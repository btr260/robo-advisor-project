# app/robo_advisor.py


import requests
import dotenv
import json
import datetime


# FUNCTIONS ----------------------------------------------------------------------

def to_usd(my_price):
    '''
    Converts a numeric value to usd-formatted string, for printing and display purposes.

    Param: my_price (int or float) like 4000.444444

    Example: to_usd(4000.444444)

    Returns: $4,000.44
    '''
    return f'${my_price:,.2f}'  # > $12,000.71



# REQUEST API DATA ----------------------------------------------------------------

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

# PARSE API DATA -----------------------------------------------------------------------

parsed_response=json.loads(response.text)
#print(type(parsed_response)) # > <class 'dict'>
#print(parsed_response.keys()) # > dict_keys(['Meta Data', 'Time Series (Daily)'])


# PULL INFORMATION FROM DATA -----------------------------------------------------------

#print(parsed_response['Meta Data'])
#{'1. Information': 'Daily Prices (open, high, low, close) and Volumes', '2. Symbol': 'IBM',
# '3. Last Refreshed': '2020-06-12', '4. Output Size': 'Compact', '5. Time Zone': 'US/Eastern'}

#print(parsed_response['Meta Data'].keys())
#dict_keys(['1. Information', '2. Symbol', '3. Last Refreshed',
#           '4. Output Size', '5. Time Zone'])

#print(parsed_response['Meta Data']['3. Last Refreshed'])
#'2020-06-12'

last_refreshed = parsed_response['Meta Data']['3. Last Refreshed']
last_ref_dt = datetime.datetime.fromisoformat(last_refreshed)
print(last_ref_dt)
print(type(last_ref_dt))
symbol = parsed_response['Meta Data']['2. Symbol']
dt_exec = datetime.datetime.now()
#print(dt_exec)  # > 2020-06-13 15:38:02.986058
#print(type(dt_exec))  # > <class 'datetime.datetime'>

#print(parsed_response['Time Series (Daily)'])
#print(parsed_response['Time Series (Daily)'].keys())
#dict_keys(['2020-06-12', '2020-06-11', '2020-06-10', '2020-06-09', '2020-06-08', '2020-06-05',
# '2020-06-04', '2020-06-03', '2020-06-02', '2020-06-01', '2020-05-29', '2020-05-28', '2020-05-27',
#  '2020-05-26', '2020-05-22', '2020-05-21', '2020-05-20', '2020-05-19', '2020-05-18', ...

#print(parsed_response['Time Series (Daily)']['2020-06-12'])
#{'1. open': '121.2500', '2. high': '123.1200', '3. low': '119.2800', '4. close': '121.9100',
#  '5. volume': '6218003'}

#print(parsed_response['Time Series (Daily)']['2020-06-12'].keys())
#dict_keys(['1. open', '2. high', '3. low', '4. close', '5. volume'])

# Get list of time series days #TODO: currently assumes data is sorted.  consider sorting to ensure
close_days = list(parsed_response['Time Series (Daily)'].keys())
latest_day = close_days[0]
px_last = parsed_response['Time Series (Daily)'][latest_day]['4. close']
#print(px_last)
#print(type(px_last)) # > <class 'str'>


# PRINT INFORMATION ---------------------------------------------------------------------

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {dt_exec.strftime('%#I:%M%p').lower()} on {dt_exec.strftime('%A, %B %#d, %Y')}")
print("-------------------------")
print(f"LATEST DAY: {last_ref_dt.strftime('%A, %B %#d, %Y')}")
print(f"LATEST CLOSE: {to_usd(float(px_last))}")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
