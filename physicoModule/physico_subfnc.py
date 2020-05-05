import numba
import numpy as np
import pandas as pd
import math


def sumNanNum(a, b):
    ma = np.isnan(a)
    mb = np.isnan(b)
    return np.where(ma & mb, np.nan, np.nansum([a, b], axis=0))


def meanNanNum(a, b):
    ma = np.isnan(a)
    mb = np.isnan(b)
    return np.where(ma & mb, np.nan, np.nanmean([a, b], axis=0))


def sumNanStr(a, b):
    ma = a.astype('str') == 'nan'
    mb = b.astype('str') == 'nan'
    return np.where(ma & mb, '', np.where(ma, '', a).astype('O')+'/' + np.where(mb, '', b).astype('O'))


def sumPositionStr(a, b):
    ma = a.astype('str') == 'R'
    mb = a.astype('str') == 'R'
    return np.where(ma & mb, 'R', np.where(ma, '', a).astype('O')+'/' + np.where(mb, '', b).astype('O'))


def sumDuplicateStr(a, b):
    assert len(a) == len(b)
    sum_str = np.zeros(a.shape, dtype='O')
    ma = a.astype('str') == 'nan'
    mb = b.astype('str') == 'nan'
    for i in range(len(a)):
        if ma[i] and mb[i]:
            sum_str[i] = ""
        elif mb[i] or a[i] == b[i]:
            sum_str[i] = a[i]
        elif ma[i]:
            sum_str[i] = b[i]
        else:
            sum_str[i] = a[i]+'/'+b[i]
    return sum_str


def typeDiscriminate(a, b):
    assert len(a) == len(b)
    type_m = np.zeros(a.shape, dtype='O')
    for i in range(len(a)):
        if a[i] == b[i]:
            type_m[i] = a[i]
        else:
            type_m[i] = b[i]
    return type_m


def getMax(a, b):
    ma = np.isnan(a)
    mb = np.isnan(b)
    a[ma] = 0.
    b[ma] = 0.
    return np.where(ma & mb, np.nan, np.nanmax([a, b], axis=0))

# Calculate Sum, Average, Stdev of np.array


def movingSum(input_m, windowSize, end=0):
    input_nonan_m = np.copy(input_m)
    input_nonan_m[np.isnan(input_m)] = 0.0

    if len(input_m.shape) == 2:
        return _movingSum2(input_nonan_m, windowSize, end)
    elif len(input_m.shape) == 1:
        return _movingSum1(input_nonan_m, windowSize, end)
    else:
        raise Exception("The input shape should be either 1D or 2D structure.")


@numba.jit(nopython=True)
def _movingSum2(input_m, windowSize, end):
    Ndi, Nii = input_m.shape
    res_m = np.zeros(input_m.shape, input_m.dtype)
    res_m[:end] = input_m[:end]
    for ii in range(Nii):
        for di in range(Ndi-end):
            if di == 0:
                cum = input_m[di, ii]
            elif di < windowSize:
                cum = cum+input_m[di, ii]
            else:
                cum = cum+input_m[di, ii]-input_m[di-windowSize, ii]
            res_m[di+end, ii] = cum
    return res_m


@numba.jit(nopython=True)
def _movingSum1(input_m, windowSize, end):
    Ndi = input_m.shape[0]
    res_m = np.zeros(input_m.shape, input_m.dtype)
    for di in range(Ndi-end):
        if di == 0:
            cum = input_m[di]
            res_m[di] = cum
        elif di < windowSize:
            cum = cum+input_m[di]
        else:
            cum = cum+input_m[di]-input_m[di-windowSize]
        res_m[di+end] = cum
    return res_m


def movingAverage(input_m, windowSize, end=0, nanIsZero=False):
    input_nonan_m = np.copy(input_m)
    input_nonan_m[np.isnan(input_m)] = 0.0

    count_m = np.ones(input_m.shape, input_m.dtype)
    if not nanIsZero:
        count_m[np.isnan(input_m)] = 0.0
    if len(input_m.shape) == 2:
        return _movingAverage2(input_nonan_m, count_m, windowSize, end)
    elif len(input_m.shape) == 1:
        return _movingAverage1(input_nonan_m, count_m, windowSize, end)
    else:
        raise Exception("The input shape should be either 1D or 2D structure.")


@numba.jit(nopython=True)
def _movingAverage2(input_m, count_m, windowSize, end):
    Ndi, Nii = input_m.shape
    res_m = np.zeros(input_m.shape, input_m.dtype)
    res_m[:end] = input_m[:end]
    for ii in range(Nii):
        for di in range(Ndi-end):
            if di == 0:
                cum = input_m[di, ii]
                div = count_m[di, ii]

            elif di < windowSize:
                cum = cum+input_m[di, ii]
                div = div+count_m[di, ii]
            else:
                cum = cum+input_m[di, ii]-input_m[di-windowSize, ii]
                div = div+count_m[di, ii]-count_m[di-windowSize, ii]

            if div == 0:
                res_m[di+end, ii] = 0.0
            else:
                res_m[di+end, ii] = cum/float(div)
    return res_m


@numba.jit(nopython=True)
def _movingAverage1(input_m, count_m, windowSize, end):
    Ndi = input_m.shape[0]
    res_m = np.zeros(input_m.shape, input_m.dtype)
    for di in range(Ndi-end):
        if di == 0:
            cum = input_m[di]
            div = count_m[di]
            res_m[di] = cum
        elif di < windowSize:
            cum = cum+input_m[di]
            div = div+count_m[di]
        else:
            cum = cum+input_m[di]-input_m[di-windowSize]
            div = div+count_m[di]-count_m[di-windowSize]

        if div == 0:
            res_m[di+end] = 0.0
        else:
            res_m[di+end] = cum/float(div)
    return res_m


def movingStdev(input_m, windowSize, nanIsZero=False):
    input_nonan_m = np.copy(input_m)
    input_nonan_m[np.isnan(input_m)] = 0.0

    count_m = np.ones(input_m.shape, input_m.dtype)
    if not nanIsZero:
        count_m[np.isnan(input_m)] = 0.0

    avg_m = movingAverage(input_m, windowSize)

    if len(input_m.shape) == 2:
        return _movingStdev2(input_nonan_m, avg_m, count_m, windowSize)
    elif len(input_m.shape) == 1:
        return _movingStdev1(input_nonan_m, avg_m, count_m, windowSize)
    else:
        raise Exception("The input shape should be either 1D or 2D structure.")


@numba.jit(nopython=True)
def _movingStdev2(input_nonan_m, avg_m, count_m, windowSize):

    Ndi, Nti = input_nonan_m.shape

    std_m = np.zeros(input_nonan_m.shape, input_nonan_m.dtype)

    for ti in range(Nti):
        for di in range(Ndi):
            if di == 0:
                dev = input_nonan_m[di, ti]-count_m[di, ti]*avg_m[di, ti]
                div = count_m[di, ti]
            elif di < windowSize:
                dev = 0
                for win in range(di+1):
                    dev += (input_nonan_m[win, ti] -
                            count_m[win, ti]*avg_m[di, ti])**2
                div = div + count_m[di, ti]
            else:
                dev = 0
                for win in range(windowSize):
                    dev += (input_nonan_m[di-win, ti] -
                            count_m[di-win, ti]*avg_m[di, ti])**2
                div = div + count_m[di, ti] - count_m[di-windowSize, ti]

            if div == 0:
                std_m[di, ti] = 0.0
            else:
                std_m[di, ti] = math.sqrt(dev/div)

    return avg_m, std_m


@numba.jit(nopython=True)
def _movingStdev1(input_nonan_m, avg_m, count_m, windowSize):

    Ndi = input_nonan_m.shape[0]

    std_m = np.zeros(input_nonan_m.shape, input_nonan_m.dtype)

    for di in range(Ndi):
        if di == 0:
            dev = input_nonan_m[di]-count_m[di]*avg_m[di]
            div = count_m[di]
        elif di < windowSize:
            dev = 0
            for win in range(di+1):
                dev += (input_nonan_m[win] -
                        count_m[win]*avg_m[di])**2
            div = div + count_m[di]
        else:
            dev = 0
            for win in range(windowSize):
                dev += (input_nonan_m[di-win] -
                        count_m[di-win]*avg_m[di])**2
            div = div + count_m[di] - count_m[di-windowSize]

        if div == 0:
            std_m[di] = 0.0
        else:
            std_m[di] = math.sqrt(dev/div)

    return avg_m, std_m


# Cacultate multiple, divide two array
@numba.jit(nopython=True)
def mulArray(over_m, under_m):
    assert len(over_m) == len(under_m)
    res_m = np.zeros(over_m.shape, over_m.dtype)
    Ndi = over_m.shape[0]
    for di in range(Ndi):
        res_m[di] = over_m[di] * under_m[di]
    return res_m


@numba.jit(nopython=True)
def divArray(over_m, under_m):
    assert len(over_m) == len(under_m)
    res_m = np.zeros(over_m.shape, over_m.dtype)
    Ndi = over_m.shape[0]
    for di in range(Ndi):
        if under_m[di] == 0:
            res_m[di] = np.NaN
        else:
            res_m[di] = over_m[di] / under_m[di]
    return res_m
