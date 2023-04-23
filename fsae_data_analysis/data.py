import pandas as pd

def process_data(csv_name, y_cols):
    df = pd.read_csv(csv_name, skiprows=14,low_memory=False)
    df = df.loc[:, y_cols]
    df = df.drop(df.iloc[[0]].index)
    df = df.reset_index()
    data_to_float(df)
    return df

def data_to_float(df):
    df[["Damper Pos FL", "Damper Pos FR","Damper Pos RL", "Damper Pos RR", "Time","Acceleration Y"]] = df[["Damper Pos FL", "Damper Pos FR","Damper Pos RL", "Damper Pos RR", "Time","Acceleration Y"]].astype(float)