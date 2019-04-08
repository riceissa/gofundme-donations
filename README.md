# gofundme donations

This is for Vipul Naik's Donations List Website:
https://github.com/vipulnaik/donations/
https://donations.vipulnaik.com/

Specific issue that prompted the creation of this repo:
https://github.com/vipulnaik/donations/issues/113

## Instructions for using the scripts

Get the donations data:

```bash
# the general syntax is: ./scrape.py GOFUNDME_SLUG > OUT_FILE
./scrape.py "ea-hotel" > ea-hotel-data.csv
```

If the gofundme page of interest uses a currency other than USD, get currency data:

```bash
# the general syntax is: ./get_currency_data.py DONATIONS_CSV_FILE SOURCE_CURRENCY > OUT_FILE
# NOTE: to run this script, you will need a Fixer.io API key stored at apikey.txt
./get_currency_data.py ea-hotel-data.csv "GBP" > ea-hotel-currency-data.json
```

Run processing script to generate a SQL file:

```bash
# the general syntax is: ./proc.py
./proc.py
```

## License

CC0.
