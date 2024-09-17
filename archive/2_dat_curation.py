#read the zone lookup data
zone_lookup = pd.read_csv('/Users/laijiang/Documents/Pers/datatest/Data/dat/taxi_zone_lookup.csv')
print(zone_lookup.head())

#only take the first two columns
zone_lookup = zone_lookup.iloc[:, :2]
#show first 10 rows
#print(zone_lookup.head(10))

#merge the trip_dur_dat with the zone lookup data by PULocationID in trip_dur_dat and LocationID in zone_lookup
trip_dur_zone_dat = pd.merge(trip_dur_dat, zone_lookup, left_on='PULocationID', right_on='LocationID', how='left')
#rename the columns
trip_dur_zone_dat.rename(columns={'Borough': 'pickup_borough'}, inplace=True)
#merge the trip_dur_dat with the zone lookup data by DOLocationID in trip_dur_dat and LocationID in zone_lookup
trip_dur_zone_dat = pd.merge(trip_dur_zone_dat, zone_lookup, left_on='DOLocationID', right_on='LocationID', how='left')
#rename the columns
trip_dur_zone_dat.rename(columns={'Borough': 'dropoff_borough'}, inplace=True)

#drop these columns : LocationID_x , LocationID_y, LocationID, Borough, trip_distance_exp
trip_dur_zone_dat = trip_dur_zone_dat.drop(['LocationID_x', 'LocationID_y',  'trip_distance_exp'], axis=1)

#show the first few rows
print("location updated trip data:")
print(trip_dur_zone_dat.head())

#summary statistics of the updated trip data for the columns: pickup_borough, dropoff_borough
print('Summary statistics of pickup_borough: ', trip_dur_zone_dat['pickup_borough'].describe())
print('Summary statistics of dropoff_borough: ', trip_dur_zone_dat['dropoff_borough'].describe())

#missing values of the columns: pickup_borough, dropoff_borough
print('Number of missing values in pickup_borough: ', trip_dur_zone_dat['pickup_borough'].isnull().sum())
print('Number of missing values in dropoff_borough: ', trip_dur_zone_dat['dropoff_borough'].isnull().sum())

#check the DOLocationID of these missing values in dropoff_borough
print('DOLocationID of missing values in dropoff_borough: ', trip_dur_zone_dat[trip_dur_zone_dat['dropoff_borough'].isnull()]['DOLocationID'].unique())

#replace the missing values in dropoff_borough with "outside of NYC"
trip_dur_zone_dat['dropoff_borough'] = trip_dur_zone_dat['dropoff_borough'].fillna('Outside of NYC')

#show the table of counts of dropoff_borough
print('Counts of dropoff_borough: ', trip_dur_zone_dat['dropoff_borough'].value_counts())

#write this data to a csv file
trip_dur_zone_dat.to_csv('/Users/laijiang/Documents/Pers/datatest/Data/save/TaxiTrips_cleaned.csv', index=False)