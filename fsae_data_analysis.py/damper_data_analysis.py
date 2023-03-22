import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from helpers import *

df = pd.read_csv('damper_data_example_4_18_2018.csv') # this may need more processing in the future
print(df)

# pre-processing
y_cols = ["Time","G Force Lat", "G Force Long", "G Force Vert", "Damper Pos FL", "Damper Pos FR", "Damper Pos RL", "Damper Pos RR", "Wheel Speed FL", "Wheel Speed FR", "Wheel Speed RL", "Wheel Speed RR", "Steering Wheel Angle"]
x_col = "Motion [Heave] (mm)" 

df = df.loc[:, y_cols]
df = df.drop(df.iloc[[0, 1, 2]].index)

print(df)

# for offset dampers
# ZERO offset		
# FL	3.15	mm
# FR	1.45	mm
# RL	-1.12	mm
# RR	-2.65	mm
df["Damper Pos FL"] = df["Damper Pos FL"].astype(float)+ 3.15
df["Damper Pos FR"] = df["Damper Pos FR"].astype(float) + 1.45
df["Damper Pos RL"] = df["Damper Pos RL"].astype(float) - 1.12
df["Damper Pos RR"] = df["Damper Pos RR"].astype(float) - 2.65

# graph damper position
graph_damper_pos(df)

# convert to wheel center? -- we should try and add virtual channels for that in MoTeC
# motion ratio defined as wheel travel/damper travel
f_mr = 0.89
r_mr = 1.11

# this is not right -- need to adjust by height of wheel
df["Wheel Center FL"] = df["Damper Pos FL"].astype(float) * f_mr
df["Wheel Center FR"] = df["Damper Pos FR"].astype(float) * f_mr
df["Wheel Center RL"] = df["Damper Pos RL"].astype(float) * r_mr
df["Wheel Center RR"] = df["Damper Pos RR"].astype(float) * r_mr

# wheel center v.s. time

# damper/wheel center velocity v.s. time

for i in range(1, len(df["Damper Pos FL"]))
    df["Damper Speed FL"] = df["Damper Pos FL"].astype(float)



# histograms for damper velocity

# wheel speed v.s. time
# might need to add virtual channel to convert this to km/h
graph_wheel_speed(df)

# g-g diagram
graph_gg(df)

# steering
graph_steer(df)
# throttle

# brake

# vehicle speed

# Ax and Ay vs. time
graph_a(df)

plt.show()