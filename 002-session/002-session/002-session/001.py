import numpy as np
from pathlib import Path
import urllib.request
import matplotlib.pyplot as plt
import seaborn
from pprint import pprint as pp


# base download URI
BASE_URI = 'ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/all/'


def load_daily_file(name):
    station_names = open('./src/stations.txt', 'r')
    stations = [station for station in station_names if name.lower() in station.lower()]
    for station in stations:
        file_name = station.split()[0] + '.dly'
        file = Path('./data/' + file_name)
        if not file.is_file():
            print("File was not find locally, download from source")
            urllib.request.urlretrieve(BASE_URI+file_name, './data/'+file_name)
        return file


def parse_raw_file(name):
    delimiter = [11, 4, 2, 4] + [5, 1, 1, 1] * 31
    usecols = [1, 2, 3] + [4 * i for i in range(1, 31+1)]
    dtype = [np.int32, np.int32, (np.str, 4)] + [np.int32 for _ in range(1, 31+1)]
    names = ['year', 'month', 'obs'] + [str(i) for i in range(1, 31+1)]
    return np.genfromtxt(str(load_daily_file(name).absolute()), delimiter=delimiter, usecols=usecols, dtype=dtype, names=names)


def unroll(record):
    start = np.datetime64('{}-{:02}'.format(record['year'], record['month']))
    dates = np.arange(start, start + np.timedelta64(1, 'M'), np.timedelta64(1, 'D'))
    rows = [(date, record[str(i+1)]/10) for i, date in enumerate(dates)]
    return np.array(rows, dtype=[('date', 'M8[D]'), ('value', 'd')])


def fill_nans(data):
    nan = np.isnan(data['value'])
    date_floats = data['date'].astype('float64')
    data['value'][nan] = np.interp(date_floats[nan], date_floats[~nan], data['value'][~nan])
    return data


def get_obs_by_name(name, obs):
    data = np.concatenate([unroll(record) for record in parse_raw_file(name) if obs == record[2]])
    data['value'][data['value'] == -999.9] = np.nan
    return fill_nans(data)


def plot_smoothed(data, win=10):
    smoothed = np.correlate(data['value'], np.ones(win)/win, 'same')
    plt.plot(data['date'], smoothed)


def select_year(data, year):
    start = np.datetime64('{}'.format(year))
    end = start + np.timedelta64(1, 'Y')
    return data[(data['date'] >= start) & (data['date'] < end)]['value']


tehran_tmax = get_obs_by_name('tehran', 'TMAX')
tehran_tmin = get_obs_by_name('tehran', 'TMIN')
print(tehran_tmax[tehran_tmax['value'].argmax()])
print(tehran_tmin[tehran_tmin['value'].argmin()])

plt.plot([i for i in range(365)], select_year(tehran_tmax, 1975))
plt.plot([i for i in range(365)], select_year(tehran_tmin, 1973))
plt.show()