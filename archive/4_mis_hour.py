#first 

import pandas as pd
import numpy as np
from itertools import product

def insert_missing_rows(df):
    # Create all possible combinations of pickup_day (1 to 365) and pickup_hour (0 to 23)
    all_combinations = pd.DataFrame(list(product(range(1, 366), range(24))), columns=['pickup_day', 'pickup_hour'])

    # Merge with the original data to find missing rows
    merged = pd.merge(all_combinations, df, on=['pickup_day', 'pickup_hour'], how='left')

    # Find missing rows where num_rows is NaN (indicating missing data)
    missing_rows = merged[merged['num_rows'].isna()]

    # Fill missing rows with 0s for all columns except pickup_day and pickup_hour
    for col in df.columns:
        if col not in ['pickup_day', 'pickup_hour']:
            missing_rows[col] = 0

    # Combine the original dataframe with the missing rows
    complete_df = pd.concat([df, missing_rows], ignore_index=True)

    # Sort the resulting dataframe by pickup_day and pickup_hour to maintain the correct order
    complete_df = complete_df.sort_values(by=['pickup_day', 'pickup_hour']).reset_index(drop=True)
    
    return complete_df

# Example usage:
filled_data = insert_missing_rows(aggregated_data)

# Display the first few rows of the new dataframe
print(filled_data.head())

#number of rows with cluster_ID = 0
print('Number of rows with cluster_ID = 0: ', filled_data[filled_data['cluster_ID'] == 0].shape[0])
#number of rows with num_rows = 0
#print('Number of rows with num_rows = 0: ', filled_data[filled_data['num_rows'] == 0].shape[0])

#show the first few rows with cluster_ID = 0
#print(filled_data[filled_data['cluster_ID'] == 0].head())

#show the rows from 25 to 30
#print(filled_data[25:30])

#reassign the values of cluster_ID as the row id of the dataframe
filled_data['cluster_ID'] =  filled_data.index

#dimension of filled_data
print('Dimension of filled_data: ', filled_data.shape)

#print the pickup_hour that have 0 num_rows and pickup_day = 1
print('pickup_hour that have 0 num_rows and pickup_day = 2: ', filled_data[(filled_data['num_rows'] == 0) & (filled_data['pickup_day'] == 2)]['pickup_hour'].unique()) 

#print the 
#print('pickup_hour that have 0 num_rows: ', filled_data[filled_data['num_rows'] == 0]['pickup_hour'].unique())