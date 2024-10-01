import pandas as pd
import csv
import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier

encoding_declaration = ['# -*- coding: utf-8 -*-\n']

file_path = "Water Energy Consumption/people water appliances.csv"

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

predict_data = pd.read_csv('Water Energy Consumption/people water appliances.csv')

# predict bathing appliances
name1_data = pd.read_excel('Water Energy Consumption/bathing appliances.xlsx')
features1 = name1_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
new_data1 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
# Predict Electric Footbath
electric_footbath_labels = name1_data['Electric Footbath']
rf_electric_footbath = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_electric_footbath.fit(features1, electric_footbath_labels.values.ravel())
predict_data['ElectricFootbath'] = rf_electric_footbath.predict(new_data1)
# Predict Water heater model
water_heater_labels = name1_data['Water heater model']
rf_water_heater = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_water_heater.fit(features1, water_heater_labels.values.ravel())
predict_data['Waterheater'] = rf_water_heater.predict(new_data1)
# Predict showerhead
showerhead_labels = name1_data['showerhead']
rf_showerhead = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_showerhead.fit(features1, showerhead_labels.values.ravel())
predict_data['showerhead'] = rf_showerhead.predict(new_data1)
# Predict thermostatic function
thermostatic_labels = name1_data['thermostatic function']
rf_thermostatic = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_thermostatic.fit(features1, thermostatic_labels.values.ravel())
predict_data['thermostatic'] = rf_thermostatic.predict(new_data1)
# Predict Faucet type
faucet_labels = name1_data['Faucet type']
rf_faucet = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_faucet.fit(features1, faucet_labels.values.ravel())
predict_data['Faucet'] = rf_faucet.predict(new_data1)

# predict cleaning appliances
name2_data = pd.read_excel('Water Energy Consumption/cleaning appliances.xlsx')
features2 = name2_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
new_data2 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
# Predict Dishwasher
dishwasher_labels = name2_data['Dishwasher']
rf_dishwasher = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_dishwasher.fit(features2, dishwasher_labels.values.ravel())
predict_data['Dishwasher'] = rf_dishwasher.predict(new_data2)
# Predict sterilizer
sterilizer_labels = name2_data['sterilizer']
rf_sterilizer = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_sterilizer.fit(features2, sterilizer_labels.values.ravel())
predict_data['sterilizer'] = rf_sterilizer.predict(new_data2)
# Predict sweeping robot
sweeping_robot_labels = name2_data['sweeping robot']
rf_sweeping_robot = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_sweeping_robot.fit(features2, sweeping_robot_labels.values.ravel())
predict_data['sweepingrobot'] = rf_sweeping_robot.predict(new_data2)
# Predict Electric mop
electric_mop_labels = name2_data['Electric mop']
rf_electric_mop = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_electric_mop.fit(features2, electric_mop_labels.values.ravel())
predict_data['Electricmop'] = rf_electric_mop.predict(new_data2)
# Predict Intelligent Toilet
intelligent_toilet_labels = name2_data['Intelligent Toilet']
rf_intelligent_toilet = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_intelligent_toilet.fit(features2, intelligent_toilet_labels.values.ravel())
predict_data['IntelligentToilet'] = rf_intelligent_toilet.predict(new_data2)
# Predict Washing machine model
washing_machine_labels = name2_data['Washing machine model']
rf_washing_machine = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_washing_machine.fit(features2, washing_machine_labels.values.ravel())
predict_data['Washingmachine'] = rf_washing_machine.predict(new_data2)
# Predict Drying or sterilizing
drying_sterilizing_labels = name2_data['Dryingorsterilizing']
rf_drying_sterilizing = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_drying_sterilizing.fit(features2, drying_sterilizing_labels.values.ravel())
predict_data['Dryorsterilize'] = rf_drying_sterilizing.predict(new_data2)

# predict cooking appliances
name3_data = pd.read_excel('Water Energy Consumption/cooking appliances.xlsx')
features3 = name3_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
new_data3 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
# Predict pressure pot
pressure_pot_labels = name3_data['pressure pot']
rf_pressure_pot = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_pressure_pot.fit(features3, pressure_pot_labels.values.ravel())
predict_data['pressure'] = rf_pressure_pot.predict(new_data3)
# Predict microwave oven
microwave_oven_labels = name3_data['microwave oven']
rf_microwave_oven = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_microwave_oven.fit(features3, microwave_oven_labels.values.ravel())
predict_data['microwaveoven'] = rf_microwave_oven.predict(new_data3)
# Predict Electric crockpot or soymilk maker or pie pan
soymilk_labels = name3_data['Electric crockpot orsoymilk maker orpie pan']
rf_soymilk = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_soymilk.fit(features3, soymilk_labels.values.ravel())
predict_data['soymilk'] = rf_soymilk.predict(new_data3)
# Predict Electric oven or toaster or coffee maker
eleoven_labels = name3_data['Electric oven ortoaster orcoffee maker']
rf_eleoven = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_eleoven.fit(features3, eleoven_labels.values.ravel())
predict_data['Eleoven'] = rf_eleoven.predict(new_data3)
# Predict Terminal water purifier
terminal_water_labels = name3_data['Terminal water purifier']
rf_terminal_water = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_terminal_water.fit(features3, terminal_water_labels.values.ravel())
predict_data['Terminalwater'] = rf_terminal_water.predict(new_data3)
# Predict Kitchen water heater
kitchen_water_labels = name3_data['Kitchen water heater']
rf_kitchen_water = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_kitchen_water.fit(features3, kitchen_water_labels.values.ravel())
predict_data['Kitchenwaterheat'] = rf_kitchen_water.predict(new_data3)

# predict hvac appliances
name4_data = pd.read_excel('Water Energy Consumption/HVAC appliances.xlsx')
features4 = name4_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
new_data4 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
radiator_bag_labels = name4_data['radiator bag']
rf_radiator_bag = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_radiator_bag.fit(features4, radiator_bag_labels.values.ravel())
predict_data['radiatorbag'] = rf_radiator_bag.predict(new_data4)

# data to csv
predict_data.to_csv('Water Energy Consumption/people water appliances.csv', index=False)