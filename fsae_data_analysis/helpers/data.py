import pandas as pd
import numpy as np

def process_analysis_data(csv_name):
    y_cols = ["Time","G Force Long", "G Force Lat", "G Force Vert", "Damper Pos FL", "Damper Pos FR", "Damper Pos RL", "Damper Pos RR", "Wheel Speed FL", "Wheel Speed FR", "Wheel Speed RL", "Wheel Speed RR", "Steering Wheel Angle", "Brake Pressure Front","Brake Pressure Rear"]
    df = pd.read_csv(csv_name, skiprows=14,low_memory=False)
    df = df.loc[:, y_cols]
    df = df.drop(df.iloc[[0]].index)

    df = df[df["Time"].astype(float) > 1300]
    df = df[df["Time"].astype(float) < 1400]
    df = df.reset_index()
    df = df.astype(np.float64)

    # processing + channel math :')
    process_2023_data(df)
    return df

def process_battery_data(csv_name):
    df = pd.read_csv(csv_name, skiprows=14,low_memory=False)
    df = df.filter(regex='Battery Temp|Battery Voltage|Time')

    df = df.drop(df.iloc[[0]].index)
    df = df[df["Time"].astype(float) > 1300]
    df = df[df["Time"].astype(float) < 1400]

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
