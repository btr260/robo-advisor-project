# "Robo Advisor" Project


## Program Overview

  1. Take list of tickers specified by user in a .env file or in command line.
  2. Parse tickers for validity and remove obviously invalid entries.
  3. Access API and pull data for screened list of tickers.
  4. Process data into 'buy' or 'don't buy' recommendation based on price history.
  5. Present results in command line and a candlestick plot.
  6. Save price data as CSV file.


### Repo Setup

Use the GitHub.com online interface to create a new remote project repository called something like "robo-advisor". When prompted by the GitHub.com online interface, add a "README.md" file and a Python-flavored ".gitignore" file (and also optionally a "LICENSE") during the repo creation process. After this process is complete, you should be able to view the repo on GitHub.com at an address like `https://github.com/YOUR_USERNAME/robo-advisor`.

After creating the remote repo, use GitHub Desktop software or the command-line to download or "clone" it onto your computer. Choose a familiar download location like the Desktop.

After cloning the repo, navigate there from the command-line:

```sh
cd ~/Desktop/robo-advisor
```

Create and activate a new Anaconda virtual environment:

```sh
conda create -n robo-env python=3.7 # (first time only)
conda activate robo-env
```

From within the virtual environment, install the required packages specified in the "requirements.txt" file:

```sh
pip install -r requirements.txt
```

In the directory, create a .env file.  In the .env file, add the following:

```sh
ALPHAVANTAGE_API_KEY="abc123"

#ADD TICKERS SEPARATED BY COMMA
INIT_TICKER_LIST="" # ="MSFT,IBM"
```

In the .env file, you MUST specify your API key (i.e., replacing abc123 in the text shown above).  You can obtain an API key from [AlphaVantage API](https://www.alphavantage.co).

In the .env file, you have the option to enter your desired list of tickers.  If initializing more than 1 ticker, please separate them using a comma to prevent errors.
When you run the program, you will have the opportunity to add more tickers.

From within the virtual environment, run the Python script from the command-line:

```sh
python app/robo_advisor.py
```
