#add a feature: month to the hourly_data_final.
def add_month(df):
    # Define the base date as 2023-01-01
    base_date = datetime.date(2023, 1, 1)

    # Create a new column 'month' by calculating the correct month
    df['month'] = df['pickup_day'].apply(lambda x: (base_date + datetime.timedelta(days=x - 1)).month)

    return df

# Example usage:
hourly_data_month = add_month(hourly_data_final)



# Initialize an empty DataFrame to store the final results with Fourier features
fourier_features_final = pd.DataFrame()

# Function to extract top N Fourier features for a time series
def extract_top_fourier_features(time_series, top_n=5):

    fft_values = np.fft.fft(time_series)
    frequencies = np.fft.fftfreq(len(time_series), 1)
    
    # Compute amplitudes
    amplitude = np.abs(fft_values)
    
    # Sort the amplitudes in descending order to get the top N values
    sorted_indices = np.argsort(amplitude)[::-1]
    
    # Get the top N frequencies and amplitudes
    top_frequencies = frequencies[sorted_indices][:top_n]
    top_amplitudes = amplitude[sorted_indices][:top_n]

    # Create a dictionary to hold the features
    features = {}
    for i in range(top_n):
        features[f'f_{i+1}'] = top_frequencies[i]
        features[f'a_{i+1}'] = top_amplitudes[i]
    
    return features

# Iterate over each month (1 to 12)
for month in range(1, 13):
    # Extract the data for the current month
    monthly_data = hourly_data_month[hourly_data_month['month'] == month].copy()

    # Extract the 'num_rows' time series for Fourier Transformation
    num_rows_series = monthly_data['num_rows'].values
    
    # Apply Fourier Transformation and extract top 5 features for this month
    fourier_features = extract_top_fourier_features(num_rows_series, top_n=5)
    
    # Convert the dictionary of features to a DataFrame and replicate it for all rows in this month
    features_df = pd.DataFrame([fourier_features] * len(monthly_data))
    
    # Concatenate the features with the original data for the current month
    monthly_with_features = pd.concat([monthly_data.reset_index(drop=True), features_df.reset_index(drop=True)], axis=1)
    
    # Append the results to the final DataFrame for all months
    fourier_features_final = pd.concat([fourier_features_final, monthly_with_features], ignore_index=True)


# Display the first few rows of the final DataFrame with Fourier features
#print(fourier_features_final.head())

#drop the f1 feature
fourier_features_final = fourier_features_final.drop(['f_1'], axis=1)

#print the count of unique features of a_1
#print('Counts of a_1: ', fourier_features_final['a_1'].value_counts())
