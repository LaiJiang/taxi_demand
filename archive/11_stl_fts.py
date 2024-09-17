from statsmodels.tsa.seasonal import STL
import pandas as pd

# Function to perform STL decomposition and extract features
def extract_stl_features(time_series, seasonal_period=25):
    stl = STL(time_series, seasonal=seasonal_period, period=seasonal_period)
    result = stl.fit()
    
    # Create a DataFrame to store the extracted features
    stl_features = pd.DataFrame({
        'trend': result.trend,
        'seasonal': result.seasonal,
        'residual': result.resid
    })
    
    return stl_features

# Function to perform STL decomposition and extract features for each month
def extract_stl_features_by_month(data, target_column, seasonal_period=25):

    stl_features_final = pd.DataFrame()  # To store the final result
    
    # Loop through each unique month
    for month in range(1, 13):
        # Extract the subset of data for the current month
        monthly_data = data[data['month'] == month].copy()
        
        # Perform STL decomposition on the target column (e.g., 'num_rows')
        time_series = monthly_data[target_column].values
        
        if len(time_series) >= seasonal_period:
            # Perform STL decomposition
            stl_features = extract_stl_features(time_series, seasonal_period)
            
            # Append the results for this month to the final DataFrame
            stl_features_final = pd.concat([stl_features_final, stl_features], ignore_index=True)
    
    return stl_features_final

#stl features for the daily, semi-daily and semi-weekly seasonal periods
stl_features_daily = extract_stl_features_by_month(fourier_features_final, target_column='num_rows', seasonal_period=25)
stl_features_semi_daily = extract_stl_features_by_month(fourier_features_final, target_column='num_rows', seasonal_period=13)
stl_features_semi_weekly = extract_stl_features_by_month(fourier_features_final, target_column='num_rows', seasonal_period=169)

#combine
stl_features_final = pd.concat([stl_features_daily, stl_features_semi_daily, stl_features_semi_weekly], axis=1)
#print dimension
print('Dimension of stl_features_final: ', stl_features_final.shape)

#the column names as "STL_trend_daily", "STL_seasonal_daily", "STL_residual_daily", "STL_trend_semi_daily", "STL_seasonal_semi_daily", "STL_residual_semi_daily", "STL_trend_semi_weekly", "STL_seasonal_semi_weekly", "STL_residual_semi_weekly"
stl_features_final.columns = ['STL_trend_daily', 'STL_seasonal_daily', 'STL_residual_daily', 'STL_trend_semi_daily', 'STL_seasonal_semi_daily', 'STL_residual_semi_daily', 'STL_trend_semi_weekly', 'STL_seasonal_semi_weekly', 'STL_residual_semi_weekly']

#now add these features to the fourier_features_final
stl_fourier_features = pd.concat([fourier_features_final, stl_features_final], axis=1)
#print column names of stl_fourier_features
print(stl_fourier_features.columns)
