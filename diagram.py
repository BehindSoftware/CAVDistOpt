# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Manually input data
# speed_location_factors = [
#     0.1, 0.2, 0.3, 0.2, 0.2,
#     0.2, 0.2, 0.2, 0.2, 0.2,
#     0.2, 0.2, 0.2, 0.2, 0.2
# ]

# travel_times = [
#     67, 71, 75, 56, 71,
#     83, 72, 72, 71, 70,
#     72, 71, 71, 71, 71
# ]

# # Create DataFrame
# df = pd.DataFrame({
#     'Speed-Location Factor': speed_location_factors,
#     'Travel Time (s)': travel_times
# })

# # Set plot style
# sns.set(style="whitegrid")

# # Create scatter plot with regression line
# plt.figure(figsize=(8, 5))
# sns.scatterplot(data=df, x='Speed-Location Factor', y='Travel Time (s)', color='blue', s=80)
# sns.regplot(data=df, x='Speed-Location Factor', y='Travel Time (s)', scatter=False, color='red', ci=None)

# # Add titles and labels
# plt.title('Effect of Speed-Location Factor on Travel Time', fontsize=14)
# plt.xlabel('Speed-Location Factor')
# plt.ylabel('Travel Time (s)')

# # Show plot
# plt.tight_layout()
# plt.show()

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Data
df = pd.DataFrame({
    'Speed-Location Factor': [
        0.1, 0.2, 0.3, 0.2, 0.2,
        0.2, 0.2, 0.2, 0.2, 0.2,
        0.2, 0.2, 0.2, 0.2, 0.2
    ],
    'Travel Time (s)': [
        67, 71, 75, 56, 71,
        83, 72, 72, 71, 70,
        72, 71, 71, 71, 71
    ]
})

# Plot
plt.figure(figsize=(8, 5))
#sns.boxplot(data=df, x='Speed-Location Factor', y='Travel Time (s)', palette="pastel")
#sns.violinplot(data=df, x='Speed-Location Factor', y='Travel Time (s)', palette="muted")
sns.barplot(data=df, x='Speed-Location Factor', y='Travel Time (s)', ci='sd', palette="Blues")


# Labels
plt.title('Boxplot: Travel Time vs Speed-Location Factor')
plt.xlabel('Speed-Location Factor')
plt.ylabel('Travel Time (s)')
plt.tight_layout()
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Define data
df = pd.DataFrame({
    'Speed-Location Factor': [
        0.1, 0.2, 0.3, 0.2, 0.2,
        0.2, 0.2, 0.2, 0.2, 0.2,
        0.2, 0.2, 0.2, 0.2, 0.2
    ],
    'Fuel Consumption': [
        4.205791616, 3.934020451, 3.802172125, 4.802890086, 3.934020451,
        3.422366056, 3.936374425, 3.941730908, 3.934020451, 4.01046715,
        3.993045676, 3.953895637, 3.934020451, 3.93639657, 3.93639657
    ]
})

# Set plot style
sns.set(style="whitegrid")

# Create boxplot
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x='Speed-Location Factor', y='Fuel Consumption', palette="Set2")

# Add labels and title
plt.title('Fuel Consumption vs Speed-Location Factor', fontsize=14)
plt.xlabel('Speed-Location Factor')
plt.ylabel('Fuel Consumption (liters or L/100km equivalent)')
plt.tight_layout()
plt.show()


import matplotlib.pyplot as plt

# Given data
rho_values = [1, 1, 1, 0.1, 1, 2.5, 1, 1, 1, 1, 1, 1, 1, 1, 1]
travel_time = [67, 71, 75, 56, 71, 83, 72, 72, 71, 70, 72, 71, 71, 71, 71]
fuel_consumption = [
    4.205791616, 3.934020451, 3.802172125, 4.802890086, 3.934020451,
    3.422366056, 3.936374425, 3.941730908, 3.934020451, 4.01046715,
    3.993045676, 3.953895637, 3.934020451, 3.93639657, 3.93639657
]

# Convert rho values to string for x-axis labeling
rho_labels = [str(r) for r in rho_values]

fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Bar plot for Travel Time
axs[0].bar(range(len(travel_time)), travel_time, color='skyblue')
axs[0].set_xticks(range(len(rho_labels)))
axs[0].set_xticklabels(rho_labels, rotation=45)
axs[0].set_xlabel('RHO')
axs[0].set_ylabel('Travel Time (s)')
axs[0].set_title('Travel Time vs RHO')

# Bar plot for Fuel Consumption
axs[1].bar(range(len(fuel_consumption)), fuel_consumption, color='lightgreen')
axs[1].set_xticks(range(len(rho_labels)))
axs[1].set_xticklabels(rho_labels, rotation=45)
axs[1].set_xlabel('RHO')
axs[1].set_ylabel('Fuel Consumption')
axs[1].set_title('Fuel Consumption vs RHO')

plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import pandas as pd

# Data
data = {
    'Alpha': [-3, -3, -3, -3, -3, -3, -3, -3, -3, -4, -2, -1, -3, -3, -3],
    'Alpha_Prime': [3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 2, 1, 3, 3, 3],
    'Epsilon_Prime': [60, 60, 60, 60, 60, 60, 60, 60, 60, 90, 60, 60, 60, 75, 90],
    'Travel_Time': [67, 71, 75, 56, 71, 83, 72, 72, 71, 70, 72, 71, 71, 71, 71],
    'Fuel_Consumption': [
        4.205791616, 3.934020451, 3.802172125, 4.802890086, 3.934020451,
        3.422366056, 3.936374425, 3.941730908, 3.934020451, 4.01046715,
        3.993045676, 3.953895637, 3.934020451, 3.93639657, 3.93639657
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Plotting
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Boxplot Travel Time by Alpha
df.boxplot(column='Travel_Time', by='Alpha', ax=axs[0, 0])
axs[0, 0].set_title('Travel Time by Alpha')
axs[0, 0].set_ylabel('Travel Time (s)')
axs[0, 0].set_xlabel('Alpha')

# Boxplot Travel Time by Epsilon_Prime
df.boxplot(column='Travel_Time', by='Epsilon_Prime', ax=axs[0, 1])
axs[0, 1].set_title('Travel Time by Epsilon_Prime')
axs[0, 1].set_ylabel('Travel Time (s)')
axs[0, 1].set_xlabel('Epsilon_Prime')

# Boxplot Fuel Consumption by Alpha
df.boxplot(column='Fuel_Consumption', by='Alpha', ax=axs[1, 0])
axs[1, 0].set_title('Fuel Consumption by Alpha')
axs[1, 0].set_ylabel('Fuel Consumption')
axs[1, 0].set_xlabel('Alpha')

# Boxplot Fuel Consumption by Epsilon_Prime
df.boxplot(column='Fuel_Consumption', by='Epsilon_Prime', ax=axs[1, 1])
axs[1, 1].set_title('Fuel Consumption by Epsilon_Prime')
axs[1, 1].set_ylabel('Fuel Consumption')
axs[1, 1].set_xlabel('Epsilon_Prime')

plt.suptitle('Effect of Parameters on Travel Time and Fuel Consumption')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Parameters repeated for all 4 scenarios, 15 test cases each
params = {
    'Alpha': [-3, -3, -3, -3, -3, -3, -3, -3, -3, -4, -2, -1, -3, -3, -3],
    'Alpha_Prime': [3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 2, 1, 3, 3, 3],
    'Epsilon_Prime': [60, 60, 60, 60, 60, 60, 60, 60, 60, 90, 60, 60, 60, 75, 90]
}

# Results for each scenario (15 testcases each)
travel_time = [
    # Scenario 1
    67, 71, 75, 56, 71, 83, 72, 72, 71, 70, 72, 71, 71, 71, 71,
    # Scenario 2
    190, 201, 217, 165, 201, 240, 201, 201, 201, 201, 201, 201, 201, 201, 201,
    # Scenario 3
    199, 210, 228, 168, 210, 254, 203, 210, 210, 210, 203, 208, 210, 210, 210,
    # Scenario 4
    188, 199, 215, 161, 199, 232, 197, 200, 199, 200, 199, 199, 199, 199, 200
]

fuel_consumption = [
    # Scenario 1
    4.205791616, 3.934020451, 3.802172125, 4.802890086, 3.934020451,
    3.422366056, 3.936374425, 3.941730908, 3.934020451, 4.01046715,
    3.993045676, 3.953895637, 3.934020451, 3.93639657, 3.93639657,
    # Scenario 2
    3.616783394, 3.426702583, 3.138372099, 4.234311002, 3.426702583,
    2.880304115, 3.399725941, 3.403150467, 3.426702583, 3.425435037,
    3.404407706, 3.366720318, 3.426702583, 3.425095324, 3.425553316,
    # Scenario 3
    3.500106683, 3.299624256, 3.001827519, 4.024111873, 3.299624256,
    2.75340749, 3.231333122, 3.303247414, 3.299624256, 3.299575799,
    3.225217551, 3.166728015, 3.299624256, 3.298274247, 3.299570697,
    # Scenario 4
    3.64857941, 3.452827782, 3.188794926, 4.114415127, 3.452827782,
    2.906053957, 3.446368623, 3.441870231, 3.452827782, 3.456446706,
    3.45697774, 3.457724587, 3.452827782, 3.455867909, 3.456533605
]

# Build dataframe
rows = []
scenarios = ['Scenario 1', 'Scenario 2', 'Scenario 3', 'Scenario 4']

for i, scenario in enumerate(scenarios):
    for j in range(15):
        idx = i * 15 + j
        rows.append({
            'Scenario': scenario,
            'Testcase': f'TC{j+1}',
            'Alpha': params['Alpha'][j],
            'Alpha_Prime': params['Alpha_Prime'][j],
            'Epsilon_Prime': params['Epsilon_Prime'][j],
            'Travel_Time': travel_time[idx],
            'Fuel_Consumption': fuel_consumption[idx]
        })

df = pd.DataFrame(rows)

# Plot boxplots grouped by Scenario
plt.figure(figsize=(16, 8))

plt.subplot(1, 2, 1)
sns.boxplot(x='Scenario', y='Travel_Time', data=df, palette='Pastel1')
plt.title('Travel Time Distribution by Scenario')
plt.ylabel('Travel Time (s)')
plt.xlabel('Scenario')

plt.subplot(1, 2, 2)
sns.boxplot(x='Scenario', y='Fuel_Consumption', data=df, palette='Pastel2')
plt.title('Fuel Consumption Distribution by Scenario')
plt.ylabel('Fuel Consumption')
plt.xlabel('Scenario')

plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Use the same dataframe 'df' from before

plt.figure(figsize=(18, 12))

# Travel Time vs Alpha
plt.subplot(3, 2, 1)
sns.boxplot(x='Alpha', y='Travel_Time', data=df, palette='Set3')
plt.title('Travel Time vs Alpha')

# Fuel Consumption vs Alpha
plt.subplot(3, 2, 2)
sns.boxplot(x='Alpha', y='Fuel_Consumption', data=df, palette='Set2')
plt.title('Fuel Consumption vs Alpha')

# Travel Time vs Alpha_Prime
plt.subplot(3, 2, 3)
sns.boxplot(x='Alpha_Prime', y='Travel_Time', data=df, palette='Set3')
plt.title('Travel Time vs Alpha_Prime')

# Fuel Consumption vs Alpha_Prime
plt.subplot(3, 2, 4)
sns.boxplot(x='Alpha_Prime', y='Fuel_Consumption', data=df, palette='Set2')
plt.title('Fuel Consumption vs Alpha_Prime')

# Travel Time vs Epsilon_Prime
plt.subplot(3, 2, 5)
sns.boxplot(x='Epsilon_Prime', y='Travel_Time', data=df, palette='Set3')
plt.title('Travel Time vs Epsilon_Prime')

# Fuel Consumption vs Epsilon_Prime
plt.subplot(3, 2, 6)
sns.boxplot(x='Epsilon_Prime', y='Fuel_Consumption', data=df, palette='Set2')
plt.title('Fuel Consumption vs Epsilon_Prime')

plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Assuming 'df' is your DataFrame with the data

plt.figure(figsize=(18, 12))

# Travel Time vs Alpha
plt.subplot(3, 2, 1)
sns.regplot(x='Alpha', y='Travel_Time', data=df, scatter_kws={'s':50}, line_kws={'color':'red'})
plt.title('Travel Time vs Alpha')

# Fuel Consumption vs Alpha
plt.subplot(3, 2, 2)
sns.regplot(x='Alpha', y='Fuel_Consumption', data=df, scatter_kws={'s':50}, line_kws={'color':'red'})
plt.title('Fuel Consumption vs Alpha')

# Travel Time vs Alpha_Prime
plt.subplot(3, 2, 3)
sns.regplot(x='Alpha_Prime', y='Travel_Time', data=df, scatter_kws={'s':50}, line_kws={'color':'red'})
plt.title('Travel Time vs Alpha_Prime')

# Fuel Consumption vs Alpha_Prime
plt.subplot(3, 2, 4)
sns.regplot(x='Alpha_Prime', y='Fuel_Consumption', data=df, scatter_kws={'s':50}, line_kws={'color':'red'})
plt.title('Fuel Consumption vs Alpha_Prime')

# Travel Time vs Epsilon_Prime
plt.subplot(3, 2, 5)
sns.regplot(x='Epsilon_Prime', y='Travel_Time', data=df, scatter_kws={'s':50}, line_kws={'color':'red'})
plt.title('Travel Time vs Epsilon_Prime')

# Fuel Consumption vs Epsilon_Prime
plt.subplot(3, 2, 6)
sns.regplot(x='Epsilon_Prime', y='Fuel_Consumption', data=df, scatter_kws={'s':50}, line_kws={'color':'red'})
plt.title('Fuel Consumption vs Epsilon_Prime')

plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import numpy as np

# Data from your message (just copy-pasting for clarity)
distributed_travel_time = [
    67, 71, 75, 56, 71, 83, 72, 72, 71, 70, 72, 71, 71, 71, 71,
    190, 201, 217, 165, 201, 240, 201, 201, 201, 201, 201, 201, 201, 201, 201,
    199, 210, 228, 168, 210, 254, 203, 210, 210, 210, 203, 208, 210, 210, 210,
    188, 199, 215, 161, 199, 232, 197, 200, 199, 200, 199, 199, 199, 199, 200
]

distributed_fuel = [
    4.205791616, 3.934020451, 3.802172125, 4.802890086, 3.934020451, 3.422366056,
    3.936374425, 3.941730908, 3.934020451, 4.01046715, 3.993045676, 3.953895637,
    3.934020451, 3.93639657, 3.93639657, 3.616783394, 3.426702583, 3.138372099,
    4.234311002, 3.426702583, 2.880304115, 3.399725941, 3.403150467, 3.426702583,
    3.425435037, 3.404407706, 3.366720318, 3.426702583, 3.425095324, 3.425553316,
    3.500106683, 3.299624256, 3.001827519, 4.024111873, 3.299624256, 2.75340749,
    3.231333122, 3.303247414, 3.299624256, 3.299575799, 3.225217551, 3.166728015,
    3.299624256, 3.298274247, 3.299570697, 3.64857941, 3.452827782, 3.188794926,
    4.114415127, 3.452827782, 2.906053957, 3.446368623, 3.441870231, 3.452827782,
    3.456446706, 3.45697774, 3.457724587, 3.452827782, 3.455867909, 3.456533605
]

centralized_travel_time = [
    60, 60, 60, 60, 60, 60, 60, 60, 60, 40, 59, 63, 60, 45, 40,
    158, 158, 158, 158, 158, 158, 158, 158, 158, 123, 169, 172, 158, 141, 126,
    168, 168, 168, 168, 168, 168, 168, 168, 168, 124, 172, 184, 168, 141, 125,
    163, 163, 163, 163, 163, 163, 163, 163, 163, 126, 170, 172, 163, 143, 130
]

centralized_fuel = [
    4.402500457, 4.402500457, 4.402500457, 4.402500457, 4.402500457, 4.402500457,
    4.402500457, 4.402500457, 4.402500457, 6.292870029, 4.049753528, 4.504231648,
    4.402500457, 4.670516537, 5.354293976, 3.849108874, 3.849108874, 3.849108874,
    3.849108874, 3.849108874, 3.849108874, 3.849108874, 3.849108874, 5.796858892,
    3.780941638, 3.642375325, 3.849108874, 4.768890631, 5.499915998, 3.538360939,
    3.538360939, 3.538360939, 3.538360939, 3.538360939, 3.538360939, 3.538360939,
    3.538360939, 3.538360939, 5.185232884, 3.66466535, 3.397246531, 3.538360939,
    4.429562946, 4.902152257, 3.482820915, 3.482820915, 3.482820915, 3.482820915,
    3.482820915, 3.482820915, 3.482820915, 3.482820915, 5.093322702, 3.426836101,
    3.4321062, 3.482820915, 4.442609543, 4.915719125
]

# Number of test cases
min_len = min(len(distributed_travel_time), len(centralized_travel_time), len(distributed_fuel), len(centralized_fuel))
test_cases = np.arange(1, min_len + 1)

distributed_travel_time = distributed_travel_time[:min_len]
distributed_fuel = distributed_fuel[:min_len]
centralized_travel_time = centralized_travel_time[:min_len]
centralized_fuel = centralized_fuel[:min_len]


plt.figure(figsize=(14, 6))

# Plot Travel Time comparison
plt.subplot(1, 2, 1)
plt.plot(test_cases, distributed_travel_time, marker='o', label='Distributed Travel Time')
plt.plot(test_cases, centralized_travel_time, marker='x', label='Centralized Travel Time')
plt.xlabel('Test Case')
plt.ylabel('Travel Time (s)')
plt.title('Travel Time: Distributed vs Centralized Optimization')
plt.legend()
plt.grid(True)

# Plot Fuel Consumption comparison
plt.subplot(1, 2, 2)
plt.plot(test_cases, distributed_fuel, marker='o', label='Distributed Fuel Consumption')
plt.plot(test_cases, centralized_fuel, marker='x', label='Centralized Fuel Consumption')
plt.xlabel('Test Case')
plt.ylabel('Fuel Consumption')
plt.title('Fuel Consumption: Distributed vs Centralized Optimization')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
