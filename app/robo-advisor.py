# app/robo_advisor.py


import requests
import dotenv
import json
import datetime
import csv
import os
from dotenv import load_dotenv
import plotly.graph_objects as go
import operator



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

#input_ticker = ['MSFT', 'IBM']

init_tk_str = os.environ.get('INIT_TICKER_LIST')
working_tk = init_tk_str.split(',')
initial_tickers = [str(t).strip() for t in working_tk]
initial_tickers = [t for t in working_tk if t != '']

if len(initial_tickers) > 0:
    print('ROBO ADVISOR IS INITIALIZED WITH THE FOLLOWING TICKER(S):')
    for t in initial_tickers:
        print(f"---{t}")
    add_tick_yn = input('Would you like to add more tickers? [y/n]')
    while str(add_tick_yn).lower() not in ["y","n"]:
        add_tick_yn=input("Response not recognized.  Please respond with 'y' for yes or 'n' for no.\nWould you like to add more tickers? [y/n]")
    if str(add_tick_yn).lower() == "n":
        raw_input_tickers = initial_tickers
    else:
        add_tick = input('Enter tickers (separated by comma if more than one):')
        working_add_tick = str(add_tick).split(',')
        fin_add_tick = [str(t).strip() for t in working_add_tick]
        fin_add_tick = [t for t in fin_add_tick if t != '']
        raw_input_tickers = initial_tickers
        for t in fin_add_tick:
            raw_input_tickers.append(t)

else:
    add_tick = input('Enter tickers (separated by comma if more than one):')
    working_add_tick = str(add_tick).split(',')
    working_add_tick = [str(t).strip() for t in working_add_tick]
    raw_input_tickers=[t for t in working_add_tick if t!='']

#breakpoint()

raw_input_tickers=[t.upper() for t in raw_input_tickers]
#raw_input_tickers=['MSFT',' IB M','BARD RICCIARDI']
input_ticker = [str(t).replace(" ", "") for t in raw_input_tickers]
spchk = [str(t).find(" ") for t in raw_input_tickers]
#print(spchk)

#TODO: write validation code for input list
failed_tickers=[]
#TODO: take user inputs
#TODO: check user inputs for formatting >> this doesn't seem to matter (unless you don't enter anything)
#TODO: since formatting may not matter, see if you can return only those list items for which there
# were errors in pulling data. Prompt user to enter more tickers or continue.

dt_exec = datetime.datetime.now()
#print(dt_exec)  # > 2020-06-13 15:38:02.986058
#print(type(dt_exec))  # > <class 'datetime.datetime'>


print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {dt_exec.strftime('%#I:%M%p').lower()} on {dt_exec.strftime('%A, %B %#d')}{date_suffix(dt_exec)}, {dt_exec.strftime('%Y')}")


#TODO: Take user risk tolerance - how to translate risk tolerance into advice?

for tkr in input_ticker:

    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={tkr}&apikey={api_key}"
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

    parsed_response = json.loads(response.text)
    #print(type(parsed_response)) # > <class 'dict'>
    #print(parsed_response.keys()) # > dict_keys(['Meta Data', 'Time Series (Daily)'])


    error_check_list = list(parsed_response.keys())
    error_check = error_check_list[0]

    if error_check=='Meta Data':


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
        # TODO: 52-week periods: For example, if the last available day of trading data is June 1st, 2018
        # , the program should find the maximum of all the "high" prices between around June 1st, 2017
        # and June 1st, 2018.
        highlow_pd = min(100,len(close_days))


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

        high_date = []
        low_date= []
        for k, d in parsed_response['Time Series (Daily)'].items():
            #print(k)
            #print(d)
            #print(d['2. high'])
            #breakpoint()
            if float(d['2. high']) == recent_high:
                high_date.append(k)
            elif float(d['3. low']) == recent_low:
                low_date.append(k)

        recent_high_dt = datetime.datetime.fromisoformat(high_date[0])
        recent_low_dt = datetime.datetime.fromisoformat(low_date[0])



        # WRITE CSV DATA ------------------------------------------------------------------------

        headers = ['timestamp', 'open', 'high', 'low', 'close', 'volume'] #list(parsed_response['Time Series(Daily)'][latest_day].keys())
        #print(headers)

        csv_filepath = os.path.join(os.path.dirname(os.path.abspath(
            __file__)), '..', 'data', f"{symbol}.csv")  # a relative filepath

        chart_data=[]

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

                chart_data.append({
                    'timestamp': k,
                    'open': parsed_response['Time Series (Daily)'][k]['1. open'],
                    'high': parsed_response['Time Series (Daily)'][k]['2. high'],
                    'low': parsed_response['Time Series (Daily)'][k]['3. low'],
                    'close': parsed_response['Time Series (Daily)'][k]['4. close'],
                    'volume': parsed_response['Time Series (Daily)'][k]['5. volume']
                    })

        # RECOMMENDATION ------------------------------------------------------------------------

        rec_criteria = float(px_last) / float(recent_low)
        if rec_criteria >= 1.2:
            rec = f"DO NOT BUY {symbol}!"
            reason=f"{symbol} most recently closed at or above 20% of its recent low."
        else:
            rec = f"BUY {symbol}!"
            reason=f"{symbol} most recently closed within 20% of its recent low"


        # PRINT INFORMATION ---------------------------------------------------------------------

        print("-------------------------")
        print(f"SELECTED SYMBOL: {symbol}")
        print("-------------------------")
        print(f"LATEST DAY: {last_ref_dt.strftime('%A, %B %#d')}{date_suffix(last_ref_dt)}, {last_ref_dt.strftime('%Y')}")
        print(f"LATEST CLOSE: {to_usd(float(px_last))}")
        print(f"RECENT HIGH: {to_usd(recent_high)}")
        print(f"RECENT LOW: {to_usd(recent_low)}")
        print("-------------------------")
        print(f"ANALYSIS: {symbol} is trading at {(100*rec_criteria):.1f}% of its recent low")
        print(f"RECOMMENDATION: {rec}")
        print(f"RECOMMENDATION REASON: {reason}")
        print("-------------------------")
        print(f"WRITING DATA TO CSV: {os.path.abspath(csv_filepath)}")
        print("-------------------------")


        sorted_chart_data = sorted(
            chart_data, key=operator.itemgetter('timestamp'), reverse=False)

        #print(sorted_chart_data)

        cht_timestamp = [p['timestamp'] for p in sorted_chart_data]
        cht_open = [p['open'] for p in sorted_chart_data]
        cht_close = [p['close'] for p in sorted_chart_data]
        cht_high = [p['high'] for p in sorted_chart_data]
        cht_low = [p['low'] for p in sorted_chart_data]
        #print(cht_timestamp)

        anno = [dict(x=last_ref_dt, y=px_last, xref='x', yref='y', text=f"Last Close: {to_usd(float(px_last))}", showarrow=True, arrowhead=7, ax=-40, ay=80),
                dict(x=recent_high_dt, y=recent_high, xref='x', yref='y', text=f"Recent High: {to_usd(recent_high)}", showarrow=True, arrowhead=7, ax=-40, ay=-40),
                dict(x=recent_low_dt, y=recent_low, xref='x', yref='y', text=f"Recent Low: {to_usd(recent_low)}", showarrow=True, arrowhead=7, ax=-40, ay=40),
                dict(x=last_ref_dt, y=(1.2*recent_low), xref='x', yref='y', text=f"Price Threshhold for Purchase: {to_usd(1.2*recent_low)}", showarrow=False, yanchor='bottom',xanchor='right')]

        thresh=[dict(x0=min(cht_timestamp),x1=max(cht_timestamp),y0=(1.2*recent_low),y1=(1.2*recent_low),xref='x',yref='y',line_width=1)]

        #print(anno)
        fig = go.Figure(data=[go.Candlestick(
            x=cht_timestamp, open=cht_open, high=cht_high, low=cht_low, close=cht_close)],
                layout=go.Layout(title=go.layout.Title(text=f"{symbol}"), shapes=thresh, annotations=anno, yaxis_title="Price per Share (USD)"))

        fig.show()




        #TODO: DATA VIS?? display a line graph of the stock prices over time.

        #TODO: EMAIL ALERT?  Modify the logic of your application such that if it detects the stock's
        # price has moved past a given threshold within a given time period (e.g. the price has increased
        # or decreased by more than 5% within the past day), it will send the user a "Price Movement
        # Alert" message via email.

        #HINT: leverage the email-sending capabilities of the sendgrid package, and optionally use Sendgrid
        # email templates to further control the formatting of email contents

        #TODO: Modify the logic of your application such that if it detects the stock's price has moved
        # past a given threshold within a given time period (e.g. the price has increased or decreased by
        # more than 5% within the past day), it will send the user a "Price Movement Alert" message via SMS.

        #HINT: leverage the SMS-sending capabilities of the twilio package

        # for tomorrow...

    else:
        #print("-------------------------")
        #print(f"There was an API error with your attempt to pull data for the ticker {tkr}.")
        #print("-------------------------")
        if error_check == "Error Message":
            failed_tickers.append({'ticker': tkr, 'err_type': 'Invalid API Call'})
        elif error_check == "Note":
            failed_tickers.append({'ticker': tkr, 'err_type': 'Exceeds API Call Limit (5 per minute and 500 per day)'})
        else:
            failed_tickers.append({'ticker': tkr, 'err_type': 'Other'})


if len(failed_tickers) > 0:
    if len(failed_tickers) == len(input_ticker):
        print("-------------------------")
        print("UNABLE TO GENERATE REPORT FOR THE SPECIFIED TICKER(S).\nSEE ERROR SUMMARY")
        print("-------------------------")

    print("-------------------------")
    print("ERROR SUMMARY:")
    print("An error occurred while attempting to pull data from the API for the following ticker(s):")
    for t in failed_tickers:
        print(f"----{t['ticker']}: {t['err_type']}")
    print("Please check the accuracy of the ticker(s) and try again.")
    if max(spchk) > -1:
        print("For example, a space was found in the middle of at least one input ticker (spaces are automatically removed).")

print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
