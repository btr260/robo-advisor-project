# app/robo_advisor.py


import requests
import dotenv
import json
import datetime
import csv
import os
from dotenv import load_dotenv



# LOAD .ENV ----------------------------------------------------------------------
load_dotenv()
api_key = os.environ.get('ALPHAVANTAGE_API_KEY')
#print(os.environ.get('ALPHAVANTAGE_API_KEY'))

# FUNCTIONS ----------------------------------------------------------------------

def to_usd(my_price):
    '''
    Converts a numeric value to usd-formatted string, for printing and display purposes.

    Param: my_price (int or float) like 4000.444444

    Example: to_usd(4000.444444)

    Returns: $4,000.44
    '''
    return f'${my_price:,.2f}'  # > $12,000.71

def date_suffix(dt_for_suf):
    if 4 <= dt_for_suf.day <= 20 or 24 <= dt_for_suf.day <= 30:
        suffix='th'
    else:
        suffix = ['st', 'nd', 'rd'][dt_for_suf.day % 10 - 1]

    return suffix



# REQUEST API DATA ----------------------------------------------------------------

input_ticker = 'BUFUuuuu'  #TODO: take user input(s)

#TODO: Take user risk tolerance - how to translate risk tolerance into advice?

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={input_ticker}&apikey={api_key}"
response = requests.get(request_url)
print(type(response))  # > <class 'requests.models.Response'>
print(response.status_code) # > 200
#print(type(response.text)) # > <class 'str'>
print(response.text) # > STRING variable (shown below).  Need to parse into process into dictionary using json module.

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


# PULL LAST REFRESH FROM DATA -----------------------------------------------------------

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
#print(last_ref_dt) # > 2020-06-12 00:00:00
#print(type(last_ref_dt)) # > <class 'datetime.datetime'>


# PULL SYMBOL FROM DATA ------------------------------------------------------------------

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

# PULL LATEST CLOSE FROM DATA ------------------------------------------------------------

# Get list of time series days #TODO: currently assumes data is sorted.  consider sorting to ensure
close_days = list(parsed_response['Time Series (Daily)'].keys())
latest_day = close_days[0]
px_last = parsed_response['Time Series (Daily)'][latest_day]['4. close']
#print(px_last)
#print(type(px_last)) # > <class 'str'>

# PULL RECENT HIGH: max of highs over last 100 days
highlow_pd = 100

high_px = []

for d in close_days[0:highlow_pd]:
    high_px.append(float(parsed_response['Time Series (Daily)'][d]['2. high']))

#print(high_px)
#print(len(high_px))
recent_high = max(high_px)
#print(recent_high)


# PULL RECENT LOW: min of lows over last 100 days

low_px = []

for d in close_days[0:highlow_pd]:
    low_px.append(float(parsed_response['Time Series (Daily)'][d]['3. low']))

#print(low_px)
#print(len(low_px))
recent_low = min(low_px)
#print(recent_low)


# WRITE CSV DATA ------------------------------------------------------------------------

headers = ['timestamp', 'open', 'high', 'low', 'close', 'volume'] #list(parsed_response['Time Series(Daily)'][latest_day].keys())
#print(headers)

csv_filepath = os.path.join(os.path.dirname(os.path.abspath(
    __file__)), '..', 'data', f"{symbol}.csv")  # a relative filepath

with open(csv_filepath,'w') as csv_file:  # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=headers)
    writer.writeheader()  # uses fieldnames set above

    for k in close_days:
        writer.writerow({
            'timestamp': k,
            'open': parsed_response['Time Series (Daily)'][k]['1. open'],
            'high': parsed_response['Time Series (Daily)'][k]['2. high'],
            'low': parsed_response['Time Series (Daily)'][k]['3. low'],
            'close': parsed_response['Time Series (Daily)'][k]['4. close'],
            'volume': parsed_response['Time Series (Daily)'][k]['5. volume']
            })




# PRINT INFORMATION ---------------------------------------------------------------------

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {dt_exec.strftime('%#I:%M%p').lower()} on {dt_exec.strftime('%A, %B %#d')}{date_suffix(dt_exec)}, {dt_exec.strftime('%Y')}")
print("-------------------------")
print(f"LATEST DAY: {last_ref_dt.strftime('%A, %B %#d')}{date_suffix(last_ref_dt)}, {last_ref_dt.strftime('%Y')}")
print(f"LATEST CLOSE: {to_usd(float(px_last))}")
print(f"RECENT HIGH: {to_usd(recent_high)}")
print(f"RECENT LOW: {to_usd(recent_low)}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"WRITING DATA TO CSV: {os.path.abspath(csv_filepath)}")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
