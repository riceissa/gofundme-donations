#!/usr/bin/env python3

import csv
import sys
import json

import util

with open(sys.argv[2], "r") as f:
    CURRENCY_TABLE = json.load(f)


def main():
    print("""insert into donations (donor, donee, amount, donation_date, donation_date_precision, donation_date_basis, cause_area, url, notes, amount_original_currency, original_currency, currency_conversion_date, currency_conversion_basis) values""")
    first = True

    with open(sys.argv[1], newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            donation_date = util.calc_donation_date(row['reference_date'],
                                                    row['relative_donation_date']).strftime("%Y-%m-%d")
            _, unit, ago = row['relative_donation_date'].split()
            assert ago == "ago"
            if unit == "days" or unit == "day":
                donation_date_precision = "day"
            elif unit == "months" or unit == "month":
                donation_date_precision = "month"

            assert row["amount"].startswith("£")
            original_amount = float(row["amount"].replace("£", "").replace(",", ""))
            amount = currency_to_usd(original_amount, "GBP", donation_date)
            print(("    " if first else "    ,") + "(" + ",".join([
                mysql_quote(row["donor_name"]),  # donor
                mysql_quote("EA Hotel"),  # donee
                str(amount),  # amount
                mysql_quote(donation_date),  # donation_date
                mysql_quote(donation_date_precision),  # donation_date_precision
                mysql_quote("donation log"),  # donation_date_basis
                mysql_quote("Effective altruism/movement growth"),  # cause_area
                mysql_quote("https://www.gofundme.com/ea-hotel"),  # url
                mysql_quote(""),  # notes
                str(original_amount),  # amount_original_currency
                mysql_quote("GBP"),  # original_currency
                mysql_quote(donation_date),  # currency_conversion_date
                mysql_quote("Fixer.io"),  # currency_conversion_basis
            ]) + ")")


def mysql_quote(x):
    """Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    our input is fixed and from a basically trustable source."""
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)


def currency_to_usd(original_amount, original_currency, date):
    for conv in CURRENCY_TABLE:
        if conv["date"] == date:
            # Since the free version of Fixer.io only supports EUR as the base
            # currency, we have to first convert to EUR, then to USD
            eur_amount = original_amount / conv["rates"][original_currency]
            usd_amount = eur_amount * conv["rates"]["USD"]
            return usd_amount


if __name__ == "__main__":
    main()
