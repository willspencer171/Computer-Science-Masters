import pandas as pd
import numpy as np
import arff


def subtract_1_day(match):
    """Reduces the number of days by one to account for dates of birth that are invalid"""
    days = int(match.group(1))
    return str(days - 1)


data = arff.load(open("Week 2/gcse.arff", "r"), True)

headers, dtypes = zip(*data["attributes"])

missing_vals = [" ", "1", "4", "K", "N"]
incorrect_vals = {"A+": "A*", "mf": "x"}

df = pd.DataFrame(data["data"], columns=headers).convert_dtypes()

df = df.replace(missing_vals, np.nan).replace(incorrect_vals)

# This deals with any datetimes that aren't valid (e.g. 1977/2/29 - not a leap year)
tempdate = pd.to_datetime(df["dob"], format="mixed", errors="coerce")
fixed_dates = df.loc[tempdate.isna(), "dob"].str.replace(
    r"(?<=/)(\d+)(?=/)", subtract_1_day, regex=True
)
tempdate.update(pd.to_datetime(fixed_dates, format="mixed"))

df["dob"] = tempdate

print(df.isnull().sum())

print(df["gender"].unique())
