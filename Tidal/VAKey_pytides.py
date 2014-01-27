# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#%pylab inline
from matplotlib import *
from scipy import *
from pytides.tide import Tide
from pylab import *
from matplotlib import dates as mdates
import datetime as datetime
#--default matplotlib
rcParams['mathtext.default'] = 'regular'
rcParams['legend.fontsize']  = 8
rcParams['axes.labelsize']   = 8
rcParams['xtick.labelsize']  = 8
rcParams['ytick.labelsize']  = 8
rcParams['figure.subplot.wspace'] = 0.35
rcParams['figure.subplot.hspace'] = 0.35
months   = mdates.MonthLocator()  # every day
weeks   = mdates.WeekdayLocator(byweekday=mdates.MO, interval=1) #--every week
days   = mdates.DayLocator()  # every day
hours   = mdates.HourLocator()  # every hour
monthsFmt = mdates.DateFormatter('%m')
daysFmt = mdates.DateFormatter('%m/%d')
weeksFmt = mdates.DateFormatter('%m/%d')
def set_daysFmt(ax):
    ax.xaxis.set_major_locator(days)    
    ax.xaxis.set_minor_locator(hours)
    ax.xaxis.set_major_formatter(daysFmt)
def set_weeksFmt(ax):
    ax.xaxis.set_major_locator(weeks)    
    ax.xaxis.set_minor_locator(days)
    ax.xaxis.set_major_formatter(weeksFmt)
def set_monthsFmt(ax):
    ax.xaxis.set_major_locator(months)    
    ax.xaxis.set_minor_locator(days)
    ax.xaxis.set_major_formatter(monthsFmt)   

# <markdowncell>

# ####Read and process data

# <codecell>

#function to parse data and normalize it
def parse_data(fname):
    data_dtype = dtype([('datetime','a20'),('head','f4')])
    raw = loadtxt(fname, delimiter=',', dtype=data_dtype, comments='#')
    dout = []
    for [d,v] in raw:
        dt = datetime.datetime.strptime(d, '%m/%d/%Y %H:%M:%S')
        dout.append([dt,v])
    dout = array(dout)
    dout[:,1] -= average(dout[:,1])
    return dout

# <codecell>

data_dir = os.path.join('data')
tide = ['tide',0.0,parse_data(os.path.join(data_dir,'VAKey_6min.csv'))]
time_min = tide[2][0,0]
time_max = tide[2][-1,0]
dt_sec = (tide[2][1,0] - tide[2][0,0]).total_seconds()
#--create time_all
tstep = datetime.timedelta(seconds=dt_sec)
dt = time_min
time_all = []
while dt <= time_max:
    time_all.append(dt)
    dt += tstep
time_all = array(time_all)
#--convert from ft to meters
tide[2][:,1] /= 3.28081
#--
de_tide = parse_data(os.path.join(data_dir,'DE_Tide.csv'))
#--plot raw normalized data
t = tide[2]
ax = subplot(1,1,1)
ax.plot(t[:,0], t[:,1], linewidth=2)
ax.plot(de_tide[:,0], de_tide[:,1], linewidth=0.75, color='red')
set_monthsFmt(ax)
ylabel('Elevation, m')
#show()

# <markdowncell>

# ####Prepare a list of datetimes, each 6 minutes apart, for a the period of the dataset.

# <codecell>

total_hours = float((time_all[-1] - time_all[0]).total_seconds()) / (60. * 60.)
nsamples = time_all.shape[0]
hours = linspace(0.,float(total_hours),nsamples)
times = Tide._times(time_all[0], hours)
print times

# <codecell>

##Fit the tidal data to the harmonic model using Pytides
current_data = tide[2][:,1].astype(float)
current_date = tide[2][:,0]
print len(current_date), current_date
print len(current_data), current_data
my_tide = Tide.decompose(current_data, t=current_date)
print my_tide.model['amplitude']
print my_tide.model['phase']
for c in my_tide.model['constituent']:
    print c.name
##Predict the tides using the Pytides model.
my_prediction = my_tide.at(times)
print my_prediction

# <codecell>


