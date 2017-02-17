# LIHUE, SAN DIEGO, MINNEAPOLIS, IRKUTSK
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

stations = {}

for line in open('stations.txt', 'r'):
    if 'GSN' in line:
        fields = line.split()
        stations[fields[0]] = ' '.join(fields[4:])


def find_stations(s):
    return {code: name for code, name in stations.items() if s in name}


datastations = ['USW00022536', 'USW00023188', 'USW00014922', 'RSM00030710']


def parse_file(file):
    return np.genfromtxt(file,
                         delimiter=dly_delimiter,
                         usecols=dly_usecols,
                         dtype=dly_dtype,
                         names=dly_names)


dly_delimiter = [11, 4, 2, 4] + [5, 1, 1, 1] * 31
dly_usecols = [1, 2, 3] + [4*i for i in range(1, 31+1)]
dly_dtype = [np.int32, np.int32, (np.str_, 4)] + [np.int32] * 31
dly_names = ['year', 'month', 'obs'] + [str(i) for i in range(1, 32)]


def unroll(record):
    start_date = np.datetime64('{}-{:02}'.format(record['year'], record['month']))
    dates = np.arange(start_date, start_date + np.timedelta64(1, 'M'), np.timedelta64(1, 'D'))
    rows = [(date, record[str(i+1)]/10) for i, date in enumerate(dates)]
    return np.array(rows, dtype=[('date', 'M8[D]'), ('value', 'd')])


def get_obs(file, obs):
    data = np.concatenate([unroll(record) for record in parse_file(file) if record[2] == obs])
    data['value'][data['value'] == -999.9] = np.nan
    return data


def fill_nans(data):
    dates_float = data['date'].astype(np.float64)
    nan = np.isnan(data['value'])
    data['value'][nan] = np.interp(dates_float[nan], dates_float[~nan], data['value'][~nan])


def plot_smoothed(t, win=10):
    smooted = np.correlate(t['value'], np.ones(win)/win, 'same')
    plt.plot(t['date'], smooted)


# plt.figure(figsize=(10, 6))
# for i, code in enumerate(datastations):
#     plt.subplot(2, 2, i+1)
#     plot_smoothed(get_obs("{}.dly".format(code), 'TMIN'), 365)
#     plot_smoothed(get_obs("{}.dly".format(code), 'TMAX'), 365)
#     plt.title(stations[code])
#     plt.axis(xmin=np.datetime64('1952'), xmax=np.datetime64('2012'), ymin=-10, ymax=30)
#
# plt.show()

def select_year(data, year):
    start = np.datetime64("{}".format(year))
    end = start + np.timedelta64(1, 'Y')
    return data[(data['date'] >= start) & (data['date'] < end)]['value']


# lihue_tmin = get_obs('USW00022536.dly', 'TMIN')
# lihue_tmax = get_obs('USW00022536.dly', 'TMAX')
# lihue_tmin_all = np.vstack([select_year(lihue_tmin, year)[:365] for year in range(1951, 2015)])
# lihue_tmax_all = np.vstack([select_year(lihue_tmax, year)[:365] for year in range(1951, 2015)])


# days = np.arange(1, 365+1)
# plt.fill_between(days, np.min(lihue_tmin_all, axis=0), np.max(lihue_tmin_all, axis=0), alpha=0.4)
# plt.plot(select_year(lihue_tmin, 2009))
# plt.fill_between(days, np.min(lihue_tmax_all, axis=0), np.max(lihue_tmax_all, axis=0), alpha=0.4)
# plt.plot(select_year(lihue_tmax, 2009))
# plt.axis(xmax=365)
# plt.show()


# challenge: SAN DIEGO vs MINNEAPOLIS

minneapolis_tmax = get_obs('USW00014922.dly', 'TMAX')
minneapolis_tmin = get_obs('USW00014922.dly', 'TMIN')
sandiego_tmax = get_obs('USW00023188.dly', 'TMAX')
sandiego_tmin = get_obs('USW00023188.dly', 'TMIN')

fill_nans(minneapolis_tmax)
fill_nans(minneapolis_tmin)
fill_nans(sandiego_tmax)
fill_nans(sandiego_tmin)


years = np.arange(1940, 2014+1)
minneapolis_tmax_all = np.vstack([select_year(minneapolis_tmax, year)[:365] for year in years])
minneapolis_mean = np.mean(minneapolis_tmax_all, axis=1)
minneapolis_warmest = years[np.argmax(minneapolis_mean)]
sandiego_tmin_all = np.vstack([select_year(sandiego_tmin,year)[:365] for year in years])
sandiego_mean = np.mean(sandiego_tmin_all, axis=1)
sandiego_coldest = years[np.argmin(sandiego_mean)]


days = np.arange(1, 366+1)
plt.fill_between(days,
                select_year(minneapolis_tmin, minneapolis_warmest),
                select_year(minneapolis_tmax, minneapolis_warmest),
                color='b', alpha=0.4)

plt.fill_between(days,
                select_year(sandiego_tmin, sandiego_coldest),
                select_year(sandiego_tmax, sandiego_coldest),
                color='r', alpha=0.4)

plt.axis(xmax=366)
plt.title('{} in Minneapolis vs. {} in San Diego'.format(minneapolis_warmest, sandiego_coldest))
plt.show()







