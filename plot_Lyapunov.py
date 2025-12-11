import matplotlib.pyplot as plt
import numpy as np

# 1. Simülasyon Parametreleri
num_cycles = 5
convergence_criterion = 0.5

# ---- BURAYA SENİN VERDİĞİN ARRAY GELECEK ----
# ÖRNEK:
decay_values = [
    [3, 0, 0, 0],   # Cycle 1 V_k değerleri
    [7, 1, 0, 0],   # Cycle 2 V_k değerleri
    [8, 0, 0, 0],   # Cycle 3 V_k değerleri
    [4, 1, 0, 0],   # Cycle 4 V_k değerleri
    [9, 1, 0, 0],   # Cycle 5 V_k değerleri

]
# ----------------------------------------------

# Renk paleti
colors = plt.cm.viridis(np.linspace(0, 1, num_cycles))

# Grafik
plt.figure(figsize=(10, 7))

for i in range(num_cycles):
    v_history = decay_values[i]
    #k_history = list(range(1, len(v_history) + 1))
    k_history = [k + i*0.03 for k in range(1, len(v_history)+1)]
    plt.plot(
        k_history, 
        v_history,
        marker='o',
        linestyle='-',
        label=f'Cycle {i+1} (k={len(v_history)})',
        color=colors[i],
        linewidth=2
    )

# Yakınsama çizgisi
plt.axhline(
    y=convergence_criterion,
    color='r',
    linestyle='--',
    label='Convergence Criteria ($V_k < 0.5$)'
)

# Başlık ve eksenler
plt.title('Lyapunov Function ($V_k$) Cycle Based Convergence', fontsize=16)
plt.xlabel('Iteration (k)', fontsize=14)
plt.ylabel('Lyapunov Function Value ($V_k$)', fontsize=14)

plt.yticks(np.arange(0, 11, 1))  # y-axis 1’er 1’er artsın
plt.xticks(np.arange(0, 5, 1))

plt.ylim(bottom=-0.05)
plt.xlim(left=0.8)

plt.legend(fontsize=12, loc='upper right')

# plt.text(
    # 0.95, 0.95,
    # 'Kararlılık Kanıtı:\nTüm çizgiler monoton azalır\n$\\Delta V_k = V_{k+1} - V_k \\leq 0$',
    # horizontalalignment='right',
    # verticalalignment='top',
    # transform=plt.gca().transAxes,
    # fontsize=12,
    # bbox=dict(boxstyle='round,pad=0.5', fc='aliceblue', alpha=0.9)
# )

plt.savefig('lyapunov_from_array.png', dpi=300, bbox_inches='tight')
print("Grafik 'lyapunov_from_array.png' olarak kaydedildi.")

