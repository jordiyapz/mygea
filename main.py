# ========= Algoritma genetika =========
# Tugas Pengantar Kecerdasan Buatan
# ditulis oleh Jordi Yaputra (130110353)
#
# lisensi: unlicense

# %% import
from matplotlib import pyplot as plt
import gea
import math as m
from utils import histogram

# %% pengaturan
verbosity_level = 0  # rentang [0, 2]
rekam_history = True  # set True jika butuh graph
plt.style.use('seaborn-whitegrid')

# %% hyper parameter
ukuran_populasi = 500
resolusi = 10
peluang_mutasi = .09
crossover_rate = .7
maks_generasi = int((10000 - ukuran_populasi * (1 - crossover_rate)) \
                   / (ukuran_populasi * crossover_rate))
print('Maksimum generasi:', maks_generasi)

# stopping_crit = (gea.Stop.TRESHOLD, 5.0218)   # fungsi kurang
stopping_crit = (gea.Stop.TRESHOLD, 16.49)  # fungsi eksponen
# stopping_crit = (gea.Stop.NO_IMPROVE, 10)
# %% fungsi hipothesis dan fitness
def h(x1, x2):
  return m.cos(x1) * m.sin(x2) - x1 / (x2**2 + 1)

def fungsiFitnessKurang(x1, x2):
  return 3 - h(x1, x2)

def fungsiFitnessBagi(x1, x2):
  return 1 / (h(x1, x2) + 2)

def fungsiFitnessEksponen(x1, x2):
  return pow(4, -h(x1, x2))

# %% single run
gen = gea.Gea(fungsi_fitness=fungsiFitnessEksponen,
              range1=(-1, 2),
              range2=(-1, 1),
              resolusi=resolusi,
              ukuran_populasi=ukuran_populasi)

result, iterasi, fitness_history = gen.fit(stopping_crit=stopping_crit,
                                           maks_generasi=maks_generasi,
                                           crossover_rate=crossover_rate,
                                           peluang_mutasi=peluang_mutasi,
                                           rekam_history=rekam_history,
                                           verbose=verbosity_level)

x1, x2 = result

print('\nBanyak iterasi: %d\n' % iterasi)
print('fitness = %f' % gen.fitness)
print('h(x1, x2) = %f' % h(x1, x2))
print('x1 = %f' % x1)
print('x2 = %f' % x2)

if rekam_history:
  plt.title('Fitness History')
  plt.xlabel('Generasi')
  plt.ylabel('Fitness')
  plt.plot(fitness_history)
else:
  print('Tidak ada rekaman')

# %% Statistik

num_of_run = 20

best_fit_hist = []
iterasi_hist = []

gen = gea.Gea(fungsi_fitness=fungsiFitnessEksponen,
              range1=(-1, 2),
              range2=(-1, 1),
              resolusi=resolusi,
              ukuran_populasi=ukuran_populasi)

print('Running', end='')
for _ in range(num_of_run):
  gen.reset()
  result, iterasi, _ = gen.fit(stopping_crit=stopping_crit,
                              maks_generasi=maks_generasi,
                              crossover_rate=crossover_rate,
                              peluang_mutasi=peluang_mutasi,
                              rekam_history=rekam_history,
                              verbose=verbosity_level)
  best_fit_hist.append(gen.fitness)
  iterasi_hist.append(iterasi)
  print('.', end='')
print('done')

print('Rata-rata banyak generasi:', sum(iterasi_hist)/num_of_run)
print('Rata-rata fitness akhir:', sum(best_fit_hist)/num_of_run)

plt.subplot(1,2,1)
plt.title('Histogram Fitness')
plt.xlabel('fitness')
plt.ylabel('frekuensi')
_ = plt.hist(best_fit_hist)

plt.tight_layout(pad=2.5)
plt.subplot(1,2,2)
plt.title('Histogram #Generasi')
plt.xlabel('banyak generasi')
_ = plt.hist(iterasi_hist)

# %%
