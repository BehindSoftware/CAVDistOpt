# # Plotting centralized vs distributed based on user's requested percentage differences
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# from caas_jupyter_tools import display_dataframe_to_user

# # Scenarios
# scenarios = ["Low (20 vehicles)", "Medium (28 vehicles)", "High (40 vehicles)"]

# # Centralized baseline values chosen within requested ranges
# central_travel = np.array([120.0, 180.0, 260.0])   # seconds (within 120-280)
# central_fuel = np.array([2.30, 2.70, 3.10])        # mg/s (within 2.30-3.20)

# # Percentage differences per user's spec: Low 6-8% -> pick 7%, Medium 3-5% -> pick 4%, High 1-2% -> pick 1.5%
# pct_travel = np.array([0.07, 0.04, 0.015])
# pct_fuel   = np.array([0.07, 0.04, 0.015])

# dist_travel = central_travel * (1 + pct_travel)
# dist_fuel   = central_fuel * (1 + pct_fuel)

# # Build dataframe for display
# df = pd.DataFrame({
    # "Scenario": scenarios,
    # "Centralized Travel (s/veh)": central_travel,
    # "Distributed Travel (s/veh)": np.round(dist_travel, 2),
    # "Centralized Fuel (mg/s per veh)": central_fuel,
    # "Distributed Fuel (mg/s per veh)": np.round(dist_fuel, 3),
    # "Travel Diff (%)": np.round(100*(dist_travel-central_travel)/central_travel, 2),
    # "Fuel Diff (%)": np.round(100*(dist_fuel-central_fuel)/central_fuel, 2)
# })

# display_dataframe_to_user("Centralized_vs_Distributed_Summary", df)

# # Plotting
# x = np.arange(len(scenarios))
# width = 0.35

# fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# # Travel time bar chart
# axes[0].bar(x - width/2, central_travel, width, label='Centralized')
# axes[0].bar(x + width/2, dist_travel, width, label='Distributed')
# axes[0].set_xticks(x)
# axes[0].set_xticklabels(scenarios, rotation=20)
# axes[0].set_ylabel("Average Travel Time (s per vehicle)")
# axes[0].set_title("Average Travel Time by Scenario")
# axes[0].legend()
# axes[0].grid(axis='y', linestyle=':', linewidth=0.5)

# # Fuel consumption bar chart
# axes[1].bar(x - width/2, central_fuel, width, label='Centralized')
# axes[1].bar(x + width/2, dist_fuel, width, label='Distributed')
# axes[1].set_xticks(x)
# axes[1].set_xticklabels(scenarios, rotation=20)
# axes[1].set_ylabel("Average Fuel Consumption (mg/s per vehicle)")
# axes[1].set_title("Average Fuel Consumption by Scenario")
# axes[1].legend()
# axes[1].grid(axis='y', linestyle=':', linewidth=0.5)

# plt.tight_layout()
# plt.show()

# # Save figure
# fig.savefig('/mnt/data/centralized_vs_distributed_pct_plot.png')
# print("Saved plot to /mnt/data/centralized_vs_distributed_pct_plot.png")

import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)

# Trafik yoğunluğu seviyeleri
scenarios = ['Low (20)', 'Medium (28)', 'High (40)']
n_samples = 10  # her yoğunlukta 10 ölçüm

# Centralized ortalama değerleri (trend: travel ↑, fuel ↓)
central_tt_mean = np.array([130, 190, 260])  # saniye
central_fc_mean = np.array([3.2, 2.8, 2.4])  # liters per 100 km

# Distributed fark oranları
pct_travel = [(0.18, 0.26), (0.13, 0.15), (0.09, 0.11)]
pct_fuel   = [(0.16, 0.18), (0.13, 0.15), (0.09, 0.11)]

# Örnekleme noktaları oluştur
central_tt, dist_tt, central_fc, dist_fc = [], [], [], []
x_vals = []

for i in range(len(scenarios)):
    # Hafif dalgalanma (zigzag)
    c_tt = central_tt_mean[i] + np.random.normal(0, 3, n_samples)
    c_fc = central_fc_mean[i] + np.random.normal(0, 0.03, n_samples)
    
    # Distributed fark + rastgele oran
    d_tt = c_tt * (1 + np.random.uniform(*pct_travel[i], n_samples))
    d_fc = c_fc * (1 + np.random.uniform(*pct_fuel[i], n_samples))
    
    central_tt.extend(c_tt)
    dist_tt.extend(d_tt)
    central_fc.extend(c_fc)
    dist_fc.extend(d_fc)
    
    # x eksenini yoğunluk gruplarına göre kaydır
    x_vals.extend(np.linspace(i*11+1, i*11+10, n_samples))

# Çizim
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
colors = ['#E6F2FF', '#E8F8F5', '#FEF9E7']

# --- Travel Time ---
axes[0].plot(x_vals, central_tt, 'o-', color='tab:blue', label='Centralized', linewidth=2)
axes[0].plot(x_vals, dist_tt, 's--', color='tab:orange', label='Distributed', linewidth=2)
axes[0].set_title("Average Travel Time vs Traffic Density", fontsize=13)
axes[0].set_ylabel("Travel Time (s per vehicle)")
axes[0].set_xlabel("Traffic Density Samples")
axes[0].grid(True, linestyle='--', alpha=0.5)
axes[0].legend()

# Arka plan bölgeleme
for i, label in enumerate(scenarios):
    start, end = i*11+0.5, (i+1)*11
    axes[0].axvspan(start, end, color=colors[i], alpha=0.25)
    axes[0].text(start+3, max(central_tt)+5, label, fontsize=9, color='gray')

axes[0].set_ylim(110, 300)

# --- Fuel Consumption ---
axes[1].plot(x_vals, central_fc, 'o-', color='tab:blue', label='Centralized', linewidth=2)
axes[1].plot(x_vals, dist_fc, 's--', color='tab:orange', label='Distributed', linewidth=2)
axes[1].set_title("Average Fuel Consumption vs Traffic Density", fontsize=13)
axes[1].set_ylabel("Fuel Consumption (liters per 100 km)")
axes[1].set_xlabel("Traffic Density Samples")
axes[1].grid(True, linestyle='--', alpha=0.5)
axes[1].legend()

for i, label in enumerate(scenarios):
    start, end = i*11+0.5, (i+1)*11
    axes[1].axvspan(start, end, color=colors[i], alpha=0.25)
    axes[1].text(start+3, max(central_fc)+0.05, label, fontsize=9, color='gray')

axes[1].set_ylim(2.2, 3.8)

plt.tight_layout()
plt.show()
