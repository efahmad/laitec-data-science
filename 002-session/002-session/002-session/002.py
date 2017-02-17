import sys
from pathlib import Path
import urllib.request
import numpy as np
import matplotlib.pyplot as plt

BASE_URI = 'ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/all/'


def load_daily_file(name):
    for station in open('stations.txt').readlines():
        if name.lower() in station.lower():
            file_name = station.split()[0] + '.dly'
            file = Path('./data/'+file_name)
            if not file.is_file():
                urllib.request.urlretrieve(BASE_URI + file_name, './data/'+file_name)
            return file


def parse_raw_file(name):
    file_name = str(load_daily_file(name).absolute())
    delimiter = [11, 4, 2, 4] + [5, 1, 1, 1, 1] * 31
    usecols = [1, 2, 3] + [i * 4 for i in range(1, 31+1)]
    names = ['year', 'month', 'obs'] + [str(i) for i in range(1, 31+1)]
    dtype = [np.int32, np.int32, (np.str, 4)] + [np.int32 for _ in range(1, 31+1)]
    return np.genfromtxt(file_name,
                  delimiter=delimiter,
                  usecols=usecols,
                  names=names,
                  dtype=dtype)


def unroll(record):
    start = np.datetime64("{}-{:02}".format(record['year'], record['month']))
    dates = np.arange(start, start + np.timedelta64(1, 'M'), np.timedelta64(1, 'D'))
    rows = [(date, record[str(i+1)] / 10) for i, date in enumerate(dates)]
    return np.array(rows, dtype=[('date', 'M8[D]'), ('value', np.float32)])


def fill_nans(data):
    nan = data['value'] < -900
    data['value'][nan] = np.nan
    date_floats = data['date'].astype('float64')
    data['value'][nan] = np.interp(date_floats[nan], date_floats[~nan], data['value'][~nan])
    return data


def get_obs_by_name(name, obs):
    data = np.concatenate([unroll(record) for record in parse_raw_file(name) if record[2] == obs])
    return data


def select_year(data, year):
    return data[(data['date'] > np.datetime64("{}-01".format(year))) & (data['date'] < np.datetime64("{}-01".format(year+1)))]

# data_tmin = fill_nans(get_obs_by_name('tehran', 'TMIN'))
# data_tmax = fill_nans(get_obs_by_name('tehran', 'TMAX'))
# print(data_tmin[data_tmin['value'].argmin()])
# print(data_tmax[data_tmax['value'].argmax()])
# d1 = select_year(data_tmin, 2016)
# d2 = select_year(data_tmax, 2016)
