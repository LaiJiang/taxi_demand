smoothed_data_final = pd.read_csv('/Users/laijiang/Documents/Pers/datatest/Data/save/smoothed_data_final.csv')


def add_day_of_week(df):
    # Define the base date as 2023-01-01 (which is a Sunday)
    base_date = datetime.date(2023, 1, 1)

    # Create a new column 'day_of_week' by calculating the correct day of the week
    # 1: Monday, 2: Tuesday, ..., 7: Sunday (as per isoweekday())
    df['day_of_week'] = df['pickup_day'].apply(lambda x: (base_date + datetime.timedelta(days=x - 1)).isoweekday())

    return df

# Example usage:
smoothed_data_add = add_day_of_week(smoothed_data_final)

# Display the first few rows of the updated dataframe
#print(smoothed_data_add.head())

#table of counts of day_of_week
#print('Counts of day_of_week: ', smoothed_data_add['day_of_week'].value_counts())


def add_week_of_month(df):
    # Define the base date as 2023-01-01
    base_date = datetime.date(2023, 1, 1)

    # Function to calculate the correct week of the month
    def week_of_month(date):
        return (date.day - 1) // 7 + 1  # This ensures that days 1-7 are week 1, 8-14 are week 2, etc.

    # Create the 'week_of_month' feature by applying the week_of_month function
    df['week_of_month'] = df['pickup_day'].apply(lambda x: week_of_month(base_date + datetime.timedelta(days=x - 1)))

    return df

smoothed_data_add = add_week_of_month(smoothed_data_add)

#print('Counts of week_of_month: ', smoothed_data_add['week_of_month'].value_counts())

#add a binary feature "holiday" that equals to 1 only for holidays
def add_holiday(df):
    # Define the holidays by their pickup_day
    holidays = [1, 2, 16, 44, 51, 99, 134, 149, 169, 170, 185, 247, 282, 311, 315, 327, 359]

    # Create the 'holiday' feature by checking if the pickup_day is in the list of holidays
    df['holiday'] = df['pickup_day'].apply(lambda x: 1 if x in holidays else 0)

    return df

smoothed_data_add = add_holiday(smoothed_data_add)

#print('Counts of holiday: ', smoothed_data_add['holiday'].value_counts())

#print the first few rows
print(smoothed_data_add.head())

#load the weather data for 2023 
weather_data = pd.read_csv('/Users/laijiang/Documents/Pers/datatest/Data/dat/Bronx_Weather_Data2023.csv')

#name the first column as row_index
weather_data = weather_data.rename(columns={'Unnamed: 0': 'row_index'})

#print the first few rows
print(weather_data.head())

#combine weather_data with smoothed_data_add
smoothed_data_add = pd.merge(smoothed_data_add, weather_data, left_on='cluster_ID', right_on='row_index', how='left')

#print(smoothed_data_add.head())

#plot the distribution of temperature_2m
plt.hist(smoothed_data_add['temperature_2m'], bins=30, edgecolor='black')  # Add edgecolor to distinguish bars
plt.xlabel('Temperature')
plt.ylabel('Frequency')
plt.title('Distribution of Temperature')
plt.savefig('temperature.png')
plt.close()


#plot the distribution of precipitation
plt.hist(smoothed_data_add['precipitation'], bins=30)
plt.xlabel('Precipitation')
plt.ylabel('Frequency')
plt.title('Distribution of Precipitation')
plt.savefig('precipitation.png')
plt.close()

#plot the distribution of rain
plt.hist(smoothed_data_add['rain'], bins=30)
plt.xlabel('Rain')
plt.ylabel('Frequency')
plt.title('Distribution of Rain')
plt.savefig('rain.png')
plt.close()

#plot the distribution of snowfall
plt.hist(smoothed_data_add['snowfall'], bins=30)
plt.xlabel('Snowfall')
plt.ylabel('Frequency')
plt.title('Distribution of Snowfall')
plt.savefig('snowfall.png')
plt.close()


#check summary statistics of temperature_2m  precipitation  rain  snowfall  
print('Summary statistics of temperature_2m: ', smoothed_data_add['temperature_2m'].describe())
print('Summary statistics of precipitation: ', smoothed_data_add['precipitation'].describe())
print('Summary statistics of rain: ', smoothed_data_add['rain'].describe())
print('Summary statistics of snowfall: ', smoothed_data_add['snowfall'].describe())

#all looks fine!
#save files
smoothed_data_add.to_csv('/Users/laijiang/Documents/Pers/datatest/Data/save/smoothed_data_add.csv', index=False)