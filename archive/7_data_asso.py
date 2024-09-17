#draw the num_rows value against the cluster_ID, colored by the day_of_week
#reduce the size of the dots

# Create the plot with connected lines between the points (omit scatter points)
plt.figure(figsize=(10, 5))
plt.plot(smoothed_data_add['cluster_ID'], smoothed_data_add['num_rows'], 
         color='b')  # 'b' is for blue color line

plt.xlabel('Hour ID')
plt.ylabel('Demands')
plt.title('Demands vs. Hour ID (connected line)')
plt.grid(True)  # Optional: Adds a grid for better visualization

# Save the figure
plt.savefig('Demand_2023_line_plot.png')
plt.close()



# Create the scatter plot with smaller dots (size controlled by 's' parameter)
plt.figure(figsize=(10, 5))
plt.scatter(smoothed_data_add['cluster_ID'], smoothed_data_add['num_rows'], 
            c=smoothed_data_add['day_of_week'], cmap='viridis', s=20)  # 's' controls the size, try reducing to 20

plt.xlabel('Hour ID')
plt.ylabel('Demand')
plt.title('Deman s vs. Hour ID (Colored by Day of Week)')
plt.colorbar(label='Day of Week')

# Save the figure
plt.savefig('Demand_2023_day_of_week.png')
plt.close()


#create a heatmap of the number of rows for each day of the week and hour of the day
# Create a pivot table to aggregate the data
pivot_table = smoothed_data_add.pivot_table(index='day_of_week', columns='pickup_hour', values='num_rows', aggfunc='median')
# Create the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, cmap='viridis')
plt.xlabel('Hour of Day')
plt.ylabel('Day of Week')
plt.title('Median number of demands by Hour and Day')
plt.savefig('heatmap_hour_day.png')
plt.close()

#heat map of the number of rows for each day of the week and week of the month
# Create a pivot table to aggregate the data
pivot_table = smoothed_data_add.pivot_table(index='day_of_week', columns='week_of_month', values='num_rows', aggfunc='median')
# Create the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, cmap='viridis')
plt.xlabel('Week of Month')
plt.ylabel('Day of Week')
plt.title('Median number of demands by Week and Day')
plt.savefig('heatmap_week_day.png')
plt.close()

#plot the boxplot of the number of rows for binary variable holiday
plt.figure(figsize=(10, 5))
sns.boxplot(x='holiday', y='num_rows', data=smoothed_data_add)
plt.xlabel('Holiday')
plt.ylabel('Number of Demands')
plt.title('Number of Demands on Holidays vs. Non-Holidays')
plt.savefig('boxplot_holiday.png')
plt.close()
#test for the difference of the number of rows between holidays and non-holidays
from scipy.stats import ttest_ind
#perform the t-test
holiday = smoothed_data_add[smoothed_data_add['holiday'] == 1]['num_rows']
non_holiday = smoothed_data_add[smoothed_data_add['holiday'] == 0]['num_rows']
t_stat, p_value = ttest_ind(holiday, non_holiday)
print('P-value for t-test of demand vs holiday (yes or no):', p_value)

#draw the scatter plot of the number of rows against the temperature_2m
plt.figure(figsize=(10, 5))
plt.scatter(smoothed_data_add['temperature_2m'], smoothed_data_add['num_rows'], s=20)
plt.xlabel('Temperature')
plt.ylabel('Number of Demands')
plt.title('Number of Demands vs. Temperature')
plt.savefig('demand_temperature.png')
plt.close()

#test for the correlation between the number of rows and the temperature_2m
from scipy.stats import pearsonr
#perform the t-test
corr, p_value = pearsonr(smoothed_data_add['temperature_2m'], smoothed_data_add['num_rows'])
print('Correlation between temperature and demand:', corr)
print('P-value for correlation between temperature and demand:', p_value)

#plot the scatter plot of the number of rows against the precipitation
plt.figure(figsize=(10, 5))
plt.scatter(smoothed_data_add['precipitation'], smoothed_data_add['num_rows'], s=20)
plt.xlabel('Precipitation')
plt.ylabel('Number of Demands')
plt.title('Number of Demands vs. Precipitation')
plt.savefig('demand_precipitation.png')
plt.close()

#test for the correlation between the number of rows and the precipitation
#perform the t-test
corr, p_value = pearsonr(smoothed_data_add['precipitation'], smoothed_data_add['num_rows'])
print('Correlation between precipitation and demand:', corr)
print('P-value for correlation between precipitation and demand:', p_value)

#plot the scatter plot of the number of rows against the rain
plt.figure(figsize=(10, 5))
plt.scatter(smoothed_data_add['rain'], smoothed_data_add['num_rows'], s=20)
plt.xlabel('Rain')
plt.ylabel('Number of Demands')
plt.title('Number of Demands vs. Rain')
plt.savefig('demand_rain.png')
plt.close()

#correlation between the train and precipitation
corr, p_value = pearsonr(smoothed_data_add['rain'], smoothed_data_add['precipitation'])
print('Correlation between rain and precipitation:', corr)
print('P-value for correlation between rain and precipitation:', p_value)

#plot the scatter plot of the number of rows against the snowfall
plt.figure(figsize=(10, 5))
plt.scatter(smoothed_data_add['snowfall'], smoothed_data_add['num_rows'], s=20)
plt.xlabel('Snowfall')
plt.ylabel('Number of Demands')
plt.title('Number of Demands vs. Snowfall')
plt.savefig('demand_snowfall.png')
plt.close()

#test for the correlation between the number of rows and the snowfall
#perform the t-test
corr, p_value = pearsonr(smoothed_data_add['snowfall'], smoothed_data_add['num_rows'])
print('Correlation between snowfall and demand:', corr)
print('P-value for correlation between snowfall and demand:', p_value)

#test for the correlation between the number of rows and the snowfall only for the days with snowfall > 0
#perform the t-test
corr, p_value = pearsonr(smoothed_data_add[smoothed_data_add['snowfall'] > 0]['snowfall'], smoothed_data_add[smoothed_data_add['snowfall'] > 0]['num_rows'])
print('Correlation between snowfall and demand on snowy days:', corr)
print('P-value for correlation between snowfall and demand on snowy days:', p_value)

#remove the snowfall and rain columns
hourly_data_final = smoothed_data_add.drop(['snowfall', 'rain'], axis=1)

#save data
hourly_data_final.to_csv('/Users/laijiang/Documents/Pers/datatest/Data/save/hourly_data_final.csv', index=False)
