import pandas as pd
import csv
from sklearn.ensemble import RandomForestClassifier

encoding_declaration = ['# -*- coding: utf-8 -*-\n']

file_path = "Daily Plan/weekend dailyplan.csv"

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

predict_data = pd.read_csv('Daily Plan/weekend dailyplan.csv')

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

predict_data['bathwinter'] = predict_data['bathwinter'].apply(update_bath_time)
predict_data['bathspring'] = predict_data['bathspring'].apply(update_bath_time)
predict_data['bathsummer'] = predict_data['bathsummer'].apply(update_bath_time)
predict_data['bathsum'] = predict_data['bathwinter'] + predict_data['bathspring'] + predict_data['bathsummer']

# predict first-bath
name1_data = pd.read_excel('Daily Plan/weekend-predict-firstbath.xlsx')
features1 = name1_data[['gender', 'age', 'permonth_income', 'education', 'status','family_member', 'minor', 'retired','hhd_income']]
second_level_labels1 = name1_data[['firstbath-happen']]
rf_second_level1 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_second_level1.fit(features1, second_level_labels1.values.ravel())
new_data1 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status','family_member', 'minor', 'retired','hhd_income']]
Y1 = rf_second_level1.predict(new_data1)
predict_data['firstbathhappen1'] = Y1
predict_data['firstbathperiod1'] = predict_data['bathsum'] / 3

# predict second-bath
name2_data = pd.read_excel('Daily Plan/weekend-predict-secondbath.xlsx')
features2 = name2_data[['gender', 'age', 'permonth_income', 'education', 'status','family_member', 'minor', 'retired','hhd_income']]
second_level_labels2 = name2_data[['secondbath-happen']]
rf_second_level2 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_second_level2.fit(features2, second_level_labels2.values.ravel())
new_data2 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status','family_member', 'minor', 'retired','hhd_income']]
Y2 = rf_second_level2.predict(new_data2)
predict_data['secondbathhappen1'] = Y2
predict_data['secondbathperiod1'] = predict_data['bathsum'] / 3

# Predict breakfast happen
name3_data = pd.read_excel('Daily Plan/weekend-predict-breakfast.xlsx')
features3 = name3_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
breakfast_happen_labels = name3_data['breakfast-happen']
rf_breakfast_happen = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_breakfast_happen.fit(features3, breakfast_happen_labels.values.ravel())
new_data3 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
breakfast_happen_prediction = rf_breakfast_happen.predict(new_data3)
predict_data['breakfasthappen1'] = breakfast_happen_prediction
# Predict breakfast period
breakfast_period_labels = name3_data['breakfast-period']
rf_breakfast_period = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_breakfast_period.fit(features3, breakfast_period_labels.values.ravel())
breakfast_period_prediction = rf_breakfast_period.predict(new_data3)
predict_data['breakfastperiod1'] = breakfast_period_prediction

# Predict lunch happen
name4_data = pd.read_excel('Daily Plan/weekend-predict-lunch.xlsx')
features4 = name4_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
lunch_happen_labels = name4_data['lunch-happen']
rf_lunch_happen = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_lunch_happen.fit(features4, lunch_happen_labels.values.ravel())
new_data4 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
lunch_happen_prediction = rf_lunch_happen.predict(new_data4)
predict_data['lunchhappen1'] = lunch_happen_prediction
# Predict lunch period
lunch_period_labels = name4_data['lunch-period']
rf_lunch_period = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_lunch_period.fit(features4, lunch_period_labels.values.ravel())
lunch_period_prediction = rf_lunch_period.predict(new_data4)
predict_data['lunchperiod1'] = lunch_period_prediction

# Predict dinner happen
name5_data = pd.read_excel('Daily Plan/weekend-predict-dinner.xlsx')
features5 = name5_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
dinner_happen_labels = name5_data['dinner-happen']
rf_dinner_happen = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_dinner_happen.fit(features5, dinner_happen_labels.values.ravel())
new_data5 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
dinner_happen_prediction = rf_dinner_happen.predict(new_data5)
predict_data['dinnerhappen1'] = dinner_happen_prediction
# Predict dinner period
dinner_period_labels = name5_data['dinner-period']
rf_dinner_period = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_dinner_period.fit(features5, dinner_period_labels.values.ravel())
dinner_period_prediction = rf_dinner_period.predict(new_data5)
predict_data['dinnerperiod1'] = dinner_period_prediction

# Predict clean happen
name6_data = pd.read_excel('Daily Plan/weekend-predict-clean.xlsx')
features6 = name6_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
clean_happen_labels = name6_data['clean-happen']
rf_clean_happen = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_clean_happen.fit(features6, clean_happen_labels.values.ravel())
new_data6 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
clean_happen_prediction = rf_clean_happen.predict(new_data6)
predict_data['cleanhappen1'] = clean_happen_prediction
# Predict clean period
clean_period_labels = name6_data['clean-period']
rf_clean_period = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_clean_period.fit(features6, clean_period_labels.values.ravel())
clean_period_prediction = rf_clean_period.predict(new_data6)
predict_data['cleanperiod1'] = clean_period_prediction

# Predict washclothes happen
name7_data = pd.read_excel('Daily Plan/weekend-predict-washclothes.xlsx')
features7 = name7_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
washclothes_happen_labels = name7_data['washclothes-happen']
rf_washclothes_happen = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_washclothes_happen.fit(features7, washclothes_happen_labels.values.ravel())
new_data7 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
washclothes_happen_prediction = rf_washclothes_happen.predict(new_data7)
predict_data['washclotheshappen1'] = washclothes_happen_prediction
# Predict washclothes period
washclothes_period_labels = name7_data['washclothes-period']
rf_washclothes_period = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_washclothes_period.fit(features7, washclothes_period_labels.values.ravel())
washclothes_period_prediction = rf_washclothes_period.predict(new_data7)
predict_data['washclothesperiod1'] = washclothes_period_prediction

# Predict footbath happen
name8_data = pd.read_excel('Daily Plan/weekend-predict-footbath.xlsx')
features8 = name8_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
footbath_happen_labels = name8_data['footbath-happen']
rf_footbath_happen = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_footbath_happen.fit(features8, footbath_happen_labels.values.ravel())
new_data8 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
footbath_happen_prediction = rf_footbath_happen.predict(new_data8)
predict_data['footbathhappen1'] = footbath_happen_prediction
# Predict footbath period
footbath_period_labels = name8_data['footbath-period']
rf_footbath_period = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_footbath_period.fit(features8, footbath_period_labels.values.ravel())
footbath_period_prediction = rf_footbath_period.predict(new_data8)
predict_data['footbathperiod1'] = footbath_period_prediction

# data to csv
predict_data.to_csv('Daily Plan/weekend dailyplan.csv', index=False)