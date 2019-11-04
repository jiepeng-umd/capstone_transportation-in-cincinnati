import pandas as pd
import geopandas as gpd
from matplotlib import pyplot as plt
import numpy as np

speed = pd.read_csv("speed_20181201to20190131.csv")
speed=speed.dropna()
Map=gpd.read_file('map_cincinnati.geojson')
# speed.to_csv('speed.csv')
# Map.head(20).to_file('Map.geojson', driver='GeoJSON')
# Map=gpd.read_file('Map.geojson')
# test case

# print(Map[Map['osmname']=='John A. Roebling Suspension Bridge'])
# f = open('name.csv', "w")
ID=Map[Map['osmname']=='John A. Roebling Suspension Bridge'].head(1)['osmwayid'].values[0]
# print(ID)
# Map[Map['osmname']=='John A. Roebling Suspension Bridge'].to_file('test.geojson', driver='GeoJSON')

# what place we are considering
# ID=41409392
# what time are we considering
def average_speed(start_time, end_time):
    filter=(speed['year']==start_time[0]) & (speed['month']==start_time[1]) & (speed['day']==start_time[2]) & \
            (speed['hour']>=start_time[-1]) & (speed['hour']<=end_time[-1]) & \
           (speed['osm_way_id'].astype(int)==ID)
    return speed[filter]['speed_mph_mean'].mean()

def daily_average(date):
    start_time = date+ [0]
    end_time=date+[23]
    return average_speed(start_time,end_time)

def hourly_average(start_date,end_date,hour):
    result=[]
    for i in range(start_date,end_date):
        start_time=[2018,12,i,hour]
        filter = (speed['year'] == start_time[0]) & (speed['month'] == start_time[1]) & (
                    speed['day'] == i) & \
                 (speed['hour'] == hour) & \
                 (speed['osm_way_id'].astype(int) == ID)
        tmp=speed[filter]['speed_mph_mean']
        if len(tmp)>0: result+=[speed[filter]['speed_mph_mean'].values[0]]
    return np.mean(result)

y=[]
for i in range(24):
    y+=[hourly_average(1,31,i)]

x1=range(24)
y1=y
plt.figure(1)
plt.plot(x1, y1,'o')
plt.xlabel('Hour(h)')
plt.ylabel('Speed(mph)')
plt.title('Monthly average traveling speed of vehicles going through the John A. Roebling Suspension Bridge in Dec, 2018')

speedlist=[]
dates=range(1,31)
for i in dates:
    date=[2018,12,i]
    speedlist+=[daily_average(date)]

# y1mask=np.isfinite(speedlist)
y1=speedlist
x1=dates
plt.figure(2)
plt.plot(x1, y1,'o')
plt.xlabel('Date')
plt.ylabel('Speed(mph)')
plt.title('Average daily traveling speed of vehicles going through the John A. Roebling Suspension Bridge in Dec, 2018')
plt.show()