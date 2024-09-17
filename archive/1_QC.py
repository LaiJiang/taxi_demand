#libraries
import dask.dataframe as dd
import pandas as pd#pandas to create small dataframes 
import datetime #Convert to unix time
import time #Convert to unix time
import numpy as np#Do aritmetic operations on arrays
# matplotlib: used to plot graphs
import matplotlib
import scipy
# matplotlib.use('nbagg') : matplotlib uses this protocall which makes plots more user intractive like zoom in and zoom out
matplotlib.use('nbagg')
import matplotlib.pylab as plt
import seaborn as sns#Plots
from matplotlib import rcParams#Size of plots  
from sklearn.cluster import MiniBatchKMeans, KMeans#Clustering
import math
import pickle
import os
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import warnings

#load trip data
trip_data = pd.read_csv('/Users/laijiang/Documents/Pers/datatest/Data/dat/TaxiTrips_BronxOrigin2023.csv')

#print number of rows 
print('Number of rows in trip data: ', trip_data.shape[0])

#print the first few rows
print(trip_data.head())

#check if any rows are duplicated in trip_data
print('Number of duplicate rows in trip data: ', trip_data.duplicated().sum())


#QC 1: drop the dupliated records
trip_data = trip_data.drop_duplicates()
print('Number of rows in trip data: ', trip_data.shape[0])

#QC 2: missing values
print('Number of missing values in trip data: ', trip_data.isnull().sum())

#for the missing values in the column "passenger_count" and "trip_distance", we impute the missing values with the median of the column with same pick-up and drop-off locationsIDs
trip_data['passenger_count'] = trip_data['passenger_count'].fillna(trip_data.groupby(['PULocationID', 'DOLocationID'])['passenger_count'].transform('median'))
trip_data['trip_distance'] = trip_data['trip_distance'].fillna(trip_data.groupby(['PULocationID', 'DOLocationID'])['trip_distance'].transform('median'))

# QC 3: zero values
#check number of rows with trip_distance = 0
print('Number of rows with trip_distance = 0: ', trip_data[trip_data['trip_distance'] == 0].shape[0])

#number of rows with exactly the same value of columns tpep_pickup_datetime and tpep_dropoff_datetime
print('Number of rows with exactly the same value of columns tpep_pickup_datetime and tpep_dropoff_datetime: ', trip_data[trip_data['tpep_pickup_datetime'] == trip_data['tpep_dropoff_datetime']].shape[0])

#remove the rows with exactly the same value of columns tpep_pickup_datetime and tpep_dropoff_datetime. probably due to technical error
trip_data = trip_data[trip_data['tpep_pickup_datetime'] != trip_data['tpep_dropoff_datetime']]

#for the rest of zero values in the column "trip_distance", we impute the zero values with median value of the subset trips data with the same pick-up and drop-off locations. 
trip_data['trip_distance'] = trip_data['trip_distance'].replace(0, np.nan)
trip_data['trip_distance'] = trip_data['trip_distance'].fillna(trip_data.groupby(['PULocationID', 'DOLocationID'])['trip_distance'].transform('median'))

#check number of rows with passenger_count = 0
print('Number of rows with passenger_count = 0: ', trip_data[trip_data['passenger_count'] == 0].shape[0])

#replace the zero values in the column "passenger_count" with the median of the column
trip_data['passenger_count'] = trip_data['passenger_count'].replace(0, np.nan)
trip_data['passenger_count'] = trip_data['passenger_count'].fillna(trip_data['passenger_count'].median())


#QC 4: check the outliers of each column
print('Summary statistics of trip data: ', trip_data.describe())

#print the table of passenger_count counts
print('Counts of passenger_count in trip data: ', trip_data['passenger_count'].value_counts())

#replace the passenger_count values greater than 6 with the median of the column
trip_data['passenger_count'] = trip_data['passenger_count'].replace(11, np.nan)
trip_data['passenger_count'] = trip_data['passenger_count'].fillna(trip_data['passenger_count'].median())

#plot the distribution of the column "trip_distance" only for the values > 100 and output to the file "trip_distance_distribution.png"
plt.hist(trip_data[trip_data['trip_distance'] > 100]['trip_distance'], bins=100)
plt.xlabel('Trip Distance')
plt.ylabel('Frequency')
plt.title('Distribution of Trip Distance')
plt.savefig('trip_distance_distribution.png')
plt.show()

#for these outliers of "trip_distance" > 24.51: 

#find calculate the trip duration 
def convert_to_unix(s):
    return time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M").timetuple())


def fun_trip_durations(trp_dat):
    duration = trp_dat[['tpep_pickup_datetime','tpep_dropoff_datetime']]
    # pickups and dropoffs to unix time
    duration_pickup = [convert_to_unix(x) for x in duration['tpep_pickup_datetime'].values]
    duration_drop = [convert_to_unix(x) for x in duration['tpep_dropoff_datetime'].values]
    # calculate duration of trips
    durations = (np.array(duration_drop) - np.array(duration_pickup))/60  # in minutes
    # append durations of trips to a new dataframe
    new_frame = trp_dat
    new_frame['trip_durations'] = durations
    # average expectation (25 mph) of trip_distances = durations * 25
    new_frame['trip_distance_exp'] = new_frame['trip_durations'] * 25 / 60

   #the rows with trip_distance > 24.51 are replaced with the values of trip_distance_exp
    new_frame.loc[new_frame['trip_distance'] > 24.51, 'trip_distance'] = new_frame['trip_distance_exp']
    return new_frame



trip_dur_dat = fun_trip_durations(trip_data)
print(trip_dur_dat.head())

print('Summary statistics of trip data: ', trip_dur_dat.describe())

#Number of rows with negative trip_durations
print('Number of rows with negative trip_durations: ', trip_dur_dat[trip_dur_dat['trip_durations'] < 0].shape[0])
#show these rows with negative trip_durations
print(trip_dur_dat[trip_dur_dat['trip_durations'] < 0])

#remove the rows with negative trip_durations
trip_dur_dat = trip_dur_dat[trip_dur_dat['trip_durations'] > 0]
#remove the rows with trip_durations > 10*60 
trip_dur_dat = trip_dur_dat[trip_dur_dat['trip_durations'] < 10*60]


print('Summary statistics of trip data: ', trip_dur_dat.describe())


#Q-Q plot for checking iftrip_distance is normal and save figure
#add the diagonal line also
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
sns.kdeplot(trip_dur_dat['trip_distance'].values, shade=True, color="b")
plt.title('PDF of trip_distance')
plt.subplot(1, 2, 2)
res = scipy.stats.probplot(trip_dur_dat['trip_distance'].values, plot=plt)
plt.plot([0,25],[0,25], color='r')
plt.savefig('trip_distance.png')
plt.show()

#Q-Q plot for checking iftrip_distance is log-normal and save figure
#add the diagonal line also
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
sns.kdeplot(np.log(trip_dur_dat['trip_distance'].values), shade=True, color="b")
plt.title('PDF of log(trip_distance)')
plt.subplot(1, 2, 2)
res = scipy.stats.probplot(np.log(trip_dur_dat['trip_distance'].values), plot=plt)
plt.plot([0,10],[0,10], color='r')
plt.savefig('log_trip_distance.png')
plt.show()


#Q-Q plot for checking if trip-durations is normal ans save figure
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
sns.kdeplot(trip_dur_dat['trip_durations'].values, shade=True, color="b")
plt.title('PDF of trip_durations')
plt.subplot(1, 2, 2)
res = scipy.stats.probplot(trip_dur_dat['trip_durations'].values, plot=plt)
plt.savefig('trip_duration.png')
plt.show()



#Q-Q plot for checking if trip-durations is log-normal ans save figure
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
sns.kdeplot(np.log(trip_dur_dat['trip_durations'].values), shade=True, color="b")
plt.title('PDF of log(trip_duration)')
plt.subplot(1, 2, 2)
res = scipy.stats.probplot(np.log(trip_dur_dat['trip_durations'].values), plot=plt)
plt.savefig('log_trip_duration.png')
plt.show()

