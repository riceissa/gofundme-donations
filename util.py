#!/usr/bin/env python3

import datetime


def calc_donation_date(reference_date, relative_donation_date):
    ref_date = datetime.datetime.strptime(reference_date, "%Y-%m-%d")
    quantity, unit, ago = relative_donation_date.split()
    assert ago == "ago"
    if unit == "days":
        return ref_date - datetime.timedelta(days=int(quantity))
    elif unit == "months":
        ref_month = ref_date.month
        back_months = int(quantity)  # Number of months to go back in time

        # Each 12-month grouping means we should go back an extra year
        target_year = ref_date.year - (back_months // 12)
        # After we go back in years via 12-month groupings, we might still need
        # to go back an extra year. To see this, suppose the month is April,
        # and we need to go back 30 months. After we go back 30 // 12 = 2 years,
        # we still need to go back 6 more months. But April (month 4) <= 6 months
        # (i.e. we will wrap past the December/January divide), so we must go
        # back an extra year.
        if back_months % 12 >= ref_month:
            target_year -= 1

        target_month = (ref_month - back_months) % 12
        if target_month == 0:
            target_month = 12

        return datetime.date(target_year, target_month, ref_date.day)
    else:
        raise ValueError("We don't know this unit of time: " + str(unit))
