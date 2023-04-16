import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# just for graph colors
from itertools import cycle
cycol = cycle('bgrcmk')

global fig_id
fig_id = 0
# graph damper position:
def graph_damper_pos(df):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)

    damperPosCols = ["Damper Pos FL", "Damper Pos FR", "Damper Pos RL", "Damper Pos RR"]
    for col in damperPosCols:
        y = df[col].astype(float)
        ax = plt.gca()
        ax.plot(df["Time"].astype(float), y, markersize=5, label = col, color=next(cycol))
    
    plt.xlabel("Time (s)")
    plt.ylabel("Damper Pos (mm)")
    plt.title("Damper Pos" + " v.s. Time")

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# graph damper velocity:
def graph_damper_vel(df):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)

    damperVelCols = ["Damper Velocity FL (in)", "Damper Velocity FR (in)", "Damper Velocity RL (in)", "Damper Velocity RR (in)"]
    for col in damperVelCols:
        y = df[col].astype(float)
        ax = plt.gca()
        ax.plot(df["Time"].astype(float), y, markersize=5, label = col, color=next(cycol))
    
    plt.xlabel("Time (s)")
    plt.ylabel("Damper Vel (in/s)")
    plt.title("Damper Velocity" + " v.s. Time")

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

def graph_damper_vel_hist(df):
    graph_histogram(df, "Damper Velocity FL (in)")
    graph_histogram(df, "Damper Velocity FR (in)")
    graph_histogram(df, "Damper Velocity RL (in)")
    graph_histogram(df, "Damper Velocity RR (in)")


# graph steering wheel angle
def graph_steer(df):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)

    y = df["Steering Wheel Angle"].astype(float)
    ax = plt.gca()
    ax.plot(df["Time"].astype(float), y, color=next(cycol))
    plt.xlabel("Time (s)")
    plt.ylabel("Steering Wheel Angle (def)")
    plt.title("Steering Wheel Angle v.s. Time")


# graph the g-g diagram
def graph_gg(df):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)

    # make sure that these are the right ones, may need to flip signs/axes etc.
    ayCol = "G Force Lat"
    axCol = "G Force Vert"
    y = df[axCol].astype(float)
    ax = plt.gca()
    ax.scatter(df[ayCol].astype(float), y, marker = ".", s = 5, color=next(cycol))
    plt.xlabel("Ay (g)")
    plt.ylabel("Ax (g)")
    plt.title("g-g Diagram")

# graph ax v.s. time
def graph_a(df):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)

    aCols = ["G Force Vert", "G Force Lat"]
    for col in aCols:
        y = df[col].astype(float)
        ax = plt.gca()
        ax.plot(df["Time"].astype(float), y, markersize=5, label = col, color=next(cycol))
    
    plt.xlabel("Time (s)")
    plt.ylabel("Accel (g)")
    plt.title("Accel" + " v.s. Time")

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# graph wheel speed:
def graph_wheel_speed(df):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)

    wheelSpeedCols = ["Wheel Speed FL", "Wheel Speed FR", "Wheel Speed RL", "Wheel Speed RR"]
    for col in wheelSpeedCols:
        y = df[col].astype(float)
        ax = plt.gca()
        ax.plot(df["Time"].astype(float), y, markersize=5, label = col, color=next(cycol))
    
    plt.xlabel("Time (s)")
    plt.ylabel("Wheel Speed (km/h))")
    plt.title("Wheel Speed" + " v.s. Time")

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


def graph_histogram(df, col):
    bins = []
    for i in range(-20, 21):
        bins.append(i)
    ax = df.hist(column=col, bins=bins, grid=False, color='#86bf91', zorder=2, rwidth=0.9)
    ax = ax[0]
    for x in ax:
        # Despine
        x.spines['right'].set_visible(False)
        x.spines['top'].set_visible(False)
        x.spines['left'].set_visible(False)

        # Switch off ticks
        x.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")

        # Draw horizontal axis lines
        vals = x.get_yticks()
        for tick in vals:
            x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)

        # Remove title
        x.set_title(col + " Frequency")

        # Set x-axis label
        x.set_xlabel(col, labelpad=20, weight='bold', size=12)

        # Set y-axis label
        x.set_ylabel("Frequency", labelpad=20, weight='bold', size=12)

        # Format y-axis label
        #x.yaxis.set_major_formatter(StrMethodFormatter('{x:,g}'))