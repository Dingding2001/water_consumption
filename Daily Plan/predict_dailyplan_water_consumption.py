import pandas as pd
import csv

encoding_declaration = ['# -*- coding: utf-8 -*-\n']

file_path = "Daily Plan/dailyplan-waterconsumption.csv"

cleaned_data = []

with open(file_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        cleaned_row = [field.replace(" ", "") for field in row]
        cleaned_data.append(cleaned_row)


with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(cleaned_data)

print(f"Spaces have been removed from '{file_path}'.")

data = pd.read_csv('Daily Plan/dailyplan-waterconsumption.csv')

ref = pd.read_csv('Water Energy Consumption/water fee.csv')

data['weekday-water'] = (data['firstbath1'] * ((5.7 * ref['bath-fre-winter'] * ref['bath-time-winter'] + 5.7 * ref['bath-fre-summer'] * ref['bath-time-summer'] + 5.7 * ref['bath-fre-spring'] * ref['bath-time-spring']) / (3 * 30)) + 
                        data['secondbath1'] * ((5.7 * ref['bath-fre-winter'] * ref['bath-time-winter'] + 5.7 * ref['bath-fre-summer'] * ref['bath-time-summer'] + 5.7 * ref['bath-fre-spring'] * ref['bath-time-spring']) / (3 * 30)) + 
                        data['breakfast1'] * ref['cook-consume'] / 30 +
                        data['lunch1'] * ref['cook-consume'] / 30 +
                        data['dinner1'] * ref['cook-consume'] / 30 +
                        data['washclothes1'] * (((ref['washmachine-fre-winter'] * 20 + ref['handwash-fre-winter'] * ref['laundry-time'] * 3 + ref['handwash-fre-winter'] * ref['Num-clothes-rinsed'] * 8) + (ref['washmachine-fre-spring'] * 20 + ref['handwash-fre-spring'] * ref['laundry-time'] * 3 + ref['handwash-fre-spring'] * ref['Num-clothes-rinsed'] * 8) + (ref['washmachine-fre-summer'] * 20 + ref['handwash-fre-summer'] * ref['laundry-time'] * 3 + ref['handwash-fre-summer'] * ref['Num-clothes-rinsed'] * 8)) / (3 * 30)) + 
                        data['clean1'] * ((ref['dishes-num'] * ref['washes-avenum'] + 1.7 * ref['wash-time'] + 4 * ref['wash-cycle'] + (ref['Sweep-fre'] + ref['Mop-fre']) * 0.16 * 27) / 30) + 
                        data['footbath1'] * ((ref['footbath-fre-winter'] + ref['footbath-fre-summer'] + ref['footbath-fre-spring']) / (3 * 30))
                        )

data['weekend-water'] = (data['firstbath2'] * ((5.7 * ref['bath-fre-winter'] * ref['bath-time-winter'] + 5.7 * ref['bath-fre-summer'] * ref['bath-time-summer'] + 5.7 * ref['bath-fre-spring'] * ref['bath-time-spring']) / (3 * 30)) + 
                        data['secondbath2'] * ((5.7 * ref['bath-fre-winter'] * ref['bath-time-winter'] + 5.7 * ref['bath-fre-summer'] * ref['bath-time-summer'] + 5.7 * ref['bath-fre-spring'] * ref['bath-time-spring']) / (3 * 30)) + 
                        data['breakfast2'] * ref['cook-consume'] / 30 +
                        data['lunch2'] * ref['cook-consume'] / 30 +
                        data['dinner2'] * ref['cook-consume'] / 30 +
                        data['washclothes2'] * (((ref['washmachine-fre-winter'] * 20 + ref['handwash-fre-winter'] * ref['laundry-time'] * 3 + ref['handwash-fre-winter'] * ref['Num-clothes-rinsed'] * 8) + (ref['washmachine-fre-spring'] * 20 + ref['handwash-fre-spring'] * ref['laundry-time'] * 3 + ref['handwash-fre-spring'] * ref['Num-clothes-rinsed'] * 8) + (ref['washmachine-fre-summer'] * 20 + ref['handwash-fre-summer'] * ref['laundry-time'] * 3 + ref['handwash-fre-summer'] * ref['Num-clothes-rinsed'] * 8)) / (3 * 30)) + 
                        data['clean2'] * ((ref['dishes-num'] * ref['washes-avenum'] + 1.7 * ref['wash-time'] + 4 * ref['wash-cycle'] + (ref['Sweep-fre'] + ref['Mop-fre']) * 0.16 * 27) / 30) + 
                        data['footbath2'] * ((ref['footbath-fre-winter'] + ref['footbath-fre-summer'] + ref['footbath-fre-spring']) / (3 * 30))
                        )
data['year-water-consumption'] = 250 * data['weekday-water'] + 115 * data['weekend-water']

data.to_csv('Daily Plan/dailyplan-waterconsumption.csv', index=False)