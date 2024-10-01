import pandas as pd
import csv
import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier

encoding_declaration = ['# -*- coding: utf-8 -*-\n']

file_path = "Daily Plan/activities.csv"

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

predict_data = pd.read_csv('Daily Plan/activities.csv')

# predict weekday activities
name1_data = pd.read_excel('Daily Plan/weekday-activities.xlsx')
features1 = name1_data[['gender', 'age', 'permonth_income', 'education', 'status','family_member', 'minor', 'retired', 'hhd_income']]

activities1 = ['firstbath', 'secondbath', 'breakfast', 'lunch', 'dinner', 'washclothes', 'clean', 'footbath']
rf_activities1 = {}

for activity in activities1:
    labels1 = name1_data[activity]
    rf_activity1 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
    rf_activity1.fit(features1, labels1)
    rf_activities1[activity] = rf_activity1

new_data1 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]

for activity in activities1:
    rf_activity1 = rf_activities1[activity]
    predict_data[activity + '_weekday'] = rf_activity1.predict(new_data1)

# predict weekend activities
name2_data = pd.read_excel('Daily Plan/weekend-activities.xlsx')
features2 = name2_data[['gender', 'age', 'permonth_income', 'education', 'status','family_member', 'minor', 'retired','hhd_income']]

activities2 = ['firstbath', 'secondbath', 'breakfast', 'lunch', 'dinner', 'washclothes', 'clean', 'footbath']
rf_activities2 = {}

for activity in activities2:
    labels2 = name2_data[activity]
    rf_activity2 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
    rf_activity2.fit(features2, labels2)
    rf_activities2[activity] = rf_activity2

new_data2 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]

for activity in activities2:
    rf_activity2 = rf_activities2[activity]
    predict_data[activity + '_weekend'] = rf_activity2.predict(new_data2)

# data to csv
predict_data.to_csv('Daily Plan/activities.csv', index=False)