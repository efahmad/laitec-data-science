import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint as pp
import seaborn
import sys

stations = {}

for line in open('stations.txt', 'r'):
    if 'GSN' in line:
        fields = line.split()
        stations[fields[0]] = ' '.join(fields[4:])
len(stations)


# LIHUE, SAN DIEGO, MINNEAPOLIS, IRKUTSK

datastations = ['USW00022536', 'USW00023188', 'USW00014922', 'RSM00030710']
# pp(open('readme.txt', 'r').readlines()[98:121])

dly_delimiter = [11, 4, 2, 4] + [5, 1, 1, 1] * 31
dly_usecols = [1, 2, 3] + [4*i for i in range(1, 32)]
dly_dtype = [np.int32, np.int32, (np.str_, 4)] + [np.int32] * 31
dly_names = ['year', 'month', 'obs'] + [str(day) for day in range(1, 31+1)]


def parsefile(filename):
    return np.genfromtxt(filename,
                         delimiter=dly_delimiter,
                         usecols=dly_usecols,
                         dtype=dly_dtype,
                         names=dly_names)

lihue = parsefile('USW00022536.dly')


def unroll(record):
    startdate = np.datetime64('{}-{:02}'.format(record['year'], record['month']))
    dates = np.arange(startdate, startdate + np.timedelta64(1, 'M'), np.timedelta64(1, 'D'))
    rows = [(date, record[str(i+1)]/10) for i, date in enumerate(dates)]
    return np.array(rows, dtype=[('date', 'M8[D]'), ('value', 'd')])


def getobs(filename, obs):
    data = np.concatenate([unroll(row) for row in parsefile(filename) if row[2] == obs])
    data['value'][data['value'] == -999.9] = np.nan
    return data


lihue_tmax = getobs('USW00022536.dly', 'TMAX')
lihue_tmin = getobs('USW00022536.dly', 'TMIN')

# plt.plot(lihue_tmax['date'], lihue_tmax['value'])
# plt.show()
# print(np.mean(lihue_tmin['value']), np.mean(lihue_tmax['value']))


def fillnans(data):
    dates_float = data['date'].astype(np.float64)
    nan = np.isnan(data['value'])
    data['value'][nan] = np.interp(dates_float[nan], dates_float[~nan], data['value'][~nan])

fillnans(lihue_tmax)
fillnans(lihue_tmin)
# print(np.mean(lihue_tmin['value']), np.mean(lihue_tmax['value']))
plt.plot(lihue_tmin['date'], lihue_tmin['value'])
# plt.show()


def plot_smoothed(t, win=10):
    smoothed = np.correlate(t['value'], np.ones(win)/win, 'same')
    plt.plot(t['date'], smoothed)


for i, code in enumerate(datastations):
    plt.subplot(2, 2, i+1)
    plot_smoothed(getobs('{}.dly'.format(code), 'TMIN'), 365)
    plot_smoothed(getobs('{}.dly'.format(code), 'TMAX'), 365)
    plt.title(stations[code])
    plt.axis(xmin=np.datetime64('1952'), xmax=np.datetime64('2012'), ymin=-10, ymax=30)

# plt.show()


def selectyear(data, year):
    start = np.datetime64('{}'.format(year))
    end = start + np.timedelta64(1, 'Y')
    return data[(data['date'] >= start) & (data['date'] < end)]['value']

# selectyear(lihue_tmin, 1951)


minneapolis_tmax = getobs('USW00014922.dly', 'TMAX')
minneapolis_tmin = getobs('USW00014922.dly', 'TMIN')
sandiego_tmax = getobs('USW00023188.dly', 'TMAX')
sandiego_tmin = getobs('USW00023188.dly', 'TMIN')


fillnans(minneapolis_tmax)
fillnans(minneapolis_tmin)
fillnans(sandiego_tmax)
fillnans(sandiego_tmin)


years = np.arange(1940, 2014+1)
minneapolis_tmax_all = np.vstack([selectyear(minneapolis_tmax, year)[:365] for year in years])
minneapolis_mean = np.mean(minneapolis_tmax_all, axis=1)

minneapolis_warmest = years[np.argmax(minneapolis_mean)]
sandiego_tmin_all = np.vstack([selectyear(sandiego_tmin, year)[:365] for year in years])
sandiego_mean = np.mean(sandiego_tmin_all, axis=1)
sandiego_coldest = years[np.argmin(sandiego_mean)]
sandiego_coldest

plt.figure(figsize=(12, 4))
days = np.arange(1, 366+1)
plt.fill_between(days,
                selectyear(minneapolis_tmin, minneapolis_warmest),
                selectyear(minneapolis_tmax, minneapolis_warmest),
                color='b', alpha=0.4)
plt.fill_between(days,
                selectyear(sandiego_tmin, sandiego_coldest),
                selectyear(sandiego_tmax, sandiego_coldest),
                color='r', alpha=0.4)
plt.axis(xmax=366)
plt.title('{} in Minneapolis vs. {} in San Diego'.format(minneapolis_warmest, sandiego_coldest))
plt.show()

