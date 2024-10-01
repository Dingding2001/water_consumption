import pandas as pd
import csv

encoding_declaration = ['# -*- coding: utf-8 -*-\n']

file_path = "Water Energy Consumption/water fee.csv"

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

data = pd.read_csv('Water Energy Consumption/water fee.csv')

# 把原来的分类变量改为实际的次数或者时间
# bathing-module
def update_bath_fre(value):
    if value == 1:
        return 45
    elif value == 2:
        return 30
    elif value == 3:
        return 10
    elif value == 4:
        return 6
    elif value == 5:
        return 4
    elif value == 6:
        return 3
    else:
        return 0

data['bath-fre-winter'] = data['bath-fre-winter'].apply(update_bath_fre)
data['bath-fre-summer'] = data['bath-fre-summer'].apply(update_bath_fre)
data['bath-fre-spring'] = data['bath-fre-spring'].apply(update_bath_fre)
def update_bath_time(value):
    if value == 1:
        return 3
    elif value == 2:
        return 7.5
    elif value == 3:
        return 15
    elif value == 4:
        return 25
    elif value == 5:
        return 45
    elif value == 6:
        return 60
    else:
        return 0

data['bath-time-winter'] = data['bath-time-winter'].apply(update_bath_time)
data['bath-time-summer'] = data['bath-time-summer'].apply(update_bath_time)
data['bath-time-spring'] = data['bath-time-spring'].apply(update_bath_time)

def update_footbath_fre(value):
    if value == 1:
        return 45
    elif value == 2:
        return 30
    elif value == 3:
        return 10
    elif value == 4:
        return 6
    elif value == 5:
        return 4
    elif value == 6:
        return 2
    else:
        return 0

data['footbath-fre-winter'] = data['footbath-fre-winter'].apply(update_footbath_fre)
data['footbath-fre-summer'] = data['footbath-fre-summer'].apply(update_footbath_fre)
data['footbath-fre-spring'] = data['footbath-fre-spring'].apply(update_footbath_fre)

# cooking module
def update_cook_fre(value):
    if value == 1:
        return 30
    elif value == 2:
        return 4
    elif value == 3:
        return 1
    elif value == 4:
        return 0.5
    else:
        return 0
data['bread-machine-fre'] = data['bread-machine-fre'].apply(update_cook_fre)
data['soymilk-fre'] = data['soymilk-fre'].apply(update_cook_fre)
data['ele-stewpot-fre'] = data['ele-stewpot-fre'].apply(update_cook_fre)
data['gasstove-fre'] = data['gasstove-fre'].apply(update_cook_fre)
data['pressure-fre'] = data['pressure-fre'].apply(update_cook_fre)
data['rice-fre'] = data['rice-fre'].apply(update_cook_fre)
data['ele-pan-fre'] = data['ele-pan-fre'].apply(update_cook_fre)

# cleaning module
def update_clean_time(value):
    if value == 1:
        return 3
    elif value == 2:
        return 7.5
    elif value == 3:
        return 12.5
    elif value == 4:
        return 25
    elif value == 5:
        return 40
    else:
        return 0

data['wash-time'] = data['wash-time'].apply(update_clean_time)
data['laundry-time'] = data['laundry-time'].apply(update_clean_time)

def update_clean_fre(value):
    if value == 1:
        return 60
    elif value == 2:
        return 30
    elif value == 3:
        return 10
    elif value == 4:
        return 6
    elif value == 5:
        return 4
    elif value == 6:
        return 3
    else:
        return 0

data['Sweep-fre'] = data['Sweep-fre'].apply(update_clean_fre)
data['Mop-fre'] = data['Mop-fre'].apply(update_clean_fre)
data['handwash-fre-winter'] = data['handwash-fre-winter'].apply(update_clean_fre)
data['handwash-fre-spring'] = data['handwash-fre-spring'].apply(update_clean_fre)
data['handwash-fre-summer'] = data['handwash-fre-summer'].apply(update_clean_fre)
data['washmachine-fre-winter'] = data['washmachine-fre-winter'].apply(update_clean_fre)
data['washmachine-fre-spring'] = data['washmachine-fre-spring'].apply(update_clean_fre)
data['washmachine-fre-summer'] = data['washmachine-fre-summer'].apply(update_clean_fre)

# HVAC module
def update_HVAC_time(value):
    if value == 1:
        return 120
    elif value == 2:
        return 90
    elif value == 3:
        return 60
    elif value == 4:
        return 48
    elif value == 5:
        return 30
    elif value == 6:
        return 18
    elif value == 7:
        return 6
    else:
        return 0
data['time-heatequipment-winter'] = data['time-heatequipment-winter'].apply(update_HVAC_time)

# calculate water consumption
data['bath-winter-consume'] = 5.7 * data['bath-fre-winter'] * data['bath-time-winter'] + data['footbath-fre-winter'] #34
data['bath-summer-consume'] = 5.7 * data['bath-fre-summer'] * data['bath-time-summer'] + data['footbath-fre-summer']
data['bath-spring-consume'] = 5.7 * data['bath-fre-spring'] * data['bath-time-spring'] + data['footbath-fre-spring']
data['cook-consume'] = 0.5 * data['bread-machine-fre'] + 0.2 * data['soymilk-fre'] + 1.5 * data['ele-stewpot-fre'] + 0.8 * data['gasstove-fre'] + 2 * data['pressure-fre'] + 0.3 * data['rice-fre'] + 0.15 * data['ele-pan-fre'] + 2 * data['dishes-num']
data['wash-winter-consume'] = 2 * data['dishes-num'] * data['washes-avenum'] + 1.7 * data['wash-time'] + 4 * data['wash-cycle'] + (data['Sweep-fre'] + data['Mop-fre']) * 0.16 * 27 + data['washmachine-fre-winter'] * 20 + data['handwash-fre-winter'] * data['laundry-time'] * 3 + data['handwash-fre-winter'] * data['Num-clothes-rinsed'] * 8
data['wash-spring-consume'] = 2 * data['dishes-num'] * data['washes-avenum'] + 1.7 * data['wash-time'] + 4 * data['wash-cycle'] + (data['Sweep-fre'] + data['Mop-fre']) * 0.16 * 27 + data['washmachine-fre-spring'] * 20 + data['handwash-fre-spring'] * data['laundry-time'] * 3 + data['handwash-fre-spring'] * data['Num-clothes-rinsed'] * 8
data['wash-summer-consume'] = 2 * data['dishes-num'] * data['washes-avenum'] + 1.7 * data['wash-time'] + 4 * data['wash-cycle'] + (data['Sweep-fre'] + data['Mop-fre']) * 0.16 * 27 + data['washmachine-fre-summer'] * 20 + data['handwash-fre-summer'] * data['laundry-time'] * 3 + data['handwash-fre-summer'] * data['Num-clothes-rinsed'] * 8
data['hvac-consume-winter'] = 2 * data['time-heatequipment-winter']

data['winter-consume'] = ( data['bath-winter-consume'] + data['cook-consume'] + data['wash-winter-consume'] + data['hvac-consume-winter'] ) / 1000 #42
data['spring-consume'] = ( data['bath-spring-consume'] + data['cook-consume'] + data['wash-spring-consume'] ) / 1000
data['summer-consume'] = ( data['bath-summer-consume'] + data['cook-consume'] + data['wash-summer-consume'] ) / 1000
data['year-consume'] = data['winter-consume'] * 3 + data['spring-consume'] * 6 + data['summer-consume'] * 3

data['family-water-winter'] = data['hhd'].map(data.groupby('hhd')['winter-consume'].sum()) #46
data['family-water-spring'] = data['hhd'].map(data.groupby('hhd')['spring-consume'].sum())
data['family-water-summer'] = data['hhd'].map(data.groupby('hhd')['summer-consume'].sum())
data['family-water-year'] = data['hhd'].map(data.groupby('hhd')['year-consume'].sum())

# calculate water fee

def calculate_water_bill(volume):
    if volume <= 22:
       price = volume * 2.67 + volume * 1 + round( 0.9 * volume ) * 0.59
    elif 23 <= volume <= 30:
       price = 22 * 2.67 + (volume - 22) * 4.01 + volume * 1 + round( 0.9 * volume ) * 0.59
    else:
       price = 22 * 2.67 + 8 * 4.01 + (volume - 30) * 8.01 + volume * 1 + round( 0.9 * volume ) * 0.59
    return round(price,2)

data['winter-fee'] = data['winter-consume'].apply(calculate_water_bill) #50
data['spring-fee'] = data['spring-consume'].apply(calculate_water_bill)
data['summer-fee'] = data['summer-consume'].apply(calculate_water_bill)
data['year-fee'] = data['year-consume'].apply(calculate_water_bill)

data['family-winter-fee'] = data['family-water-winter'].apply(calculate_water_bill) #54
data['family-spring-fee'] = data['family-water-spring'].apply(calculate_water_bill)
data['family-summer-fee'] = data['family-water-summer'].apply(calculate_water_bill)
data['family-year-fee'] = data['family-water-year'].apply(calculate_water_bill)


data.to_csv('Water Energy Consumption/water fee.csv', index=False)