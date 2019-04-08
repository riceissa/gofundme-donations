#!/usr/bin/env python3

import requests
import re
import sys
import csv
import datetime
from bs4 import BeautifulSoup

import pdb

def main():
    fieldnames = ["donor_name", "amount", "current_date", "relative_donation_date"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()

    url_pattern = "https://www.gofundme.com/mvc.php?route=donate/pagingDonationsFoundation&url={}&idx={}&type=recent"
    has_more_donations = True
    idx = 0  # Keeps track of how many donations we have seen; this should go 0, 10, 20, ...
    while has_more_donations:
        # sys.argv[1] should be the slug of the GoFundMe donee, e.g. "ea-hotel"
        url = url_pattern.format(sys.argv[1], idx)
        print("Downloading from " + url, file=sys.stderr)
        response = requests.get(url,
                                headers={'User-Agent': 'Mozilla/5.0 '
                                         '(X11; Linux x86_64) AppleWebKit/537.36 '
                                         '(KHTML, like Gecko) '
                                         'Chrome/63.0.3239.132 Safari/537.36'})
        soup = BeautifulSoup(response.content, "lxml")

        # Loop through the donations listed on the current page, saving them to
        # a CSV file
        num_donations_on_page = 0
        for supporter in soup.find_all("div", {"class": "supporter"}):
            donor_name = supporter.find("a", {"class": "supporter-name"})
            # Anonymous donors aren't linked using an <a> tag, so look for a
            # <div> instead
            if donor_name is None:
                donor_name = supporter.find("div", {"class": "supporter-name"})
            donor_name = donor_name.text
            amount = supporter.find("div", {"class": "supporter-amount"}).text
            relative_donation_date = supporter.find("div", {"class": "supporter-time"}).text
            writer.writerow({
                "donor_name": donor_name,
                "amount": amount,
                "current_date": datetime.date.today().strftime("%Y-%m-%d"),
                "relative_donation_date": relative_donation_date,
            })
            num_donations_on_page += 1

        # Now we use the footer to determine whether we need to continue
        # getting the next page
        footer_lines = soup.find("div", {"class": "donations-control-footer"}).text.split("\n")
        # The following (converted to a list) should look like
        # ['See More', 'See More', 'Viewing 10 of 18 Donations']
        nonblank_lines = filter(bool, map(str.strip, footer_lines))
        # The following should look like ['Viewing 10 of 18 Donations']
        lst = list(filter(lambda x: x.startswith("Viewing"), nonblank_lines))
        assert len(lst) == 1
        match = re.match(r"Viewing (\d+) of (\d+) Donations$", lst[0])
        print(lst[0], file=sys.stderr)
        if int(match.group(1)) == int(match.group(2)):
            has_more_donations = False
        idx += num_donations_on_page


if __name__ == "__main__":
    main()
