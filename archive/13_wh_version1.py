from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pandas as pd


# Assuming 'hourly_data_final' contains your time series data and 'num_rows' is the target column
train_data = stl_fourier_features[stl_fourier_features['month'] <= 9]  # Jan to Sep for training
test_data = stl_fourier_features[stl_fourier_features['month'] > 9]  # Oct

#reset the index
train_data = train_data.reset_index(drop=True)
test_data = test_data.reset_index(drop=True)


#time_series = train_data['num_rows']  # Time series to train on


#alpha can be 0.1, 0.5, 0.9, beta can be 0.1, 0.5, 0.9, gamma can be 0.1, 0.5, 0.9
#create a list of the parameter value combinations
alpha_values = [0.1, 0.5, 0.9]
beta_values = [0.1, 0.5, 0.9]
gamma_values = [0.1, 0.5, 0.9]

# Generate all combinations of alpha, beta, and gamma using product
params_abc = list(product(alpha_values, beta_values, gamma_values))
params_abc = pd.DataFrame(params_abc, columns=['Alpha', 'Beta', 'Gamma'])


def generate_hw_features(train_data, params_abc, seasonal_lengths, target_column='num_rows'):
    hw_features = pd.DataFrame()  # Initialize an empty DataFrame to store the results
    
    # Loop through each seasonal length (e.g., 24, 168)
    for i_season in seasonal_lengths:
        # Loop through each parameter combination (alpha, beta, gamma)
        for j_params in range(len(params_abc)):
            # Get the alpha, beta, and gamma values for the current parameter set
            alpha = params_abc['Alpha'][j_params]
            beta = params_abc['Beta'][j_params]
            gamma = params_abc['Gamma'][j_params]
            
            # Convert series to numpy array to avoid pandas indexing issues
            time_series = train_data[target_column].values
            
            # Calculate the Holt-Winters predictions using the triple_exponential_smoothing function
            predict_hw = triple_exponential_smoothing(time_series, i_season, alpha, beta, gamma, 0)
            
            # Store the result as a new column in the hw_features DataFrame
            column_name = f'hw_{i_season}_{j_params}'
            hw_features[column_name] = predict_hw
    
    return hw_features

# Example usage
seasonal_lengths = [24, 168]  # The two seasonal lengths
hw_features_train = generate_hw_features(train_data, params_abc, seasonal_lengths, target_column='num_rows')
hw_features_test = generate_hw_features(test_data, params_abc, seasonal_lengths, target_column='num_rows')

#now attach hw_features_train to the train_data
train_data = pd.concat([train_data, hw_features_train], axis=1)
#now attach hw_features_test to the test_data
test_data = pd.concat([test_data, hw_features_test], axis=1)
