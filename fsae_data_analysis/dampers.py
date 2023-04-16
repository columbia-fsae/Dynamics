import pandas as pd

def apply_damper_offset(df, fl_offset, fr_offset, rl_offset, rr_offset):
    df["Damper Pos FL"] = df["Damper Pos FL"] + fl_offset
    df["Damper Pos FR"] = df["Damper Pos FR"] + fr_offset
    df["Damper Pos RL"] = df["Damper Pos RL"] + rl_offset
    df["Damper Pos RR"] = df["Damper Pos RR"] + rr_offset

def calc_damper_travel(df):
    damper_fl_delta = []
    for i in range(0, len(df["Damper Pos FL"])):
        damper_fl_delta.append(df["Damper Pos FL"][i]-df["Damper Pos FL"][0])
    df["Damper Pos FL Delta"]=damper_fl_delta

    damper_fr_delta = []
    for i in range(0, len(df["Damper Pos FR"])):
        damper_fr_delta.append(df["Damper Pos FR"][i]-df["Damper Pos FR"][0])
    df["Damper Pos FR Delta"]=damper_fr_delta

    damper_rl_delta = []
    for i in range(0, len(df["Damper Pos RL"])):
        damper_rl_delta.append(df["Damper Pos RL"][i]-df["Damper Pos RL"][0])
    df["Damper Pos RL Delta"]=damper_rl_delta

    damper_rr_delta = []
    for i in range(0, len(df["Damper Pos RR"])):
        damper_rr_delta.append(df["Damper Pos RR"][i]-df["Damper Pos RR"][0])
    df["Damper Pos RR Delta"]=damper_rr_delta


def calc_wheel_travel(df, front_IR, rear_IR):
    df["Wheel Center FL Delta"] = df["Damper Pos FL Delta"] * front_IR
    df["Wheel Center FR Delta"] = df["Damper Pos FR Delta"] * front_IR
    df["Wheel Center RL Delta"] = df["Damper Pos RL Delta"] * rear_IR
    df["Wheel Center RR Delta"] = df["Damper Pos RR Delta"] * rear_IR

def calc_damper_velocity(df):
    damper_fl_velocity = []
    damper_fl_velocity.append(0) # set initial value
    for i in range(1, len(df["Damper Pos FL"])):
        inst_vel = (df["Damper Pos FL"][i]-df["Damper Pos FL"][i-1])/(df["Time"][i]-df["Time"][i-1])
        damper_fl_velocity.append(inst_vel)
    df["Damper Velocity FL"]=damper_fl_velocity

    damper_fr_velocity = []
    damper_fr_velocity.append(0) # set initial value
    for i in range(1, len(df["Damper Pos FR"])):
        inst_vel = (df["Damper Pos FR"][i]-df["Damper Pos FR"][i-1])/(df["Time"][i]-df["Time"][i-1])
        damper_fr_velocity.append(inst_vel)
    df["Damper Velocity FR"]=damper_fr_velocity

    damper_rl_velocity = []
    damper_rl_velocity.append(0) # set initial value
    for i in range(1, len(df["Damper Pos RL"])):
        inst_vel = (df["Damper Pos RL"][i]-df["Damper Pos RL"][i-1])/(df["Time"][i]-df["Time"][i-1])
        damper_rl_velocity.append(inst_vel)
    df["Damper Velocity RL"]=damper_rl_velocity

    damper_rr_velocity = []
    damper_rr_velocity.append(0) # set initial value
    for i in range(1, len(df["Damper Pos RR"])):
        inst_vel = (df["Damper Pos RR"][i]-df["Damper Pos RR"][i-1])/(df["Time"][i]-df["Time"][i-1])
        damper_rr_velocity.append(inst_vel)
    df["Damper Velocity RR"]=damper_rr_velocity

    df["Damper Velocity FL (in)"] = df["Damper Velocity FL"]/25.4
    df["Damper Velocity FR (in)"] = df["Damper Velocity FR"]/25.4
    df["Damper Velocity RL (in)"] = df["Damper Velocity RL"]/25.4
    df["Damper Velocity RR (in)"] = df["Damper Velocity RR"]/25.4
