import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

# just for graph colors
from itertools import cycle
cycol = cycle('bgrcmk')

global fig_id
fig_id = 0


# graph damper position:
def graph_damper_pos(df, saveFig=False, testName=""):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)
    ax = plt.gca()

    damperPosCols = ["Damper Pos FL", "Damper Pos FR", "Damper Pos RL", "Damper Pos RR"]
    for col in damperPosCols:
        y = df[col].astype(float)
        ax = plt.gca()
        ax.plot(df["Time"].astype(float), y, markersize=2, label = col, color=next(cycol))
    
    plt.xlabel("Time (s)")
    plt.ylabel("Damper Pos (mm)")
    plt.title("Damper Pos" + " v.s. Time")

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    if saveFig:
        plt.tight_layout()
        plt.savefig("./outputs/%s_damper_pos.png" % df.name, bbox_inches='tight')

# graph damper velocity:
def graph_damper_vel(df, saveFig=False):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)
    ax = plt.gca()

    damperVelCols = ["Damper Velocity FL (mm)", "Damper Velocity FR (mm)", "Damper Velocity RL (mm)", "Damper Velocity RR (mm)"]
    for col in damperVelCols:
        y = df[col].astype(float)
        ax.plot(df["Time"].astype(float), y, markersize=5, label = col, color=next(cycol))
    
    plt.xlabel("Time (s)")
    plt.ylabel("Damper Vel (mm/s)")
    plt.title("Damper Velocity" + " v.s. Time")

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    if saveFig:
        plt.tight_layout()
        plt.savefig("./outputs/%s_damper_vel.png" % df.name, bbox_inches='tight')


# graph steering wheel angle
def graph_steer(df, saveFig=False):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)

    y = df["Steering Wheel Angle"].astype(float)
    ax = plt.gca()
    ax.plot(df["Time"].astype(float), y, color=next(cycol))
    plt.xlabel("Time (s)")
    plt.ylabel("Steering Wheel Angle (def)")
    plt.title("Steering Wheel Angle v.s. Time")
    if saveFig:
        plt.tight_layout()
        plt.savefig("./outputs/%s_steer_angle.png" % df.name, bbox_inches='tight')


# graph the g-g diagram
def graph_gg(df, saveFig=False):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)

    # make sure that these are the right ones, may need to flip signs/axes etc.
    ayCol = "G Force Lat"
    axCol = "G Force Long"
    y = df[axCol]
    ax = plt.gca()
    ax.scatter(df[ayCol], y, marker = ".", s = 5, color=next(cycol))
    plt.xlabel("Ay (g)")
    plt.ylabel("Ax (g)")
    plt.title("g-g Diagram")
    if saveFig:
        plt.tight_layout()
        plt.savefig("./outputs/%s_gg.png" % df.name, bbox_inches='tight')

# graph ax v.s. time
def graph_a(df, saveFig=False):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)
    ax = plt.gca()

    aCols = ["G Force Long", "G Force Lat"]
    for col in aCols:
        y = df[col]
        ax.plot(df["Time"], y, markersize=5, label = col, color=next(cycol))
    
    plt.xlabel("Time (s)")
    plt.ylabel("Accel (g)")
    plt.title("Accel" + " v.s. Time")

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    if saveFig:
        plt.tight_layout()
        plt.savefig("./outputs/%s_accel.png" % df.name, bbox_inches='tight')

# graph wheel speed:
def graph_wheel_speed(df, saveFig=False):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)
    ax = plt.gca()

    wheelSpeedCols = ["Wheel Speed FL", "Wheel Speed FR", "Wheel Speed RL", "Wheel Speed RR"]
    for col in wheelSpeedCols:
        y = df[col].to_numpy()
        ax.plot(df["Time"], y, markersize=5, label = col, color=next(cycol))

    plt.xlabel("Time (s)")
    plt.ylabel("Wheel Speed (km/h)")
    plt.title("Wheel Speed" + " v.s. Time")

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    if saveFig:
        plt.tight_layout()
        plt.savefig("./outputs/%s_wheel_speed.png" % df.name, bbox_inches='tight')


def graph_damper_vel_hist(df, saveFig=False):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)

    fig, ((ax1, ax2),(ax3, ax4)) = plt.subplots(2, 2, num=fig_id)
    graph_histogram(df, "Damper Velocity FL (in)",axes = ax1)
    graph_histogram(df, "Damper Velocity FR (in)",axes = ax2)
    graph_histogram(df, "Damper Velocity RL (in)",axes = ax3)
    graph_histogram(df, "Damper Velocity RR (in)",axes = ax4)
    if saveFig:
        plt.tight_layout()
        plt.savefig("./outputs/%s_damper_vel.png" % df.name, bbox_inches='tight')


def graph_histogram(df, col, axes, saveFig=False):
    bins = []
    for i in range(-20, 21):
        bins.append(i)
    x = df.hist(column=col, bins=bins, grid=False, ax = axes, color='#86bf91', zorder=2, rwidth=0.9)
        # Despine

    # print(x)
    x = x[0]
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
    x.set_xlabel(col, labelpad=10, size=12)

    # Set y-axis label
    x.set_ylabel("Frequency", labelpad=10, size=12)
    # Format y-axis label
    # x.yaxis.set_major_formatter(StrMethodFormatter('{x:,g}'))


def graph_left_turn_roll(df, date, saveFig=False):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)

    left_turns_i = df.index[df["G Force Lat (downsampled)"].astype(float)<0].tolist()
    accel_left = (df["G Force Lat (downsampled)"].iloc[left_turns_i]).astype(float)
    left_roll_front = df["Front Roll Angle (downsampled)"].iloc[left_turns_i]
    left_roll_rear = df["Rear Roll Angle (downsampled)"].iloc[left_turns_i]
    left_roll_total = df["Total Roll Angle (downsampled)"].iloc[left_turns_i]

    slope_front, intercept_front = linear_regression(accel_left, left_roll_front) # np.polyfit(accel_left, left_roll_front, 1)
    slope_rear, intercept_rear = linear_regression(accel_left, left_roll_rear)
    slope_total, intercept_total = linear_regression(accel_left, left_roll_total)

    # print("left turn front roll gradient for " + date +": ", slope_front)
    # print("left turn rear roll gradient for " + date +": ", slope_rear)
    # print("left turn total roll gradient for " + date +": ", slope_total)

    ax = plt.gca()
    ax.scatter(accel_left, left_roll_front, marker = "o", s = 1, color=next(cycol),label = "front roll angle = " + str(slope_front) + "x + " + str(intercept_front))
    ax.scatter(accel_left, left_roll_rear, marker = "o", s = 1, color=next(cycol),label = "rear roll angle = " + str(slope_rear) + "x + " + str(intercept_rear))
    ax.scatter(accel_left, left_roll_total, marker = "o", s = 1, color=next(cycol),label = "total roll angle = " + str(slope_total) + "x + " + str(intercept_total))

    abline(slope_front, intercept_front, "front regression")
    abline(slope_rear, intercept_rear, "rear regression")
    abline(slope_total, intercept_total, "total regression")

    plt.xlabel("Lateral accel")
    plt.ylabel("Roll Angle (downsampled) (deg)")
    plt.title("Roll Angle v.s. Lateral Accel (left turn) for " + date)

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    return slope_front, slope_rear, slope_total


def graph_right_turn_roll(df, date, saveFig=False):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)

    right_turns_i = df.index[df["G Force Lat (downsampled)"].astype(float)>0].tolist()
    accel_right = (df["G Force Lat (downsampled)"].iloc[right_turns_i]).astype(float)
    right_roll_front = df["Front Roll Angle (downsampled)"].iloc[right_turns_i]
    right_roll_rear = df["Rear Roll Angle (downsampled)"].iloc[right_turns_i]
    right_roll_total = df["Total Roll Angle (downsampled)"].iloc[right_turns_i]

    slope_front, intercept_front = linear_regression(accel_right, right_roll_front)
    slope_rear, intercept_rear = linear_regression(accel_right, right_roll_rear)
    slope_total, intercept_total = linear_regression(accel_right, right_roll_total)

    # print("right turn front roll gradient for " + date + ": ", slope_front)
    # print("right turn rear roll gradient for " + date + ": ", slope_rear)
    # print("right turn total roll gradient for " + date + ": ", slope_total)

    ax = plt.gca()
    ax.scatter(accel_right, right_roll_front, marker = "o", s = 1, color=next(cycol),label = "front roll angle = " + str(slope_front) + "x + " + str(intercept_front))
    ax.scatter(accel_right, right_roll_rear, marker = "o", s = 1, color=next(cycol),label = "rear roll angle = " + str(slope_rear) + "x + " + str(intercept_rear))
    ax.scatter(accel_right, right_roll_total, marker = "o", s = 1, color=next(cycol),label = "total roll angle = " + str(slope_total) + "x + " + str(intercept_total))

    abline(slope_front, intercept_front, "front regression")
    abline(slope_rear, intercept_rear, "rear regression")
    abline(slope_total, intercept_total, "total regression")

    plt.xlabel("Lateral accel")
    plt.ylabel("Roll Angle (downsampled) (deg)")
    plt.title("Roll Angle v.s. Lateral Accel (right turn) for " + date)

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    return slope_front, slope_rear, slope_total


def linear_regression(accel, roll):
    # slope, intercept = np.polyfit(accel, roll, 1)
    lr = linear_model.LinearRegression()
    lr.fit(accel.values.reshape(len(accel), 1), roll)

    return lr.coef_,  lr.intercept_


def graph_rollvtime(df, saveFig=False):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)
    ax = plt.gca()

    rollAngleCols = ["Front Roll Angle", "Rear Roll Angle", "G Force Lat"]  # "Total Roll Angle"
    for col in rollAngleCols:
        y = df[col].astype(float)
        ax.plot(df["Time"].astype(float), y, markersize=5, label = col, color=next(cycol))
    
    plt.xlabel("Time (s)")
    plt.ylabel("Roll Angle (deg) and Accel (g)")
    plt.title("Roll Angle and Accel" + " v.s. Time")

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    if saveFig:
        plt.tight_layout()
        plt.savefig("./outputs/%s_roll_angle_accel.png" % df.name, bbox_inches='tight')

def graph_long_slip(df, saveFig=False):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)
    ax = plt.gca()

    longSlipPercent = ["Longitudinal Slip RL", "Longitudinal Slip RR"]
    for col in longSlipPercent:
        y = df[col].astype(float)
        ax.plot(df["Time"].astype(float), y, markersize=5, label = col, color=next(cycol))
    
    plt.xlabel("Time (s)")
    plt.ylabel("Longitudinal Slip Percent (%)")
    plt.title("Longitudinal Slip Percent" + " v.s. Time")

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    if saveFig:
        plt.tight_layout()
        plt.savefig("./outputs/%s_long_slip.png" % df.name, bbox_inches='tight')


# brake pressures v.s. time
def graph_brake_pres(df, saveFig=False):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)
    ax = plt.gca()

    brakePressures = ["Brake Pressure Front", "Brake Pressure Rear"]
    for col in brakePressures:
        y = df[col].astype(float)
        ax.plot(df["Time"].astype(float), y, markersize=5, label = col, color=next(cycol))
    
    plt.xlabel("Time (s)")
    plt.ylabel("Brake Pressures (kPa)")
    plt.title("Brake Pressures (kPa)" + " v.s. Time")

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# brake bias v.s. front pressure (scatter plot)
    if saveFig:
        plt.tight_layout()
        plt.savefig("./outputs/%s_brake_pres.png" % df.name, bbox_inches='tight')


# battery temperatures
def graph_battery_temps(df, saveFig=False):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)
    ax = plt.gca()

    for col in df.filter(like="Battery Temp").columns:
        ax.plot(df["Time"].astype(float), df[col], markersize=5, label = col, color=next(cycol))
    
    plt.xlabel("Time (s)")
    plt.ylabel("Battery Temps (C)")
    plt.title("Battery Temps" + " v.s. Time")

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    if saveFig:
        plt.tight_layout()
        plt.savefig("./outputs/%s_battery_temp.png" % df.name, bbox_inches='tight')


# battery voltages
def graph_battery_volts(df, saveFig=False):
    global fig_id
    fig_id = fig_id+1
    fig = plt.figure(fig_id)
    ax = plt.gca()

    for col in df.filter(like="Battery Voltage").columns:
        ax.plot(df["Time"].astype(float), df[col], markersize=5, label = col, color=next(cycol))
    
    plt.xlabel("Time (s)")
    plt.ylabel("Battery Voltage (V)")
    plt.title("Battery Voltages" + " v.s. Time")

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    if saveFig:
        plt.tight_layout()
        plt.savefig("./outputs/%s_battery_volts.png" % df.name, bbox_inches='tight')


def abline(slope, intercept, label):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--', color=next(cycol),label=label)


def graph_coolant_temp(df, saveFig=False):
    global fig_id
    fig_id = fig_id + 1
    fig = plt.figure(fig_id)
    ax = plt.gca()

    for col in df.filter(like="Coolant Temperature").columns:
        ax.plot(df["Time"].astype(float), df[col], markersize=5, label=col, color=next(cycol))

    plt.xlabel("Time (s)")
    plt.ylabel("Coolant temperature (°C)")
    plt.title("Coolant Temperature" + " v.s. Time")

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    if saveFig:
        plt.tight_layout()
        plt.savefig("./outputs/%s_coolant_temp.png" % df.name, bbox_inches='tight')


def graph_coolant_flow(df, saveFig=False):
    global fig_id
    fig_id = fig_id + 1
    fig = plt.figure(fig_id)

    y = df['GP Vol Flow 1'].to_numpy()
    ax = plt.gca()
    ax.plot(df["Time"].astype(float), y, markersize=5)

    plt.xlabel("Time (s)")
    plt.ylabel("Coolant Flow (ml/s)")
    plt.title("Coolant Flow" + " v.s. Time")

    if saveFig:
        plt.tight_layout()
        plt.savefig("./outputs/%s_coolant_flow.png" % df.name, bbox_inches='tight')

