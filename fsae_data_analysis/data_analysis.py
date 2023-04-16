import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from graph import *
from dampers import *
from data import *

# front_track = 48*25.4 #mm
# sprung_weight=217.72*2.2 #lb
# rear_track =46 * 25.4 #mm
front_IR = 1.064 #spring/wheel
rear_IR=0.9033 #spring/wheel
# wheelbase = 61 #in
# front_wt_dist=0.455
# rch=2 #in, roll center height
# tot_weight = 720 #lb
# cgh = 10 #in


# pre-processing
y_cols = ["Time","G Force Lat", "G Force Long", "G Force Vert", "Damper Pos FL", "Damper Pos FR", "Damper Pos RL", "Damper Pos RR", "Wheel Speed FL", "Wheel Speed FR", "Wheel Speed RL", "Wheel Speed RR", "Steering Wheel Angle"]
df = process_data('4_28_autoX.csv', y_cols)
data_to_float(df)

# for offset dampers
# ZERO offset		
# FL	3.15	mm
# FR	1.45	mm
# RL	-1.12	mm
# RR	-2.65	mm
apply_damper_offset(df, 3.15, 1.45, -1.12, -2.65)
calc_damper_travel(df)
calc_wheel_travel(df, front_IR, rear_IR)

# graph damper position
graph_damper_pos(df)

# wheel center v.s. time

# damper/wheel center velocity v.s. time
calc_damper_velocity(df)
graph_damper_vel(df)
# histograms for damper velocity
graph_damper_vel_hist(df)

# wheel speed v.s. time
# might need to add virtual channel to convert this to km/h
#graph_wheel_speed(df)

# g-g diagram
#graph_gg(df)

# steering
#graph_steer(df)
# throttle

# brake

# vehicle speed

# Ax and Ay vs. time
#graph_a(df)

plt.show()