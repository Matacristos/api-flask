import csv
import datetime
import os
import requests
import time

print("Starting")
start = 1577437200000
end = int(round(time.time() * 1000))
product_code = 'BTC_USD'
output = f'data/bitcoin.csv'

url = f"https://bitflyer.com/api/trade/chartdata?product_code={product_code}&start={start}&end={end}"

r = requests.get(url)
print(f"got response: {r.status_code} from {url}")
data = r.json()

if not os.path.exists('output'):
    os.makedirs('my_folder')
wtr = csv.writer(open(output, 'w'), delimiter=',', lineterminator='\n')
for row in data:
    date = datetime.datetime.fromtimestamp(row[0]/1000.0)
    date = date.strftime("%Y-%m-%d %H:%M")
    wtr.writerow([date, product_code, row[1]])

print(f"finished, check file: {output}")
