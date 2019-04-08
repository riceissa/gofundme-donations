#!/usr/bin/env python3

import requests
import json
import csv
import sys

import util

apikey = ""
with open("apikey.txt", "r") as f:
    apikey = next(f).strip()

payload = {"access_key": apikey, "symbols": "USD,GBP"}

# Find the dates for which we need currency conversion rates
date_list = []
with open(sys.argv[1], newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        donation_date = util.calc_donation_date(row['reference_date'],
                                                row['relative_donation_date'])
        date_list.append(donation_date.strftime("%Y-%m-%d"))
date_list = sorted(set(date_list))

data = []

for date_string in date_list:
        url = "http://data.fixer.io/api/" + date_string
        r = requests.get(url, params=payload)
        j = r.json()
        data.append(j)

with open("currency-data.json", "w") as f:
    json.dump(data, f, indent=4)
