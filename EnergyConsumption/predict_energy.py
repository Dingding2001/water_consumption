import pandas as pd
import csv
import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier

encoding_declaration = ['# -*- coding: utf-8 -*-\n']

file_path = "EnergyConsumption/household electricity.csv"


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

predict_data = pd.read_csv('EnergyConsumption/household electricity.csv')

# predict air
name1_data = pd.read_csv('EnergyConsumption/air.csv')
features1 = name1_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership']]
second_level_labels_1 = name1_data[['Num_cooling_AC']]
rf_second_level_1 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_second_level_1.fit(features1, second_level_labels_1.values.ravel())
new_data_1 = predict_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership']]
Num_cooling_AC = rf_second_level_1.predict(new_data_1)
predict_data['Num_cooling_AC'] = Num_cooling_AC

# predict month-cool
name2_data = pd.read_csv('EnergyConsumption/month_cool.csv')
features2 = name1_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Num_cooling_AC']]
second_level_labels_2 = name2_data[['Num_month_cooling']]
rf_second_level_2 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_second_level_2.fit(features2, second_level_labels_2.values.ravel())
new_data_2 = predict_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Num_cooling_AC']]
Num_month_cooling = rf_second_level_2.predict(new_data_2)
predict_data['Num_month_cooling'] = Num_month_cooling

# predict weekday-hour
name3_data = pd.read_csv('EnergyConsumption/hr_weekday.csv')
features_3 = name3_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Num_cooling_AC', 'Num_month_cooling']]
second_level_labels_3 = name3_data[['Cool_hr_weekday']]
rf_second_level_3 = RandomForestRegressor(n_estimators=trees, random_state=seeds)
rf_second_level_3.fit(features_3, second_level_labels_3.values.ravel())
new_data_3 = predict_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Num_cooling_AC', 'Num_month_cooling']]
Cool_hr_weekday = rf_second_level_3.predict(new_data_3)
predict_data['Cool_hr_weekday'] = Cool_hr_weekday

# predict weekend-hour
name4_data = pd.read_csv('EnergyConsumption/hr_weekend.csv')
features_4 = name4_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Num_cooling_AC', 'Num_month_cooling', 'Cool_hr_weekday']]
second_level_labels_4 = name4_data[['Cool_hr_weekend']]
rf_second_level_4 = RandomForestRegressor(n_estimators=trees, random_state=seeds)
rf_second_level_4.fit(features_4, second_level_labels_4.values.ravel())
new_data_4 = predict_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Num_cooling_AC', 'Num_month_cooling', 'Cool_hr_weekday']]
Cool_hr_weekend = rf_second_level_4.predict(new_data_4)
predict_data['Cool_hr_weekend'] = Cool_hr_weekend

# predict daytime-temp-air
name5_data = pd.read_csv('EnergyConsumption/daytime-temp-air.csv')
features_5 = name5_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Num_cooling_AC', 'Num_month_cooling', 'Cool_hr_weekday', 'Cool_hr_weekend']]
second_level_labels_5 = name5_data[['Temp_summer_day']]
rf_second_level_5 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_second_level_5.fit(features_5, second_level_labels_5.values.ravel())
new_data_5 = predict_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Num_cooling_AC', 'Num_month_cooling', 'Cool_hr_weekday', 'Cool_hr_weekend']]
Temp_summer_day = rf_second_level_5.predict(new_data_5)
predict_data['Temp_summer_day'] = Temp_summer_day

# predict night-temp-air
name6_data = pd.read_csv('EnergyConsumption/night-temp-air.csv')
features_6 = name6_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Num_cooling_AC', 'Num_month_cooling', 'Cool_hr_weekday', 'Cool_hr_weekend', 'Temp_summer_day']]
second_level_labels_6 = name6_data[['Temp_summer_night']]
rf_second_level_6 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_second_level_6.fit(features_6, second_level_labels_6.values.ravel())
new_data_6 = predict_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Num_cooling_AC', 'Num_month_cooling', 'Cool_hr_weekday', 'Cool_hr_weekend', 'Temp_summer_day']]
Temp_summer_night = rf_second_level_6.predict(new_data_6)
predict_data['Temp_summer_night'] = Temp_summer_night

# predict fre-cook
name7_data = pd.read_csv('EnergyConsumption/fre-cooking.csv')
features_7 = name7_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership']]
second_level_labels_7 = name7_data[['Cooking_fre']]
rf_second_level_7 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_second_level_7.fit(features_7, second_level_labels_7.values.ravel())
new_data_7 = predict_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership']]
Cooking_fre = rf_second_level_7.predict(new_data_7)
predict_data['Cooking_fre'] = Cooking_fre

# predict bread
name8_data = pd.read_csv('EnergyConsumption/bread.csv')
features_8 = name8_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Cooking_fre']]
second_level_labels_8 = name8_data[['Bread_machine']]
rf_second_level_8 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_second_level_8.fit(features_8, second_level_labels_8.values.ravel())
new_data_8 = predict_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Cooking_fre']]
Bread_machine = rf_second_level_8.predict(new_data_8)
predict_data['Bread_machine'] = Bread_machine

# predict induction
name9_data = pd.read_csv('EnergyConsumption/induction.csv')
features_9 = name9_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Cooking_fre']]
second_level_labels_9 = name9_data[['Induction_cooker']]
rf_second_level_9 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_second_level_9.fit(features_9, second_level_labels_9.values.ravel())
new_data_9 = predict_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Cooking_fre']]
Induction_cooker = rf_second_level_9.predict(new_data_9)
predict_data['Induction_cooker'] = Induction_cooker

# predict rice
name10_data = pd.read_csv('EnergyConsumption/rice.csv')
features_10 = name10_data[['gender', 'age', 'income', 'education', 'Status','Num_family', 'Num_child', 'Num_old','Household_income', 'House_ownership', 'Cooking_fre']]
second_level_labels_10 = name10_data[['rice_cooker']]
rf_second_level_10 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_second_level_10.fit(features_10, second_level_labels_10.values.ravel())
new_data_10 = predict_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Cooking_fre']]
rice_cooker = rf_second_level_10.predict(new_data_10)
predict_data['rice_cooker'] = rice_cooker

# predict pressure
name11_data = pd.read_csv('EnergyConsumption/pressure.csv')
features_11 = name11_data[['gender', 'age', 'income', 'education', 'Status','Num_family', 'Num_child', 'Num_old','Household_income', 'House_ownership', 'Cooking_fre']]
second_level_labels_11 = name11_data[['Pressure_cooker']]
rf_second_level_11 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_second_level_11.fit(features_11, second_level_labels_11.values.ravel())
new_data_11 = predict_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Cooking_fre']]
Pressure_cooker = rf_second_level_11.predict(new_data_11)
predict_data['Pressure_cooker'] = Pressure_cooker

# predict baking
name12_data = pd.read_csv('EnergyConsumption/baking.csv')
features_12 = name12_data[['gender', 'age', 'income', 'education', 'Status','Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Cooking_fre']]
second_level_labels_12 = name12_data[['Electric_baking_pan']]
rf_second_level_12 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_second_level_12.fit(features_12, second_level_labels_12.values.ravel())
new_data_12 = predict_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Cooking_fre']]
Electric_baking_pan = rf_second_level_12.predict(new_data_12)
predict_data['Electric_baking_pan'] = Electric_baking_pan

# predict pot
name13_data = pd.read_csv('EnergyConsumption/pot.csv')
features_13 = name13_data[['gender', 'age', 'income', 'education', 'Status','Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Cooking_fre']]
second_level_labels_13 = name13_data[['Pot']]
rf_second_level_13 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_second_level_13.fit(features_13, second_level_labels_13.values.ravel())
new_data_13 = predict_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Cooking_fre']]
Pot = rf_second_level_13.predict(new_data_13)
predict_data['Pot'] = Pot

# predict milk
name14_data = pd.read_csv('EnergyConsumption/milk.csv')
features_14 = name14_data[['gender', 'age', 'income', 'education', 'Status','Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Cooking_fre']]
second_level_labels_14 = name14_data[['Soymilk']]
rf_second_level_14 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_second_level_14.fit(features_14, second_level_labels_14.values.ravel())
new_data_14 = predict_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Cooking_fre']]
Soymilk = rf_second_level_14.predict(new_data_14)
predict_data['Soymilk'] = Soymilk

# predict LED
name15_data = pd.read_csv('EnergyConsumption/LED.csv')
features_15 = name15_data[['gender', 'age', 'income', 'education', 'Status','Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership']]
second_level_labels_15 = name15_data[['LED']]
rf_second_level_15 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_second_level_15.fit(features_15, second_level_labels_15.values.ravel())
new_data_15 = predict_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership']]
LED = rf_second_level_15.predict(new_data_15)
predict_data['LED'] = LED


#predict microveoven
name16_data = pd.read_csv('EnergyConsumption/microwave.csv')
features_16 = name16_data[['gender', 'age', 'income', 'education', 'Status','Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Cooking_fre']]
second_level_labels_16 = name16_data[['Microwave_oven']]
rf_second_level_16 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_second_level_16.fit(features_16, second_level_labels_16.values.ravel())
new_data_16 = predict_data[['gender', 'age', 'income', 'education', 'Status', 'Num_family', 'Num_child', 'Num_old', 'Household_income', 'House_ownership', 'Cooking_fre']]
microwave = rf_second_level_16.predict(new_data_16)
predict_data['microwave'] = microwave

# data to csv
predict_data.to_csv('EnergyConsumption/household electricity.csv', index=False)