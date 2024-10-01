import pandas as pd
import csv
import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier

encoding_declaration = ['# -*- coding: utf-8 -*-\n']

file_path = "Water Energy Consumption/people water behavior.csv"

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

predict_data = pd.read_csv('Water Energy Consumption/people water behavior.csv')

# predict bathing behavior
# step 1
name1_data = pd.read_excel('Water Energy Consumption/bathing behavior-1.xlsx')
features1 = name1_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income', 'Waterheatermodel', 'showerhead', 'thermostaticfunction', 'Faucettype']]
new_data1 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income', 'Waterheatermodel', 'showerhead', 'thermostaticfunction', 'Faucettype']]

rf_bathing1 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_bathing1.fit(features1, name1_data['Bathingstyle'].values.ravel())
predict_data['Bathingstyle'] = rf_bathing1.predict(new_data1)

rf_temperature1 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_temperature1.fit(features1, name1_data['Adjustingtemperature'].values.ravel())
predict_data['Adjustingtemperature'] = rf_temperature1.predict(new_data1)

rf_insulation1 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_insulation1.fit(features1, name1_data['Waterheaterinsulation'].values.ravel())
predict_data['Waterheaterinsulation'] = rf_insulation1.predict(new_data1)
# step 2
name2_data = pd.read_excel('Water Energy Consumption/bathing behavior-2.xlsx')
features2 = name2_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income', 'Bathingstyle', 'Adjustingtemperature', 'Waterheaterinsulation']]
second_level_labels2 = name2_data[['Bathingfrequencyinwinter', 'Bathingfrequencyinspring', 'Bathingfrequencyinsummer', 'Bathingtimeinwinter', 'Bathingtimeinspring', 'Bathingtimeinsummer', 'Frequencyoffootbathsinwinter', 'Frequencyoffootbathsinspring', 'Frequencyoffootbathsinsummer']]

rf_frequency_winter = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_frequency_spring = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_frequency_summer = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_time_winter = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_time_spring = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_time_summer = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_footbath_winter = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_footbath_spring = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_footbath_summer = RandomForestClassifier(n_estimators=trees, random_state=seeds)

rf_frequency_winter.fit(features2, second_level_labels2['Bathingfrequencyinwinter'].values.ravel())
rf_frequency_spring.fit(features2, second_level_labels2['Bathingfrequencyinspring'].values.ravel())
rf_frequency_summer.fit(features2, second_level_labels2['Bathingfrequencyinsummer'].values.ravel())
rf_time_winter.fit(features2, second_level_labels2['Bathingtimeinwinter'].values.ravel())
rf_time_spring.fit(features2, second_level_labels2['Bathingtimeinspring'].values.ravel())
rf_time_summer.fit(features2, second_level_labels2['Bathingtimeinsummer'].values.ravel())
rf_footbath_winter.fit(features2, second_level_labels2['Frequencyoffootbathsinwinter'].values.ravel())
rf_footbath_spring.fit(features2, second_level_labels2['Frequencyoffootbathsinspring'].values.ravel())
rf_footbath_summer.fit(features2, second_level_labels2['Frequencyoffootbathsinsummer'].values.ravel())

new_data2 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income', 'Bathingstyle', 'Adjustingtemperature', 'Waterheaterinsulation']]

predict_data['Bathfrewinter'] = rf_frequency_winter.predict(new_data2)
predict_data['Bathfrespring'] = rf_frequency_spring.predict(new_data2)
predict_data['Bathfresummer'] = rf_frequency_summer.predict(new_data2)
predict_data['Bathtimewinter'] = rf_time_winter.predict(new_data2)
predict_data['Bathtimespring'] = rf_time_spring.predict(new_data2)
predict_data['Bathtimesummer'] = rf_time_summer.predict(new_data2)
predict_data['footbathfrewinter'] = rf_footbath_winter.predict(new_data2)
predict_data['footbathfrespring'] = rf_footbath_spring.predict(new_data2)
predict_data['footbathfresummer'] = rf_footbath_summer.predict(new_data2)

# predict cooking behavior
# step 1
name3_data = pd.read_excel('Water Energy Consumption/cooking behavior-1.xlsx')
features3 = name3_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income', 'pressurepot', 'microwaveoven', 'Electriccrockpotorsoymilkmakerorpiepan', 'Electricovenortoasterorcoffeemaker', 'Terminalwaterpurifier', 'Kitchenwaterheater']]
second_level_labels3 = name3_data[['Frequencyofcookingonfire', 'FrequencyofSoup', 'CookingEnergy', 'TimeforGasStove']]

rf_cooking_fire = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_soup = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_cooking_energy = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_gas_stove_time = RandomForestClassifier(n_estimators=trees, random_state=seeds)

rf_cooking_fire.fit(features3, second_level_labels3['Frequencyofcookingonfire'].values.ravel())
rf_soup.fit(features3, second_level_labels3['FrequencyofSoup'].values.ravel())
rf_cooking_energy.fit(features3, second_level_labels3['CookingEnergy'].values.ravel())
rf_gas_stove_time.fit(features3, second_level_labels3['TimeforGasStove'].values.ravel())

new_data3 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income', 'pressurepot', 'microwaveoven', 'Electriccrockpotorsoymilkmakerorpiepan', 'Electricovenortoasterorcoffeemaker', 'Terminalwaterpurifier', 'Kitchenwaterheater']]

predict_data['Frequencyofcookingonfire'] = rf_cooking_fire.predict(new_data3)
predict_data['FrequencyofSoup'] = rf_soup.predict(new_data3)
predict_data['CookingEnergy'] = rf_cooking_energy.predict(new_data3)
predict_data['TimeforGasStove'] = rf_gas_stove_time.predict(new_data3)
# step 2
name4_data = pd.read_excel('Water Energy Consumption/cooking behavior-2.xlsx')
features4 = name4_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income', 'Frequencyofcookingonfire', 'FrequencyofSoup', 'CookingEnergy', 'TimeforGasStove']]
second_level_labels4 = name4_data[['breadmachine', 'electricoven', 'soymilk', 'electricstewpot', 'inductioncooktop', 'gasstove', 'electricpressurecooker', 'ricecooker', 'electricbakingpan', 'sterilizer', 'Numberofdishes']]

rf_bread_machine = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_electric_oven = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_soy_milk = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_electric_stew_pot = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_induction_cooktop = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_gas_stove = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_electric_pressure_cooker = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_rice_cooker = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_electric_baking_pan = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_sterilizer = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_dishes_num = RandomForestClassifier(n_estimators=trees, random_state=seeds)

rf_bread_machine.fit(features4, second_level_labels4['breadmachine'].values.ravel())
rf_electric_oven.fit(features4, second_level_labels4['electricoven'].values.ravel())
rf_soy_milk.fit(features4, second_level_labels4['soymilk'].values.ravel())
rf_electric_stew_pot.fit(features4, second_level_labels4['electricstewpot'].values.ravel())
rf_induction_cooktop.fit(features4, second_level_labels4['inductioncooktop'].values.ravel())
rf_gas_stove.fit(features4, second_level_labels4['gasstove'].values.ravel())
rf_electric_pressure_cooker.fit(features4, second_level_labels4['electricpressurecooker'].values.ravel())
rf_rice_cooker.fit(features4, second_level_labels4['ricecooker'].values.ravel())
rf_electric_baking_pan.fit(features4, second_level_labels4['electricbakingpan'].values.ravel())
rf_sterilizer.fit(features4, second_level_labels4['sterilizer'].values.ravel())
rf_dishes_num.fit(features4, second_level_labels4['Numberofdishes'].values.ravel())

new_data4 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income', 'Frequencyofcookingonfire', 'FrequencyofSoup', 'CookingEnergy', 'TimeforGasStove']]

predict_data['breadmachinefre'] = rf_bread_machine.predict(new_data4)
predict_data['eleovenfre'] = rf_electric_oven.predict(new_data4)
predict_data['soymilkfre'] = rf_soy_milk.predict(new_data4)
predict_data['elestewpotfre'] = rf_electric_stew_pot.predict(new_data4)
predict_data['inductionfre'] = rf_induction_cooktop.predict(new_data4)
predict_data['gasstovefre'] = rf_gas_stove.predict(new_data4)
predict_data['pressurefre'] = rf_electric_pressure_cooker.predict(new_data4)
predict_data['ricefre'] = rf_rice_cooker.predict(new_data4)
predict_data['elepanfre'] = rf_electric_baking_pan.predict(new_data4)
predict_data['sterilizerfre'] = rf_sterilizer.predict(new_data4)
predict_data['dishesnum'] = rf_dishes_num.predict(new_data4)

# predict cleaning behavior
# step 1
name5_data = pd.read_excel('Water Energy Consumption/cleaning behavior-1.xlsx')
features5 = name5_data[['gender', 'age', 'permonth_income', 'education', 'status','family_member', 'minor', 'retired','hhd_income','sweepingrobot','Electricmop']]
second_level_labels5 = name5_data[['Cleaningmethod']]
rf_second_level5 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_second_level5.fit(features5, second_level_labels5.values.ravel())
new_data5 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status','family_member', 'minor', 'retired','hhd_income','sweepingrobot','Electricmop']]
Y5 = rf_second_level5.predict(new_data5)
predict_data['Cleaningmethod'] = Y5
# step 2
name6_data = pd.read_excel('Water Energy Consumption/cleaning behavior-2.xlsx')
features6 = name6_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income','Cleaningmethod']]
second_level_labels6 = name6_data[['Sweepingfrequency', 'Moppingfrequency']]
rf_sweeping = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_mopping = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_sweeping.fit(features6, second_level_labels6['Sweepingfrequency'].values.ravel())
rf_mopping.fit(features6, second_level_labels6['Moppingfrequency'].values.ravel())
new_data6 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income', 'Cleaningmethod']]
predict_data['Sweepfre'] = rf_sweeping.predict(new_data6)
predict_data['Mopfre'] = rf_mopping.predict(new_data6)
# step 3
name7_data = pd.read_excel('Water Energy Consumption/cleaning behavior-3.xlsx')
features7 = name7_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]
second_level_labels7 = name7_data[['Averagenumberofwashesbeforecooking', 'Washingdishmethod', 'Washhotwater', 'Washingtime', 'washingcycles']]

rf_washes = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_dish = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_hotwater = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_wash_time = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_wash_cycles = RandomForestClassifier(n_estimators=trees, random_state=seeds)

rf_washes.fit(features7, second_level_labels7['Averagenumberofwashesbeforecooking'])
rf_dish.fit(features7, second_level_labels7['Washingdishmethod'].values.ravel())
rf_hotwater.fit(features7, second_level_labels7['Washhotwater'].values.ravel())
rf_wash_time.fit(features7, second_level_labels7['Washingtime'].values.ravel())
rf_wash_cycles.fit(features7, second_level_labels7['washingcycles'].values.ravel())

new_data7 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income']]

predict_data['washesavenum'] = rf_washes.predict(new_data7)
predict_data['washdishmethod'] = rf_dish.predict(new_data7)
predict_data['Washhotwater'] = rf_hotwater.predict(new_data7)
predict_data['washtime'] = rf_wash_time.predict(new_data7)
predict_data['washcycle'] = rf_wash_cycles.predict(new_data7)
# step 4
name8_data = pd.read_excel('Water Energy Consumption/cleaning behavior-4.xlsx')
features8 = name8_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income', 'Washingmachinemodel', 'Dryingorsterilizing']]
second_level_labels8 = name8_data[['washingmethod', 'Frequencyhandwashingclothesinwinter', 'Frequencyhandwashingclothesinspring', 'Frequencyhandwashingclothesinsummer', 'Frequencywashingmachineuseinwinter', 'Frequencywashingmachineuseinspring', 'Frequencywashingmachineuseinsummer', 'Rinsingmethod', 'Runninglaundrytime', 'Numberoftimesclothesarerinsed', 'Usehotwaterforlaundry', 'Dryingsterilizingclothesafterwashing']]

rf_wash_method = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_handwash_winter = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_handwash_spring = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_handwash_summer = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_washmachine_winter = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_washmachine_spring = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_washmachine_summer = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_rinse_method = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_laundry_time = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_num_clothes_rinsed = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_hot_water_laundry = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_dry_sterilize = RandomForestClassifier(n_estimators=trees, random_state=seeds)

rf_wash_method.fit(features8, second_level_labels8['washingmethod'].values.ravel())
rf_handwash_winter.fit(features8, second_level_labels8['Frequencyhandwashingclothesinwinter'].values.ravel())
rf_handwash_spring.fit(features8, second_level_labels8['Frequencyhandwashingclothesinspring'].values.ravel())
rf_handwash_summer.fit(features8, second_level_labels8['Frequencyhandwashingclothesinsummer'].values.ravel())
rf_washmachine_winter.fit(features8, second_level_labels8['Frequencywashingmachineuseinwinter'].values.ravel())
rf_washmachine_spring.fit(features8, second_level_labels8['Frequencywashingmachineuseinspring'].values.ravel())
rf_washmachine_summer.fit(features8, second_level_labels8['Frequencywashingmachineuseinsummer'].values.ravel())
rf_rinse_method.fit(features8, second_level_labels8['Rinsingmethod'].values.ravel())
rf_laundry_time.fit(features8, second_level_labels8['Runninglaundrytime'].values.ravel())
rf_num_clothes_rinsed.fit(features8, second_level_labels8['Numberoftimesclothesarerinsed'].values.ravel())
rf_hot_water_laundry.fit(features8, second_level_labels8['Usehotwaterforlaundry'].values.ravel())
rf_dry_sterilize.fit(features8, second_level_labels8['Dryingsterilizingclothesafterwashing'].values.ravel())

new_data8 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status', 'family_member', 'minor', 'retired', 'hhd_income', 'Washingmachinemodel', 'Dryingorsterilizing']]

predict_data['washmethod'] = rf_wash_method.predict(new_data8)
predict_data['handwashfrewinter'] = rf_handwash_winter.predict(new_data8)
predict_data['handwashfrespring'] = rf_handwash_spring.predict(new_data8)
predict_data['handwashfresummer'] = rf_handwash_summer.predict(new_data8)
predict_data['washmachinefrewinter'] = rf_washmachine_winter.predict(new_data8)
predict_data['washmachinefrespring'] = rf_washmachine_spring.predict(new_data8)
predict_data['washmachinefresummer'] = rf_washmachine_summer.predict(new_data8)
predict_data['Rinsemethod'] = rf_rinse_method.predict(new_data8)
predict_data['laundrytime'] = rf_laundry_time.predict(new_data8)
predict_data['Numclothesrinsed'] = rf_num_clothes_rinsed.predict(new_data8)
predict_data['hotwaterlaundry'] = rf_hot_water_laundry.predict(new_data8)
predict_data['Drysterilize'] = rf_dry_sterilize.predict(new_data8)

# predict HVAC behavior
name9_data = pd.read_excel('Water Energy Consumption/HVAC behavior.xlsx')
features9 = name9_data[['gender', 'age', 'permonth_income', 'education', 'status','family_member', 'minor', 'retired','hhd_income']]
second_level_labels9 = name9_data[['Timeheatingequipmentinwinter']]
rf_second_level9 = RandomForestClassifier(n_estimators=trees, random_state=seeds)
rf_second_level9.fit(features9, second_level_labels9.values.ravel())
new_data9 = predict_data[['gender', 'age', 'permonth_income', 'education', 'status','family_member', 'minor', 'retired','hhd_income']]
Y9 = rf_second_level9.predict(new_data9)
predict_data['heattime'] = Y9

# data to csv
predict_data.to_csv('Water Energy Consumption/people water behavior.csv', index=False)