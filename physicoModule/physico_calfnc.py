import numpy as np
import pandas as pd
from physicoModule import physico_subfnc as psf


def calculateLoad(rpe, totTime):
    load = rpe*totTime
    return load


def calculateMono(load):
    week_avg, week_std = psf.movingStdev(load, 7)
    mono = psf.divArray(week_avg, week_std)
    return mono


def calculateStrain(load, mono):
    week_load = psf.movingSum(load, 7)
    strain = psf.mulArray(week_load, mono)
    return strain


def calculateEwam(load):
    week_load = psf.movingSum(load, 7)
    month_load = psf.movingSum(load, 28)
    ewam = psf.divArray(week_load, month_load)
    return ewam


def calculateTotal(df, type='T', name='Total'):
    if type == 'M':
        df = df[df.Type == 'M']
        df = df[df.Position != 'GK']
        df = df[df.Position != 'R']
    elif type == 'R':
        df = df[df.Type == 'M']
        df = df[df.Position == 'R']
        if df.empty:
            return None, None

    df = df.loc[:, 'RPE':]
    len_df = len(df)

    SUMLIST = ['TR Time', 'Total Dist.',
               'HSR+Sprint', 'HSR+Sprint', 'MSR', 'HSR', 'Sprint', 'Accel Cnt.', 'Decel Cnt.', 'GPS PL', 'Load', 'Strain']
    MAXLIST = ['Max Speed']
    total_list = []
    for col in df.columns:
        if col in SUMLIST:
            total = df[col].sum()
        elif col in MAXLIST:
            total = df[col].max()
        else:
            total = df[col].mean()
        total_list.append(total)
    total_df = pd.DataFrame([total_list], columns=df.columns)
    total_df = total_df.rename(index={0: name})
    total_df = total_df.round(1)
    return total_df, len_df


def calculateAverage(df, len_df, name):
    if df is not None and len_df != 0:
        avg_df = df.rename(index={df.index.values[0]: name})
        avg_df.loc[:, 'TR Time':] = avg_df.loc[:,
                                               'TR Time':] / len_df
        avg_df['Max Speed'] = df['Max Speed'].values
    else:
        avg_df = None
    return avg_df
