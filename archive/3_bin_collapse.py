def func_add_time_stamp(df):
    # Convert the tpep_pickup_datetime to datetime format if it's not already
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'], format='%Y-%m-%d %H:%M')
    # Define the start time
    start_time = pd.Timestamp('2023-01-01 00:00:00')
    # Calculate the number of hours between each pickup time and the start time
    df['pick_up_time_cluster'] = ((df['tpep_pickup_datetime'] - start_time) / np.timedelta64(1, 'h')).astype(int) + 1
    # Return the updated dataframe with the new column
    return df

new_trip_data = func_add_time_stamp(trip_dur_zone_dat)



#sort new_trip_data by the tpep_pickup_datetime
new_trip_data = new_trip_data.sort_values(by='tpep_pickup_datetime')

print(new_trip_data.head(10))

#save for later use
new_trip_data.to_csv('/Users/laijiang/Documents/Pers/datatest/Data/save/TaxiTrips_cleaned.csv', index=False)



def aggregate_by_time_cluster(df):
    # Convert tpep_pickup_datetime to datetime if it's not already
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'], format='%Y-%m-%d %H:%M')

    # Extract the hour from the pickup time to add as a feature
    df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour

    # Group by the pick_up_time_cluster
    grouped = df.groupby('pick_up_time_cluster')

    # Create a new DataFrame with aggregated information for each cluster
    result = grouped.agg(
        cluster_ID=('pick_up_time_cluster', 'first'),  # (7) cluster ID
        num_rows=('pick_up_time_cluster', 'size'),  # (1) number of rows in this cluster
        sum_passenger_count=('passenger_count', 'sum'),  # (2) summation of passenger_count
        sum_trip_distance=('trip_distance', 'sum'),  # (3) summation of trip_distance
        sum_trip_durations=('trip_durations', 'sum'),  # (4) summation of trip_durations
        avg_trip_durations=('trip_durations', 'mean'),  # (5) average trip_durations
        pickup_hour=('pickup_hour', 'first')  # (new feature) the hour of the day for the cluster
    ).reset_index(drop=True)

    # Initialize columns for the count of dropoff_borough categories (6)
    borough_columns = ['Bronx', 'Manhattan', 'Queens', 'Brooklyn', 'Outside of NYC', 'Staten Island', 'Unknown', 'EWR']

    # Count the occurrences of each dropoff_borough category within each cluster
    for borough in borough_columns:
        result[borough] = grouped['dropoff_borough'].apply(lambda x: (x == borough).sum()).values
    
    return result

aggregated_data = aggregate_by_time_cluster(new_trip_data)

print("hourly data:")
# Display the first few rows of the aggregated dataframe
print(aggregated_data.head())

#dimension of the aggregated_data
print('Dimension of the aggregated data: ', aggregated_data.shape)

