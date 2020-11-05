import requests
import pytz
import sys
import os
import csv
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from time import sleep
from random import randint
 

URL = "https://production.api.coindesk.com/v2/price/values/"

COIN = "BTC"
API_TIMEZONE = pytz.timezone("Europe/Madrid")
CODE = f"{COIN}_USD"
DATA_FOLDER = "data"
DATA_FILE = "bitcoin.csv"
DATA_PATH = os.path.join(DATA_FOLDER, DATA_FILE)


DEFAULT_START_DATE = datetime.now(tz=API_TIMEZONE) - relativedelta(month=1)
DEFAULT_END_DATE = datetime.now(tz=API_TIMEZONE) 


def wait():
    sleep_seconds = randint(5,7)
    sleep(sleep_seconds)


def write_dataframe_to_csv(dataframe, path=DATA_PATH):
    index_col = "Date"
    dataframe = dataframe.drop_duplicates(index_col).sort_values(by=[index_col])
    return dataframe.to_csv(path, sep=',', line_terminator='\n', index=False)

def read_dataframe_from_csv(path=DATA_PATH):
    return pd.read_csv(path, sep=',')

def dates_query_params(start_date, end_date):
    return f"start_date={start_date}&end_date={end_date}"


def fetch_hourly_between_dates(start_date=DEFAULT_START_DATE, end_date=DEFAULT_END_DATE):
    try:
        start_date = start_date.strftime("%Y-%m-%dT%H:%m")
        end_date = end_date.strftime("%Y-%m-%dT%H:%m")

        date_param = dates_query_params(start_date, end_date)
        fetch_url = f"{URL}{COIN}?{date_param}"

        print(fetch_url)
        response = requests.get(fetch_url)

        data =  response.json().get("data")
        return data
    except:
        print("Cannot fetch more data")
        return


def format_timestamp(timestamp):
    datetime_wo_timezone = datetime.fromtimestamp(timestamp//1000.0)
    datetime_localized = API_TIMEZONE.localize(datetime_wo_timezone)
    return datetime_localized.strftime("%Y-%m-%d %H:%M")


def parse_response_data(entries, **kwargs):
    if not entries:
        raise ValueError("No entries provided")

    entries = [(format_timestamp(ts), price) for ts, price, *r in entries]
    return entries

def run_between_dates(start_date, end_date):
    raw_data = fetch_hourly_between_dates(start_date, end_date)
    if raw_data:
        parsed_data = parse_response_data(**raw_data)
        return parsed_data  # return list of lists
    else:
        return []
    
def run_monthly(end_date):
    #print((end_date - relativedelta(months=1), end_date))
    return run_between_dates(end_date - relativedelta(months=1), end_date)

def run_for_last_n_months(n_months=1):
    data = []
    for n in range(n_months):
        data.extend(run_monthly(
            DEFAULT_END_DATE - relativedelta(months=n)
        ))
        wait()

    return data

def populate():
    n_months = 24
    #n_months = 3
    records = run_for_last_n_months(n_months)
    dataframe = pd.DataFrame.from_records(records, columns=['Date', 'Close'])
    write_dataframe_to_csv(dataframe)


def check_data():
    df = read_dataframe_from_csv()
    
    for index in range(len(df)):
        try:
            start = pd.to_datetime(df['Date'][index])
            end = pd.to_datetime(df['Date'][index+1])
            diff_seconds = (end - start).total_seconds()
            diff_expected = 3600.0
            #if diff_seconds != diff_expected:
            if diff_seconds < diff_expected - 100 or diff_seconds > diff_expected + 100:
                print(f"Error diffing datetime <{diff_seconds}> between {index}-{index+1}")
        except KeyError:
            return
        except Exception as e:
            raise e

def update():
    # read latest_data
    df = read_dataframe_from_csv()

    # latest_date = pd.to_datetime(df["datetime"].iloc[-1]).to_pydatetime()
    # get latest_date
    # get time_diff
    # (if time_diff > 1 month)
    # n_months between latest_date and now 
    # fetch latest_n_months

    # else fetch between dates(latest_date, now)
    records = run_monthly(DEFAULT_END_DATE)
    dataframe = df.append(pd.DataFrame.from_records(records, columns=['Date', 'Close']))
    print(dataframe.tail())
    write_dataframe_to_csv(dataframe)


def print_help():
    print(f"Usage: {sys.argv[0]} <command>")
    print("Commands: \n\t populate: populate data \n\t update: fetch latest data \n\t check: check current data for failing rows")

if __name__ == "__main__":

    try:
        cmd = sys.argv[1]
    except:
        print_help()
        exit(1)

    if cmd == "populate":
        populate()

    if cmd == "update":
        update()

    if cmd == "check":
        check_data()
