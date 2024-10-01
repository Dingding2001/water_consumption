import pandas as pd
import csv

encoding_declaration = ['# -*- coding: utf-8 -*-\n']

file_path = "Water Energy Consumption/generate others appliances.csv"

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

df = pd.read_csv('Water Energy Consumption/generate others appliances.csv')

# 找到relationship为1的人和相应属性
person1 = df[df['relationship'] == 1]

# 保持特定属性相同
attributes = ['Electric-Footbath', 'Water-heater', 'showerhead', 'thermostatic', 'Faucet', 'Dishwasher',
              'sterilizer', 'sweeping-robot', 'Electric-mop', 'Intelligent-Toilet', 'Washing-machine',
              'Dry-or-sterilize', 'pressure', 'microwave-oven', 'soymilk', 'Ele-oven', 'Terminal-water',
              'Kitchen-water-heat', 'radiator-bag']

# 根据'hhd'进行分组并将属性相同的值赋给其他人
df.update(df.groupby('hhd')[attributes].ffill().bfill())

# 将结果保存回原始CSV文件中
df.to_csv('Water Energy Consumption/generate others appliances.csv', index=False)