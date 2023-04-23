import pandas as pd
import numpy as np

def process_data(csv_name):
    y_cols = ["Time","G Force Long", "G Force Lat", "G Force Vert", "Damper Pos FL", "Damper Pos FR", "Damper Pos RL", "Damper Pos RR", "Wheel Speed FL", "Wheel Speed FR", "Wheel Speed RL", "Wheel Speed RR", "Steering Wheel Angle", "Brake Pres Front","Brake Pres Rear"]
    df = pd.read_csv(csv_name, skiprows=14,low_memory=False)
    df = df.loc[:, y_cols]
    df = df.drop(df.iloc[[0]].index)
    df = df.reset_index()
    data_to_float(df)

    # processing + channel math :')
    process_2023_data(df)

    return df

def process_2023_data(df):
    df["G Force Long"] = -1 * df["G Force Long"]
    df["Vehicle Speed"] = df[["Wheel Speed FL","Wheel Speed FR"]].max(axis=1).astype(float)
    df["Brake Bias"] = df["Brake Pres Front"]/(df["Brake Pres Front"]+df["Brake Pres Rear"])
    df["Corner Radius"] = (df["Vehicle Speed"].pow(2))/df["G Force Lat"]
    df["Longitudinal Slip RR"] = (df["Wheel Speed RR"] - df["Vehicle Speed"])/df["Vehicle Speed"]
    df["Longitudinal Slip RL"] = (df["Wheel Speed RL"] - df["Vehicle Speed"])/df["Vehicle Speed"]

def data_to_float(df):
    to_float = ["Damper Pos FL", "Damper Pos FR","Damper Pos RL", "Damper Pos RR", "Time","G Force Lat","G Force Long","Brake Pres Front","Brake Pres Rear", "Wheel Speed FL", "Wheel Speed FR", "Wheel Speed RL", "Wheel Speed RR"]
    df[to_float] = df[to_float].astype(float)