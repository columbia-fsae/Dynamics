import numpy as np
import math
from scipy.signal import lfilter, decimate
import pandas as pd

def calc_roll_angle(df, front_track, rear_track):
    df["Front Roll Angle"] = np.degrees(np.arctan(df["Wheel Center FL Delta"]/(front_track/2))) +np.degrees(np.arctan(-1*df["Wheel Center FR Delta"]/(front_track/2)))
    df["Rear Roll Angle"] = np.degrees(np.arctan(df["Wheel Center RL Delta"]/(rear_track/2))) + np.degrees(np.arctan(-1*df["Wheel Center RR Delta"]/(rear_track/2)))
    df["Total Roll Angle"] = (df["Front Roll Angle"]+df["Rear Roll Angle"])/2

def filter_downsample_rollangle(df):
    n = round(len(df["Total Roll Angle"])/len(df["G Force Long"]))
    #n = 12
    coef = np.ones(n) / n

    df_downsampled = pd.DataFrame(columns=['Front Roll Angle (downsampled)', 'Rear Roll Angle (downsampled)', 'Total Roll Angle (downsampled)', 'G Force Lat (downsampled)'])
    df["Front Roll Angle (filtered)"] = lfilter(coef, 1, df["Front Roll Angle"])
    df["Rear Roll Angle (filtered)"] = lfilter(coef, 1, df["Rear Roll Angle"])
    df["Total Roll Angle (filtered)"] = lfilter(coef, 1, df["Total Roll Angle"])
    df_downsampled["Front Roll Angle (downsampled)"] = decimate(df["Front Roll Angle (filtered)"],n)
    df_downsampled["Rear Roll Angle (downsampled)"] = decimate(df["Rear Roll Angle (filtered)"],n)
    df_downsampled["Total Roll Angle (downsampled)"] = decimate(df["Total Roll Angle (filtered)"],n)
    df_downsampled["G Force Lat (downsampled)"] = decimate(df["G Force Lat"],n)
    return df_downsampled


def calc_roll_stiffness(M_roll, front_rg, rear_rg, total_rg):
    Ktot = M_roll/total_rg
    Kfront = Ktot * front_rg/(front_rg+rear_rg)
    Krear = Ktot-Kfront
    return Kfront, Krear, Ktot

def calc_roll_moment(cgh, center_rch, sprung_weight):
    m_roll = (cgh-center_rch)*sprung_weight/12 # lb*ft
    return m_roll


def calc_FLLTD(tot_weight, front_track, rear_track, cgh, rch):  #fix rch
    w_trans_front = (tot_weight/front_track)*((cgh-rch)*KfrontL_4_28/KtotL_4_28 + b*rch/wheelbase)
    w_trans_rear = (tot_weight/rear_track)*((cgh-rch)*KrearL_4_28/KtotL_4_28 + a*rch/wheelbase)
    FLLTD = (w_trans_front_L_4_28)/(w_trans_front_L_4_28+w_trans_rear_L_4_28)
    return FLLTD


# calc _theoretical roll stiffness
