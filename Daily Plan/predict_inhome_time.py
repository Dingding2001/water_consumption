import pandas as pd
import csv
import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputClassifier

encoding_declaration = ['# -*- coding: utf-8 -*-\n']

file_path = "Daily Plan/people in-home time.csv"

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

seeds = 1
trees = 100

predict_data = pd.read_csv('Daily Plan/people in-home time.csv')

# predict in-home time
# 读取训练数据
# 读取训练数据
name_data = pd.read_csv('Daily Plan/SZ inhome time.csv')

# 选择特征和标签
features = name_data[['gender', 'income', 'age-group', 'status', 'livelon', 'livelat', 'wslong', 'wslat', 'current-ws-dis', 'weekday-shopping', 'weekday-leisure', 'weekend-shopping', 'distance-max']]
weekday_deptime_labels = name_data['weekday-deptime']
weekday_endtime_labels = name_data['weekday-endtime']
weekend_deptime_labels = name_data['weekend-deptime']
weekend_endtime_labels = name_data['weekend-endtime']


# 创建四个独立的随机森林回归器
rf_weekday_deptime = RandomForestRegressor(n_estimators=trees, random_state=seeds)
rf_weekday_endtime = RandomForestRegressor(n_estimators=trees, random_state=seeds)
rf_weekend_deptime = RandomForestRegressor(n_estimators=trees, random_state=seeds)
rf_weekend_endtime = RandomForestRegressor(n_estimators=trees, random_state=seeds)

# 拟合模型
rf_weekday_deptime.fit(features, weekday_deptime_labels.values.ravel())
rf_weekday_endtime.fit(features, weekday_endtime_labels.values.ravel())
rf_weekend_deptime.fit(features, weekend_deptime_labels.values.ravel())
rf_weekend_endtime.fit(features, weekend_endtime_labels.values.ravel())


# 选择新数据
new_data = predict_data[['gender', 'income', 'age-group', 'status', 'livelon', 'livelat', 'wslong', 'wslat', 'current-ws-dis', 'weekday-shopping', 'weekday-leisure', 'weekend-shopping', 'distance-max']]

# 进行预测
predict_data['weekdaydeptime'] = rf_weekday_deptime.predict(new_data)
predict_data['weekdayendtime'] = rf_weekday_endtime.predict(new_data)
predict_data['weekenddeptime'] = rf_weekend_deptime.predict(new_data)
predict_data['weekendendtime'] = rf_weekend_endtime.predict(new_data)


# 将预测结果保存到CSV文件
predict_data.to_csv('Daily Plan/people in-home time.csv', index=False)