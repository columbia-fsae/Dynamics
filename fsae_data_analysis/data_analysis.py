#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from helpers.graph import *
from helpers.dampers import *
from helpers.data import *
from helpers.roll import *
import sys
 
# total arguments
n = len(sys.argv)
if n > 2:
    print("Too many arguments, this script takes 1 filepath.")
 
front_track = 46.89*25.4 #mm
sprung_weight=613.9 #lb -- an assumption
rear_track =45.374*25.4 #mm
front_IR = 1.064 #spring/wheel
rear_IR=0.9033 #spring/wheel
wheelbase = 61 #in
front_wt_dist=0.499
rch=2 #in, roll center height
front_rch = 30.785/25.4 # in, front roll center height
rear_rch = 15.763/25.4 # in, rear roll center height
b = front_wt_dist*wheelbase
a = wheelbase-b

tot_weight = 713.9 #lb
cgh = 9.831 #in
center_rch = (abs(rear_rch-front_rch)/wheelbase)*b + rear_rch # watch out for signs here -- this works because our rear roll center is lower than the front


date = "4_28"
# pre-processing
df = process_analysis_data(sys.argv[1])

# for offset dampers
# ZERO offset		
# FL	3.15	mm
# FR	1.45	mm
# RL	-1.12	mm
# RR	-2.65	mm
#apply_damper_offset(df, 3.15, 1.45, -1.12, -2.65)
calc_damper_travel(df)
#calc_wheel_travel(df, front_IR, rear_IR)

# graph damper position
graph_damper_pos(df)

# wheel center v.s. time

# damper/wheel center velocity v.s. time
calc_damper_velocity(df)
#graph_damper_vel(df)
# histograms for damper velocity
graph_damper_vel_hist(df)

# wheel speed v.s. time
# might need to add virtual channel to convert this to km/h
graph_wheel_speed(df)

# g-g diagram
graph_gg(df)

# steering
graph_steer(df)
# throttle

# brake pressures, longitudinal slip
#graph_brake_pres(df)
#graph_long_slip(df)

# vehicle speed

# Ax and Ay vs. time
graph_a(df)

#roll :)
#calc_roll_angle(df, front_track, rear_track)
#graph_rollvtime(df)
#df_downsampled = filter_downsample_rollangle(df)
# left turns
#l_front_rg, l_rear_rg, l_total_rg = graph_left_turn_roll(df_downsampled, date)

# right turns
#r_front_rg, r_rear_rg, r_total_rg = graph_right_turn_roll(df_downsampled, date)

# roll stiffness
#m_roll = calc_roll_moment(cgh, center_rch, sprung_weight)
#KfrontL, KrearL, KtotL = calc_roll_stiffness(m_roll, l_front_rg, l_rear_rg, l_total_rg)
#KfrontR, KrearR, KtotR = calc_roll_stiffness(m_roll, r_front_rg, r_rear_rg, r_total_rg)

#print(KfrontL, KfrontR)
#print(KrearL, KrearR)
#print(KtotL, KtotR)
plt.show()