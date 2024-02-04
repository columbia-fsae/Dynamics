import pandas as pd
import numpy as np
from pyarrow import csv

def process_analysis_data(csv_name):
    df = csv.read_csv(csv_name, csv.ReadOptions(skip_rows = 14)).to_pandas()
    df = df.filter(regex='Time|G Force|Damper Pos|Wheel Speed|Steering Wheel Angle|Wheel Center|Brake Pressure|Torque|Battery|Coolant|GP Vol Flow')
    df = df.drop(df.iloc[[0]].index)
    # df = df[df["Time"].astype(float) > 1050]
    # df = df[df["Time"].astype(float) < 2600]
    df = df.reset_index()
    df = df.astype(np.float64)

    # processing + channel math :')
    process_2023_data(df)
    return df

def process_battery_data(csv_name):
    df = pd.read_csv(csv_name, skiprows=14,low_memory=False)
    df = df.filter(regex='Battery Temp|Battery Voltage|Time')
    df = df.drop(df.iloc[[0]].index)
    # df = df[df["Time"].astype(float) > 1050]
    # df = df[df["Time"].astype(float) < 2600]
    df = df.reset_index()
    df = df.astype(np.float64)
    return df

def process_2023_data(df):
    df["G Force Long"] = -1 * df["G Force Long"]
    try:
        df["Ground Speed"] = df["Ground Speed"].astype(float)
    except:
        df["Ground Speed"] = df[["Wheel Speed FL","Wheel Speed FR"]].max(axis=1).astype(float)

    df["Brake Bias"] = df["Brake Pressure Front"]/(df["Brake Pressure Front"]+df["Brake Pressure Rear"])
    df["Corner Radius"] = (df["Ground Speed"].pow(2))/df["G Force Lat"]
    df["Longitudinal Slip RR"] = (df["Wheel Speed RR"] - df["Ground Speed"])/df["Ground Speed"]
    df["Longitudinal Slip RL"] = (df["Wheel Speed RL"] - df["Ground Speed"])/df["Ground Speed"]
