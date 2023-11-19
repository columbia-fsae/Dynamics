import pandas as pd
import numpy as np

def apply_damper_offset(df, fl_offset, fr_offset, rl_offset, rr_offset):
    df["Damper Pos FL"] = df["Damper Pos FL"] + fl_offset
    df["Damper Pos FR"] = df["Damper Pos FR"] + fr_offset
    df["Damper Pos RL"] = df["Damper Pos RL"] + rl_offset
    df["Damper Pos RR"] = df["Damper Pos RR"] + rr_offset

def calc_damper_travel(df):
    
    df["Damper Pos FL Delta"]=df["Damper Pos FL"]-df["Damper Pos FL"][0]
    df["Damper Pos FR Delta"]=df["Damper Pos FR"]-df["Damper Pos FR"][0]
    df["Damper Pos RL Delta"]=df["Damper Pos RL"]-df["Damper Pos RL"][0]
    df["Damper Pos RR Delta"]=df["Damper Pos RR"]-df["Damper Pos RR"][0]


def calc_wheel_travel(df, front_IR, rear_IR):
    df["Wheel Center FL Delta"] = df["Damper Pos FL Delta"] * front_IR
    df["Wheel Center FR Delta"] = df["Damper Pos FR Delta"] * front_IR
    df["Wheel Center RL Delta"] = df["Damper Pos RL Delta"] * rear_IR
    df["Wheel Center RR Delta"] = df["Damper Pos RR Delta"] * rear_IR

def calc_damper_velocity(df):

    df["Damper Velocity FL"]=np.insert(np.diff(df["Damper Pos FL"])/np.diff(df["Time"]), 0, 0)
    df["Damper Velocity FR"]=np.insert(np.diff(df["Damper Pos FR"])/np.diff(df["Time"]), 0, 0)
    df["Damper Velocity RL"]=np.insert(np.diff(df["Damper Pos RL"])/np.diff(df["Time"]), 0, 0)
    df["Damper Velocity RR"]=np.insert(np.diff(df["Damper Pos RR"])/np.diff(df["Time"]), 0, 0)

    df["Damper Velocity FL (in)"] = df["Damper Velocity FL"]/25.4
    df["Damper Velocity FR (in)"] = df["Damper Velocity FR"]/25.4
    df["Damper Velocity RL (in)"] = df["Damper Velocity RL"]/25.4
    df["Damper Velocity RR (in)"] = df["Damper Velocity RR"]/25.4
