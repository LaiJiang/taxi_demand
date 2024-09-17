import pandas as pd
import numpy as np

def fill_zero_demand_hours(df):
    # Sort the dataframe by pickup_day and pickup_hour to ensure rows are in the correct order
    df = df.sort_values(by=['pickup_day', 'pickup_hour']).reset_index(drop=True)

    # Iterate through the rows where num_rows == 0
    for i in range(1, len(df) - 1):
        if df.loc[i, 'num_rows'] == 0:
            # Get the previous, current, and next rows
            previous_row = df.loc[i - 1]
            current_row = df.loc[i]
            next_row = df.loc[i + 1]

            # Calculate the rounded average for the columns
            avg_sum_passenger_count = np.round(np.mean([previous_row['sum_passenger_count'], current_row['sum_passenger_count'], next_row['sum_passenger_count']]))
            avg_sum_trip_distance = np.mean([previous_row['sum_trip_distance'], current_row['sum_trip_distance'], next_row['sum_trip_distance']])
            avg_sum_trip_durations = np.mean([previous_row['sum_trip_durations'], current_row['sum_trip_durations'], next_row['sum_trip_durations']])
            avg_num_rows = np.round(np.mean([previous_row['num_rows'], current_row['num_rows'], next_row['num_rows']]))  # Smoothing num_rows

            avg_Manhattan = np.round(np.mean([previous_row['Manhattan'], current_row['Manhattan'], next_row['Manhattan']]))
            avg_Queens = np.round(np.mean([previous_row['Queens'], current_row['Queens'], next_row['Queens']]))
            avg_Brooklyn = np.round(np.mean([previous_row['Brooklyn'], current_row['Brooklyn'], next_row['Brooklyn']]))
            avg_Outside_of_NYC = np.round(np.mean([previous_row['Outside of NYC'], current_row['Outside of NYC'], next_row['Outside of NYC']]))
            avg_Staten_Island = np.round(np.mean([previous_row['Staten Island'], current_row['Staten Island'], next_row['Staten Island']]))
            avg_Unknown = np.round(np.mean([previous_row['Unknown'], current_row['Unknown'], next_row['Unknown']]))
            avg_EWR = np.round(np.mean([previous_row['EWR'], current_row['EWR'], next_row['EWR']]))

            # Calculate the max for avg_trip_durations
            max_avg_trip_durations = np.max([previous_row['avg_trip_durations'], current_row['avg_trip_durations'], next_row['avg_trip_durations']])

            # Assign these values to the previous, current, and next rows
            df.loc[i - 1:i + 1, 'sum_passenger_count'] = avg_sum_passenger_count
            df.loc[i - 1:i + 1, 'sum_trip_distance'] = avg_sum_trip_distance
            df.loc[i - 1:i + 1, 'sum_trip_durations'] = avg_sum_trip_durations
            df.loc[i - 1:i + 1, 'avg_trip_durations'] = max_avg_trip_durations
            df.loc[i - 1:i + 1, 'num_rows'] = avg_num_rows  # Assign smoothed num_rows

            df.loc[i - 1:i + 1, 'Manhattan'] = avg_Manhattan
            df.loc[i - 1:i + 1, 'Queens'] = avg_Queens
            df.loc[i - 1:i + 1, 'Brooklyn'] = avg_Brooklyn
            df.loc[i - 1:i + 1, 'Outside of NYC'] = avg_Outside_of_NYC
            df.loc[i - 1:i + 1, 'Staten Island'] = avg_Staten_Island
            df.loc[i - 1:i + 1, 'Unknown'] = avg_Unknown
            df.loc[i - 1:i + 1, 'EWR'] = avg_EWR

    return df

# Example usage
smoothed_data = fill_zero_demand_hours(filled_data)

# Display the first few rows of the updated dataframe
print(smoothed_data.head())

#print number of rows with num_rows = 0
print('Number of rows with num_rows = 0: ', smoothed_data[smoothed_data['num_rows'] == 0].shape[0])

#the first row with num_rows = 0
#print(smoothed_data[smoothed_data['num_rows'] == 0].head(1))

#print(smoothed_data[95:99])

#for each row with num_rows = 0, we replace the values of the columns with the values of the previous row




def replace_zero_demand_rows(df):
    # Sort the dataframe by pickup_day and pickup_hour to ensure rows are in the correct order
    df = df.sort_values(by=['pickup_day', 'pickup_hour']).reset_index(drop=True)
    
    # Identify rows where num_rows is 0
    zero_demand_indices = df[df['num_rows'] == 0].index
    
    # Replace values in these rows with values from the previous row
    for idx in zero_demand_indices:
        if idx > 0:  # Ensure that we are not trying to access row -1
            df.loc[idx, df.columns != 'pickup_day'] = df.loc[idx - 1, df.columns != 'pickup_day']
            df.loc[idx, df.columns != 'pickup_hour'] = df.loc[idx - 1, df.columns != 'pickup_hour']

    return df

# Example usage:
smoothed_data_final = replace_zero_demand_rows(smoothed_data)

# Display the first few rows of the updated dataframe
#print(smoothed_data_final.head())

#print number of rows with num_rows = 0
#print('Number of rows with num_rows = 0: ', smoothed_data_final[smoothed_data_final['num_rows'] == 0].shape[0])

#print(smoothed_data_final[95:99])

#print("cluster ID adjustment")
#reassign the values of cluster_ID and pickup_hour and pickup_day
smoothed_data_final['cluster_ID'] =  smoothed_data_final.index
smoothed_data_final['pickup_hour'] = smoothed_data_final['cluster_ID'] % 24
smoothed_data_final['pickup_day'] = smoothed_data_final['cluster_ID'] // 24 + 1

#print number of rows with num_rows = 0
print('Number of rows with num_rows = 0: ', smoothed_data_final[smoothed_data_final['num_rows'] == 0].shape[0])

#print("data dimension: ",smoothed_data_final[95:99])
#print('Dimension of smoothed_data_final: ', smoothed_data.shape)
#print('Counts of pickup_hour: ', smoothed_data['pickup_hour'].value_counts())
#print('Counts of pickup_day: ', smoothed_data['pickup_day'].value_counts())

#save files
smoothed_data_final.to_csv('/Users/laijiang/Documents/Pers/datatest/Data/save/smoothed_data_final.csv', index=False)

