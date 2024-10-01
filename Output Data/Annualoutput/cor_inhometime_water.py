#%%
import pandas as pd
import os

years = list(range(2010, 2054))
data = pd.DataFrame(columns=['year', 'cor_weekday','cor_weekend'])

for year in years:
    csv_file_path = f"inhome-time{year}year.csv"
    if os.path.isfile(csv_file_path):
        df = pd.read_csv(csv_file_path)
        
        column1 = df['weekday-inhome-time']
        column2 = df['dailyplan-water']
        correlation1 = column1.corr(column2)
        
        column3 = df['weekend-inhome-time']
        column4 = df['dailyplan-water']
        correlation2 = column3.corr(column4)

        average_value_weekday = sum(df['weekday-inhome-time']) / len(df['weekday-inhome-time'])
        average_value_weekend = sum(df['weekend-inhome-time']) / len(df['weekend-inhome-time'])
        average_value_water = sum(df['dailyplan-water']) / len(df['dailyplan-water'])
        data = pd.concat([data, pd.DataFrame({'year': [year], 'cor_weekday': [correlation1], 'cor_weekend': [correlation2], 'average_weekday_time':[average_value_weekday], 'average_weekend_time':[average_value_weekend], 'average_water':[average_value_water]})], ignore_index=True)
      
        
data.to_csv('cor_inhometime_water.csv')
print(data)
# %%
