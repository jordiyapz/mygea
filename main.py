# ========= Algoritma genetika =========
# Tugas Pengantar Kecerdasan Buatan
# ditulis oleh Jordi Yaputra (130110353)
#
# lisensi: unlicense

# %% import
from matplotlib import pyplot as plt
from math import sin, cos
import gea

# %% pengaturan
verbosity_level = 1  # rentang [0, 3]
rekam_history = True  # set True jika butuh graph
plt.style.use('seaborn-whitegrid')

# %% fungsi hipothesis dan fitness
def h(fenotip):
  x1, x2 = fenotip
  return cos(x1) * sin(x2) - x1 / (x2**2 + 1)

def fungsiFitnessKurang(fenotip):
  return 3 - h(fenotip)

def fungsiFitnessBagi(fenotip):
  return 1 / (h(fenotip) + 2)

def fungsiFitnessEksponen(fenotip):
  return pow(4, -h(fenotip))

# %% hyper parameter

""" tebakan terbaik
# hasil:
# rata-rata generasi = 9.9
# rata-rata fitness = 16.490743452040977

ukuran_populasi = 750
resolusi = 10
peluang_mutasi = .09
crossover_rate = .7
# """

""" hasil GA Tuner #1
# hasil:
# rata-rata generasi = 6.05
# rata-rata fitness  = 16.49107486703866
# selalu konvergen global

ukuran_populasi = 779
resolusi = 8
peluang_mutasi = 0.021176470588235297
crossover_rate = 0.8694117647058823
# """

""" hasil GA Tuner #2
# hasil:
# rata-rata generasi = 4.2
# rata-rata fitness  = 16.4905685130365
# selalu konvergen global

ukuran_populasi = 591
resolusi = 7
peluang_mutasi = 0.13592156862745097
crossover_rate = 0.9470588235294117
# """

# """ hasil GA Tuner #3
# hasil:
# rata-rata generasi = 3.4
# rata-rata fitness  = 16.4905685130365
# selalu konvergen global

ukuran_populasi = 797
resolusi = 7
peluang_mutasi = 0.16945098039215686
crossover_rate = 0.9400000000000001
# """

fungsiFitness = fungsiFitnessEksponen
maks_generasi = int((10000 - ukuran_populasi * (1 - crossover_rate)) \
                   / (ukuran_populasi * crossover_rate))
print('Maksimum generasi:', maks_generasi)

# stopping_crit = (gea.Stop.MAX_IT,)
# stopping_crit = (gea.Stop.TRESHOLD, 5.0218)   # fungsi kurang
stopping_crit = (gea.Stop.TRESHOLD, 16.49)  # fungsi eksponen
# stopping_crit = (gea.Stop.NO_IMPROVE, round(maks_generasi*.2))

# %% single run
gen = gea.Gea(fungsi_fitness=fungsiFitness,
              ranges=((-1, 2), (-1, 1)),
              resolusi=resolusi,
              ukuran_populasi=ukuran_populasi)

fenotip, iterasi, fitness_history = gen.fit(stopping_crit=stopping_crit,
                                            maks_generasi=maks_generasi,
                                            crossover_rate=crossover_rate,
                                            peluang_mutasi=peluang_mutasi,
                                            rekam_history=rekam_history,
                                            verbose=verbosity_level)

print('Banyak generasi:', iterasi)
print('Kromosom:\n', gen.best_individu[0].kromosom)
print('fitness =', fungsiFitness(fenotip))
print('h(x1, x2) =', h(fenotip))
print('x1 =', fenotip[0])
print('x2 =', fenotip[1])

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

gen = gea.Gea(fungsi_fitness=fungsiFitness,
              ranges=((-1, 2), (-1, 1)),
              resolusi=resolusi,
              ukuran_populasi=ukuran_populasi)

print('Running', end='')
for _ in range(num_of_run):
  gen.reset()
  fenotip, iterasi, _ = gen.fit(stopping_crit=stopping_crit,
                              maks_generasi=maks_generasi,
                              crossover_rate=crossover_rate,
                              peluang_mutasi=peluang_mutasi,
                              rekam_history=rekam_history,
                              verbose=0)
  best_fit_hist.append(fungsiFitness(fenotip))
  iterasi_hist.append(iterasi)
  print('.', end='')
print(' done!')

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

# %% experiment lab