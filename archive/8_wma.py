
# Function to calculate MAPE
def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) 

# Function to compute the Weighted Moving Average (WMA)
def func_wma(data, window_size):
    weights = np.arange(1, window_size + 1)  # Weights are 1, 2, ..., window_size
    wma = data.rolling(window_size).apply(lambda values: np.dot(values, weights) / weights.sum(), raw=True)
    wma = wma.round(0)  # Round the WMA predictions
    wma = wma.dropna()  # Drop NaN values 
    #drop the last value of wma
    wma = wma[:-1]
    data = data[window_size:]  # Drop the first few rows to match the length 
    mape = mean_absolute_percentage_error(data, wma)
    return mape

# Example data (replace this with your actual DataFrame)
# hourly_data_final = pd.read_csv('your_file.csv')

window_size = 2  # You can adjust this as needed

# Calculate WMA for num_rows
wma2 = func_wma(hourly_data_final['num_rows'], window_size)
#print the MAPE
print('Baseline model: WMA2, WMA with window size 2')
print('MAPE of baseline model WMA2:', wma2.round(4))





