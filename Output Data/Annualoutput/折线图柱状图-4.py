#%%
import csv
import re
import pandas as pd
import os
import numpy as np
import math
from datetime import datetime
file_path = "SelfSim-water-dailyplan cleaning appliances.csv"

#start_row表示第几行开始是数据
start_row = 25

#y_interval词条为y轴间隔，除了Householdlncome Population Change是自动调节，其他图因为多条线因此间隔是需要手动设置的
#索引从0开始，所以第28行在索引中是27,因此下面-1
start_row = start_row - 1
#x=0的开始年份
Year = 2020


data = pd.read_csv(file_path, skiprows=start_row)
data.to_csv('del_first.csv', index=True, encoding='utf-8')
first_file = 'del_first.csv'
second_file = 'del_second.csv'

with open(first_file, 'r', encoding='utf-8') as csvfile, open(second_file, 'w', encoding='utf-8', newline='') as output_csvfile:
    reader = csv.reader(csvfile)
    writer = csv.writer(output_csvfile)

    for row in reader:
        new_row = [data.strip('"') if isinstance(data, str) else data for data in row]
        writer.writerow(new_row)

data2 = pd.read_csv(second_file)
data2 = data2.rename(columns=lambda x: '' if 'Unnamed' in str(x) else x)
data2 = data2.replace("'", "")
#data2 = data2.dropna()


def round_and_remove_decimal(num):
    if isinstance(num, (int, float)) and not math.isnan(num):
        return round(num)
    else:
        return num

data2 = data2.round(0)
data2 = data2.applymap(round_and_remove_decimal)


data2.to_csv('del_second.csv', index=False)
def round_and_remove_decimal(num):
    if isinstance(num, str):

        num_parts = num.split('.')
        return num_parts[0]
    else:

        return num


data2 = data2.applymap(round_and_remove_decimal)

data2.to_csv('del_second.csv', index=False)
#%%
with open('del_second.csv', 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)
    

    x_y_columns = []
    
    for row in reader:
        for i, cell in enumerate(row):
            if i < len(headers) and (cell == 'x' or cell == 'y'):
                x_y_columns.append(i)
        
with open('del_third.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    

    writer.writerow(headers)
    
    with open('del_second.csv', 'r') as file:
        reader = csv.reader(file)
        
        next(reader)
    
        for row in reader:
            new_row = [row[i] for i in x_y_columns]
            writer.writerow(new_row)
#%%
def read_csv_and_clean(filename):
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
        
    header = [entry for entry in data[0] if entry != '']
    cleaned_data = data[1:]
    
    new_filename = 'del_fourth.csv'
    with open(new_filename, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(cleaned_data)
        
    return header

filename = 'del_third.csv'
type_table = read_csv_and_clean(filename)
print(type_table)
#print(new_filename)
#%%
data = pd.read_csv('del_fourth.csv')
columns = type_table
groups = []
output_folder = '输出分类'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for i in range(0, len(data.columns), 2):
    group = data.iloc[:, i:i+2]  
    group.columns = ['x', 'y'] 
    output_file_name = f"{type_table[i//2]}.csv"
    output_file = os.path.join(output_folder, output_file_name)

    # 过滤掉 'x' 列值为 0 的行
    group = group[group['x'] != 0]

    group.to_csv(output_file, index=False)
    

file_names = [file for file in os.listdir(output_folder) if file.endswith('.csv')]

for file_name in file_names:
    file_path = os.path.join(output_folder, file_name)

    df = pd.read_csv(file_path)
    
    # 在"x"列中加入Year的值
    df['x'] = df['x'] + Year

    df.to_csv(file_path, index=False)
#%%
current_directory = os.getcwd()
files_and_folders = os.listdir(current_directory)

for item in files_and_folders:
    if item.startswith("del_") and item.endswith(".csv"):
        file_path = os.path.join(current_directory, item)
        os.remove(file_path)
#%%

#画图


import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
#Male Female
output_folder_line = '输出分类\折线图'
if not os.path.exists(output_folder_line):
    os.makedirs(output_folder_line)
output_folder_bar = '输出分类\柱状图'
if not os.path.exists(output_folder_bar):
    os.makedirs(output_folder_bar)

folder_path = '输出分类'
# %%
dishwasher = pd.read_csv(os.path.join(folder_path, 'dishwasher.csv'))
sterilizer = pd.read_csv(os.path.join(folder_path, 'sterilizer.csv'))
sweeping_robot = pd.read_csv(os.path.join(folder_path, 'sweeping-robot.csv'))
elemop = pd.read_csv(os.path.join(folder_path, 'ele-mop.csv'))
toilet = pd.read_csv(os.path.join(folder_path, 'intelligent-toilet.csv'))

# 绘制折线图
plt.plot(dishwasher['x'], dishwasher['y'], label='dishwasher', marker='o', color='blue', linewidth=2, linestyle='dotted')
plt.plot(sterilizer['x'], sterilizer['y'], label='sterilizer', marker='o', color='green', linewidth=2, linestyle='dotted')
plt.plot(sweeping_robot['x'], sweeping_robot['y'], label='sweeping-robot', marker='o', color='orange', linewidth=2, linestyle='dotted')
plt.plot(elemop['x'], elemop['y'], label='eletric-mop', marker='o', color='red', linewidth=2, linestyle='dotted')
plt.plot(toilet['x'], toilet['y'], label='intelligent-toilet', marker='o', color='purple', linewidth=2, linestyle='dotted')

# 设置图的标签、标题等
plt.xlabel('Year')
plt.ylabel('Number')
plt.xticks(dishwasher['x'], dishwasher['x'].tolist())
y_interval = 1000  # 设置你希望的y轴间隔

# 计算y轴的最小和最大值
y_min = min(dishwasher['y'].min(), sterilizer['y'].min(), sweeping_robot['y'].min(), elemop['y'].min(), toilet['y'].min()) - y_interval
y_max = max(dishwasher['y'].max(), sterilizer['y'].max(), sweeping_robot['y'].max(), elemop['y'].max(), toilet['y'].max()) + y_interval

# 设置y轴刻度间隔和最小最大值
ax = plt.gca()
ax.yaxis.set_major_locator(MultipleLocator(base=y_interval))
ax.set_ylim([y_min, y_max])
plt.tight_layout()
plt.legend(loc='upper center', fontsize=8, bbox_to_anchor=(0.5, -0.2), ncol=2)
plt.tight_layout(rect=(0, 0, 1, 0.9))
plt.ticklabel_format(style='plain', axis='y')
plt.xlim(min(dishwasher['x'].min(), sterilizer['x'].min(), sweeping_robot['x'].min(), elemop['x'].min(), toilet['x'].min()) - 0.25, max(dishwasher['x'].max(), sterilizer['x'].max(), sweeping_robot['x'].max(), elemop['x'].max(), toilet['x'].max()) + 0.25)
plt.grid()
plt.savefig(os.path.join(output_folder_line, 'Cleaning Appliances'))
plt.show()

# 柱状图
# 设置图的标签、标题等
plt.xlabel('Year')
plt.ylabel('Number')
plt.xticks(dishwasher['x'], dishwasher['x'].tolist())

# 绘制多年柱状图
width = 0.15  # 柱状图的宽度
plt.bar(dishwasher['x'] - 2*width, dishwasher['y'], width, label='dishwasher', color='blue')
plt.bar(sterilizer['x'] - width, sterilizer['y'], width, label='sterilizer', color='green')
plt.bar(sweeping_robot['x'], sweeping_robot['y'], width, label='sweeping-robot', color='orange')
plt.bar(elemop['x'] + width, elemop['y'], width, label='eletric-mop', color='red')
plt.bar(toilet['x'] + 2*width, toilet['y'], width, label='intelligent-toilet', color='purple')
plt.tight_layout()
plt.legend()

output_folder_bar = '输出分类\柱状图'
plt.savefig(os.path.join(output_folder_bar, 'Cleaning Appliances'))
plt.show()
# %%
washmachine1 = pd.read_csv(os.path.join(folder_path, 'washmachine-1.csv'))
washmachine2 = pd.read_csv(os.path.join(folder_path, 'washmachine-2.csv'))

# 绘制折线图
plt.plot(washmachine1['x'], washmachine1['y'], label='drum washing machine',marker='o', color='blue',linewidth=2,linestyle='dotted')  
plt.plot(washmachine2['x'], washmachine2['y'], label='pulsator washing machine',marker='o', color='red',linewidth=2,linestyle='dotted')  

# 设置图的标签、标题等
plt.xlabel('Year')
plt.ylabel('Number')
plt.xticks(washmachine1['x'], washmachine1['x'].tolist())  
y_interval = 500  # 设置你希望的y轴间隔

# 计算y轴的最小和最大值
y_min = min(washmachine1['y'].min(), washmachine2['y'].min()) - y_interval/2
y_max = max(washmachine1['y'].max(), washmachine2['y'].max()) + y_interval/2

# 设置y轴刻度间隔和最小最大值
ax = plt.gca()
ax.yaxis.set_major_locator(MultipleLocator(base=y_interval))
ax.set_ylim([y_min, y_max])
plt.tight_layout()
plt.legend(loc='upper center', fontsize=8, bbox_to_anchor=(0.5, -0.2), ncol=2)
plt.tight_layout(rect=(0, 0, 1, 0.9))
plt.ticklabel_format(style='plain', axis='y')
plt.xlim(min(washmachine1['x'].min(), washmachine2['x'].min()) - 0.25, max(washmachine1['x'].max(), washmachine2['x'].max()) + 0.25)
plt.grid()
plt.savefig(os.path.join(output_folder_line, 'washing machine model'))
plt.show()

#柱状图
# 设置图的标签、标题等
plt.xlabel('Year')
plt.ylabel('Number')
plt.xticks(washmachine1['x'], washmachine1['x'].tolist())   

# 绘制多年柱状图
width = 0.35  # 柱状图的宽度
plt.bar(washmachine1['x'] - width/2, washmachine1['y'], width, label='drum washing machine',color='blue')  
plt.bar(washmachine2['x'] + width/2, washmachine2['y'], width, label='pulsator washing machine',color='red')  
plt.tight_layout()
plt.legend()

output_folder_bar = '输出分类\柱状图'
plt.savefig(os.path.join(output_folder_bar, 'washing machine model'))
plt.show()
# %%
current_time = datetime.now()
old_name = '输出分类'
new_name = "输出分类" + current_time.strftime("%Y-%m-%d-%H-%M-%S")
os.rename(old_name, new_name)
# %%
