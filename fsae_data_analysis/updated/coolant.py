"""Plots the data about the coolant temp, flow and pressure
Takes the csv file containing the test data as its first argument and ignores the rest
"""

import csv
import sys
import re

import numpy as np
import matplotlib.pyplot as plt

path = r"C:\Users\v2met9j\Downloads\11-01-23_garage_test.csv"

# row that contains the column names
header_row = 14
# row that contains the column units
unit_row = 15
# first row that contains data
data_row = 18

if len(sys.argv) > 1:
    path = sys.argv[1]

unit_dict = {"Time": "s"}
data_dict = {}

# regular expressions that define which columns are used in the program
extract_cols = [
    r"(^Time)",
    r"(Coolant Temperature)",
    r"(Coolant Pressure)",
    r"(GP Vol Flow)"
]

# complete regex of columns to extract
re_pat = re.compile("|".join(extract_cols))
col_flags = []

# determine number of data rows
with open(path) as readfile:
    n_rows = sum(1 for rows in readfile)-data_row
print("Number of data rows:", n_rows)

with open(path) as csvfile:
    reader = csv.reader(csvfile)

    # extract header and units row
    for row in range(data_row):
        if row == header_row:
            header = reader.__next__()
        elif row == unit_row:
            units = reader.__next__()
        else:
            reader.__next__()

    # define data dictionary with needed columns
    for i, j in enumerate(header):
        if re_pat.search(j):
            unit_dict[j] = units[i]
            data_dict[j] = np.empty(n_rows, dtype=float)
            col_flags.append(True)
        else:
            col_flags.append(False)
    
    columns = list(data_dict.keys())
    print("Extracted columns:", columns)

    # fill the data dict with the needed values
    for row, data in enumerate(reader):
        for col, field in enumerate(data):
            if not col_flags[col]:
                continue
            try:
                data_dict[header[col]][row] = float(field)
            except ValueError as v:
                fixed_field = field.replace(",", ".")
                data_dict[header[col]][row] = float(fixed_field)
            except Exception as e:
                print(type(e).__name__, "-", e)
                print(header[col], col)
                data_dict[header[col]][row] = 0

plt.rcParams["figure.figsize"] = (20, 20)
figure = 0

figure += 1
plt.figure(figure)
ax = plt.gca()
ax.set_title("Coolant Temperature")
ax.set_ylabel(f"Temperature [{unit_dict['Coolant Temperature']}]")
ax.set_xlabel(f"Time [{unit_dict['Time']}]")
coolant_temps = []
for col in columns:
    if "Coolant Temperature" not in col:
        continue
    ax.plot(data_dict["Time"], data_dict[col], label=col)
ax.legend()

figure += 1
plt.figure(figure)
ax = plt.gca()
ax.set_title("Coolant Pressure")
ax.set_ylabel(f"Pressure [{unit_dict['Coolant Pressure']}]")
ax.set_xlabel(f"Time [{unit_dict['Time']}]")
ax.plot(data_dict["Time"], data_dict["Coolant Pressure"])

figure += 1
plt.figure(figure)
ax = plt.gca()
ax.set_title("Coolant Flow")
ax.set_ylabel(f"Flow [{unit_dict['GP Vol Flow 1']}]")
ax.set_xlabel(f"Time [{unit_dict['Time']}]")
ax.plot(data_dict["Time"], data_dict["GP Vol Flow 1"])

plt.show()
