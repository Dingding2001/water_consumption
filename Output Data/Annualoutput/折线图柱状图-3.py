#%%
import csv
import re
import pandas as pd
import os
import numpy as np
import math
from datetime import datetime
file_path = "SelfSim-water-dailyplan Bathing Appliances.csv"

#start_row表示第几行开始是数据
start_row = 29

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
Electric_Footbath_data = pd.read_csv(os.path.join(folder_path, 'electric footbath.csv'))

# 绘制折线图
plt.plot(Electric_Footbath_data['x'], Electric_Footbath_data['y'], label='Electric Footbath',marker='o', color='DeepSkyBlue',linewidth=2,linestyle='dotted')  

# 设置图的标签、标题等
plt.xlabel('Year')
plt.ylabel('Number')
plt.xticks(Electric_Footbath_data['x'], Electric_Footbath_data['x'].tolist())  
y_interval = 10  # 设置你希望的y轴间隔

# 计算y轴的最小和最大值
y_min = min(Electric_Footbath_data['y'])
y_max = max(Electric_Footbath_data['y'])
num_ticks = 5  # 想有几个
y_interval = (y_max - y_min) / num_ticks
y_min = int(min(Electric_Footbath_data['y']- y_interval/2))
y_max = int(max(Electric_Footbath_data['y']+ y_interval))
# 设置y轴刻度间隔和最小最大值
ax = plt.gca()
ax.yaxis.set_major_locator(MultipleLocator(base=y_interval))
ax.set_ylim([y_min, y_max])
plt.tight_layout()
plt.legend(loc='upper center', fontsize=8, bbox_to_anchor=(0.5, -0.2), ncol=2)
plt.tight_layout(rect=(0, 0, 1, 0.9))
plt.ticklabel_format(style='plain', axis='y')
plt.xlim(min(Electric_Footbath_data['x']) - 0.25, max(Electric_Footbath_data['x']) + 0.25)
plt.grid()
plt.savefig(os.path.join(output_folder_line, 'Electric Footbath'))
plt.show()
#柱状图
# 设置图的标签、标题等
plt.xlabel('Year')
plt.ylabel('Number')
plt.xticks(Electric_Footbath_data['x'], Electric_Footbath_data['x'].tolist())   
# 绘制多年柱状图
width = 0.35  # 柱状图的宽度
plt.bar(Electric_Footbath_data['x'] - width/2, Electric_Footbath_data['y'], width, label='Electric Footbath',color='DeepSkyBlue')  
plt.tight_layout()
plt.legend()
output_folder_bar = '输出分类\柱状图'
plt.savefig(os.path.join(output_folder_bar, 'Electric Footbath'))
plt.show()
# %%
heater1_data = pd.read_csv(os.path.join(folder_path, 'water heater-1.csv'))
heater2_data = pd.read_csv(os.path.join(folder_path, 'water heater-2.csv'))
heater3_data = pd.read_csv(os.path.join(folder_path, 'water heater-3.csv'))
heater4_data = pd.read_csv(os.path.join(folder_path, 'water heater-4.csv'))


# 绘制折线图
plt.plot(heater1_data['x'], heater1_data['y'], label='Instantaneous gas water heaters', marker='o', color='green', linewidth=2, linestyle='dotted')
plt.plot(heater2_data['x'], heater2_data['y'], label='Instantaneous electric water heater', marker='o', color='blue', linewidth=2, linestyle='dotted')
plt.plot(heater3_data['x'], heater3_data['y'], label='Storage water heater', marker='o', color='orange', linewidth=2, linestyle='dotted')
plt.plot(heater4_data['x'], heater4_data['y'], label='Solar water heater', marker='o', color='red', linewidth=2, linestyle='dotted')

# 设置图的标签、标题等
plt.xlabel('Year')
plt.ylabel('Number')
plt.xticks(heater1_data['x'], heater1_data['x'].tolist())
y_interval = 2000  # 设置你希望的y轴间隔

# 计算y轴的最小和最大值
y_min = min(heater1_data['y'].min(), heater2_data['y'].min(), heater3_data['y'].min(), heater4_data['y'].min()) - y_interval
y_max = max(heater1_data['y'].max(), heater2_data['y'].max(), heater3_data['y'].max(), heater4_data['y'].max()) + y_interval

# 设置y轴刻度间隔和最小最大值
ax = plt.gca()
ax.yaxis.set_major_locator(MultipleLocator(base=y_interval))
ax.set_ylim([y_min, y_max])
plt.tight_layout()
plt.legend(loc='upper center', fontsize=8, bbox_to_anchor=(0.5, -0.2), ncol=4)
plt.tight_layout(rect=(0, 0, 1, 0.9))
plt.ticklabel_format(style='plain', axis='y')
plt.xlim(min(heater1_data['x'].min(), heater2_data['x'].min(), heater3_data['x'].min(), heater4_data['x'].min()) - 0.5,
         max(heater1_data['x'].max(), heater2_data['x'].max(), heater3_data['x'].max(), heater4_data['x'].max()) + 0.5)
plt.grid()
plt.savefig(os.path.join(output_folder_line, 'Water Heater Model'))
plt.show()

# 柱状图
# 设置图的标签、标题等
plt.xlabel('Year')
plt.ylabel('Number')
plt.xticks(heater1_data['x'], heater1_data['x'].tolist())

# 绘制多年柱状图
width = 0.2  # 柱状图的宽度
plt.bar(heater1_data['x'] - width * 1.5, heater1_data['y'], width, label='Instantaneous gas water heaters', color='green')
plt.bar(heater2_data['x'] - width / 2, heater2_data['y'], width, label='Instantaneous electric water heater', color='blue')
plt.bar(heater3_data['x'] + width / 2, heater3_data['y'], width, label='Storage water heater', color='orange')
plt.bar(heater4_data['x'] + width * 1.5, heater4_data['y'], width, label='Solar water heater', color='red')
plt.tight_layout()
plt.legend()

output_folder_bar = '输出分类\柱状图'
plt.savefig(os.path.join(output_folder_bar, 'Water Heater Model'))
plt.show()
# %%
water_heater_data = pd.read_csv(os.path.join(folder_path, 'water heater.csv'))

# 绘制折线图
plt.plot(water_heater_data['x'], water_heater_data['y'], label='water heater',marker='o', color='DarkOrange',linewidth=2,linestyle='dotted')  

# 设置图的标签、标题等
plt.xlabel('Year')
plt.ylabel('Number')
plt.xticks(water_heater_data['x'], water_heater_data['x'].tolist())  
y_interval = 2000  # 设置你希望的y轴间隔

# 计算y轴的最小和最大值
y_min = min(water_heater_data['y'])
y_max = max(water_heater_data['y'])
num_ticks = 5  # 想有几个
y_interval = (y_max - y_min) / num_ticks
y_min = int(min(water_heater_data['y']- y_interval/2))
y_max = int(max(water_heater_data['y']+ y_interval/2))
# 设置y轴刻度间隔和最小最大值
ax = plt.gca()
ax.yaxis.set_major_locator(MultipleLocator(base=y_interval))
ax.set_ylim([y_min, y_max])
plt.tight_layout()
plt.legend(loc='upper center', fontsize=8, bbox_to_anchor=(0.5, -0.2), ncol=2)
plt.tight_layout(rect=(0, 0, 1, 0.9))
plt.ticklabel_format(style='plain', axis='y')
plt.xlim(min(water_heater_data['x']) - 0.25, max(water_heater_data['x']) + 0.25)
plt.grid()
plt.savefig(os.path.join(output_folder_line, 'Number of water heaters'))
plt.show()
#柱状图
# 设置图的标签、标题等
plt.xlabel('Year')
plt.ylabel('Number')
plt.xticks(water_heater_data['x'], water_heater_data['x'].tolist())   
# 绘制多年柱状图
width = 0.35  # 柱状图的宽度
plt.bar(water_heater_data['x'] - width/2, water_heater_data['y'], width, label='water heater',color='DarkOrange')  
plt.tight_layout()
plt.legend()
output_folder_bar = '输出分类\柱状图'
plt.savefig(os.path.join(output_folder_bar, 'Number of water heaters'))
plt.show()
# %%
shower1_data = pd.read_csv(os.path.join(folder_path, 'shower head-1.csv'))
shower2_data = pd.read_csv(os.path.join(folder_path, 'shower head-2.csv'))
shower3_data = pd.read_csv(os.path.join(folder_path, 'shower head-3.csv'))

# 绘制折线图
plt.plot(shower1_data['x'], shower1_data['y'], label='Hand Shower', marker='o', color='blue', linewidth=2, linestyle='dotted')  
plt.plot(shower2_data['x'], shower2_data['y'], label='Overhead Shower', marker='o', color='red', linewidth=2, linestyle='dotted') 
plt.plot(shower3_data['x'], shower3_data['y'], label='Side-spray Shower', marker='o', color='green', linewidth=2, linestyle='dotted') 

# 设置图的标签、标题等
plt.xlabel('Year')
plt.ylabel('Number')
plt.xticks(shower1_data['x'], shower1_data['x'].tolist())  
y_interval = 1000  # 设置你希望的y轴间隔

# 计算y轴的最小和最大值
y_min = min(shower1_data['y'].min(), shower2_data['y'].min(), shower3_data['y'].min()) - y_interval
y_max = max(shower1_data['y'].max(), shower2_data['y'].max(), shower3_data['y'].max()) + y_interval  

# 设置y轴刻度间隔和最小最大值
ax = plt.gca()
ax.yaxis.set_major_locator(MultipleLocator(base=y_interval))
ax.set_ylim([y_min, y_max])
plt.tight_layout()
plt.legend(loc='upper center', fontsize=8, bbox_to_anchor=(0.5, -0.2), ncol=4)
plt.tight_layout(rect=(0, 0, 1, 0.9))
plt.ticklabel_format(style='plain', axis='y')
plt.xlim(min(shower1_data['x'].min(), shower2_data['x'].min(), shower3_data['x'].min()) - 0.25, max(shower1_data['x'].max(), shower2_data['x'].max(), shower3_data['x'].max()) + 0.25)
plt.grid()
plt.savefig(os.path.join(output_folder_line, 'Shower Head Model'))
plt.show()

# 柱状图
# 设置图的标签、标题等
plt.xlabel('Year')
plt.ylabel('Number')
plt.xticks(shower1_data['x'], shower1_data['x'].tolist())   

# 绘制多年柱状图
width = 0.2  # 柱状图的宽度
plt.bar(shower1_data['x'] - 1.5*width, shower1_data['y'], width, label='Hand Shower', color='blue')  
plt.bar(shower2_data['x'] - 0.5*width, shower2_data['y'], width, label='Overhead Shower', color='red')  
plt.bar(shower3_data['x'] + 0.5*width, shower3_data['y'], width, label='Side-spray Shower', color='green')  

plt.tight_layout()
plt.legend()

output_folder_bar = '输出分类\柱状图'
plt.savefig(os.path.join(output_folder_bar, 'Shower Head Model'))
plt.show()
# %%
thermostatic = pd.read_csv(os.path.join(folder_path, 'thermostatic.csv'))

# 绘制折线图
plt.plot(thermostatic['x'], thermostatic['y'], label='thermostatic',marker='o', color='GoldEnrod',linewidth=2,linestyle='dotted')  

# 设置图的标签、标题等
plt.xlabel('Year')
plt.ylabel('number')
plt.xticks(thermostatic['x'], thermostatic['x'].tolist())  
y_interval = 1000  # 设置你希望的y轴间隔

# 计算y轴的最小和最大值
y_min = min(thermostatic['y'])
y_max = max(thermostatic['y'])
num_ticks = 5  # 想有几个
y_interval = (y_max - y_min) / num_ticks
y_min = int(min(thermostatic['y']- y_interval/2))
y_max = int(max(thermostatic['y']+ y_interval))
# 设置y轴刻度间隔和最小最大值
ax = plt.gca()
ax.yaxis.set_major_locator(MultipleLocator(base=y_interval))
ax.set_ylim([y_min, y_max])
plt.tight_layout()
plt.legend(loc='upper center', fontsize=8, bbox_to_anchor=(0.5, -0.2), ncol=2)
plt.tight_layout(rect=(0, 0, 1, 0.9))
plt.ticklabel_format(style='plain', axis='y')
plt.xlim(min(thermostatic['x']) - 0.25, max(thermostatic['x']) + 0.25)
plt.grid()
plt.savefig(os.path.join(output_folder_line, 'thermostatic'))
plt.show()
#柱状图
# 设置图的标签、标题等
plt.xlabel('Year')
plt.ylabel('number')
plt.xticks(thermostatic['x'], thermostatic['x'].tolist())   
# 绘制多年柱状图
width = 0.35  # 柱状图的宽度
plt.bar(thermostatic['x'] - width/2, thermostatic['y'], width, label='thermostatic',color='GoldEnrod')  
plt.tight_layout()
plt.legend()
output_folder_bar = '输出分类\柱状图'
plt.savefig(os.path.join(output_folder_bar, 'thermostatic'))
plt.show()

#%%
faucet1 = pd.read_csv(os.path.join(folder_path, 'faucet-1.csv'))
faucet2 = pd.read_csv(os.path.join(folder_path, 'faucet-2.csv'))
faucet3 = pd.read_csv(os.path.join(folder_path, 'faucet-3.csv'))

# 绘制折线图
plt.plot(faucet1['x'], faucet1['y'], label='General Faucet', marker='o', color='blue', linewidth=2, linestyle='dotted')
plt.plot(faucet2['x'], faucet2['y'], label='Water-saving Faucet', marker='o', color='green', linewidth=2, linestyle='dotted')
plt.plot(faucet3['x'], faucet3['y'], label='Sensor Faucet', marker='o', color='orange', linewidth=2, linestyle='dotted')

# 设置图的标签、标题等
plt.xlabel('Year')
plt.ylabel('Number')
plt.xticks(faucet1['x'], faucet1['x'].tolist())
y_interval = 2000  # 设置你希望的y轴间隔

# 计算y轴的最小和最大值
y_min = min(faucet1['y'].min(), faucet2['y'].min(), faucet3['y'].min()) - y_interval
y_max = max(faucet1['y'].max(), faucet2['y'].max(), faucet3['y'].max()) + y_interval

# 设置y轴刻度间隔和最小最大值
ax = plt.gca()
ax.yaxis.set_major_locator(MultipleLocator(base=y_interval))
ax.set_ylim([y_min, y_max])
plt.tight_layout()
plt.legend(loc='upper center', fontsize=8, bbox_to_anchor=(0.5, -0.2), ncol=2)
plt.tight_layout(rect=(0, 0, 1, 0.9))
plt.ticklabel_format(style='plain', axis='y')
plt.xlim(min(faucet1['x'].min(), faucet2['x'].min(), faucet3['x'].min()) - 0.25, max(faucet1['x'].max(), faucet2['x'].max(), faucet3['x'].max()) + 0.25)
plt.grid()
plt.savefig(os.path.join(output_folder_line, 'Faucet Model'))
plt.show()

# 柱状图
# 设置图的标签、标题等
plt.xlabel('Year')
plt.ylabel('Number')
plt.xticks(faucet1['x'], faucet1['x'].tolist())

# 绘制多年柱状图
width = 0.15  # 柱状图的宽度
plt.bar(faucet1['x'] - 2*width, faucet1['y'], width, label='General Faucet', color='blue')
plt.bar(faucet2['x'] - width, faucet2['y'], width, label='Water-saving Faucet', color='green')
plt.bar(faucet3['x'], faucet3['y'], width, label='Sensor Faucet', color='orange')
plt.tight_layout()
plt.legend()

output_folder_bar = '输出分类\柱状图'
plt.savefig(os.path.join(output_folder_bar, 'Faucet Model'))
plt.show()
# %%
current_time = datetime.now()
old_name = '输出分类'
new_name = "输出分类" + current_time.strftime("%Y-%m-%d-%H-%M-%S")
os.rename(old_name, new_name)
# %%
