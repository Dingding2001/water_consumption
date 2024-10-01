import pandas as pd
from scipy.optimize import minimize

household = pd.read_csv('EnergyConsumption/household electricity.csv')

districts = pd.read_csv('EnergyConsumption/Regional Electricity.csv')
districts.set_index('District', inplace=True)

for district in household['District'].unique():
    household_district = household.loc[household['District'] == district].copy()

    household_district.loc[:, 'min'] = household_district['Yearly_electricity'] * (1 - household_district['Certainty'])
    household_district.loc[:, 'max'] = household_district['Yearly_electricity'] * (1 + household_district['Certainty'])

    total_electricity = districts.loc[district, 'Electricity']

    def objective(x):
        return (x.sum() - total_electricity) ** 2

    bounds = list(zip(household_district['min'], household_district['max']))

    result = minimize(objective, household_district['Yearly_electricity'], bounds=bounds)

    household_district.loc[:, 'Adjusted_electricity'] = result.x
    household.loc[household['District'] == district, 'Adjusted_electricity'] = household_district['Adjusted_electricity']

household.to_csv('EnergyConsumption/Adjusted Household Electricity.csv', index=False)