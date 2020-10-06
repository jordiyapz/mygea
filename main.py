# ========= Algoritma genetika =========
# Tugas Pengantar Kecerdasan Buatan
# ditulis oleh Jordi Yaputra (130110353)
#
# lisensi: unlicense

# %% import
from gea import *

# %% pengaturan
verbosity_level = 0  # rentang [0, 2]
rekam_history = True  # set True jika butuh graph
maks_iterasi = 1000  # batas apabila treshold tidak terpenuhi

# %% fungsi hipothesis dan fitness
def h(x1, x2):
  return cos(x1) * sin(x2) - x1 / (x2**2 + 1)

def fungsiFitness(x1, x2):
  return 1 / (h(x1, x2) + 2)

# %% hyper parameter
ukuran_populasi = 50
resolusi = 5
peluang_mutasi = .04
treshold = 200
banyak_pasangan = 17  # harus kurang dari setengah ukuran populasi

# %% main
iterasi = 0
populasi = [Individu(resolusi=resolusi) for _ in range(ukuran_populasi)]
fitness_history = []

fitness_list = hitungFitness(fungsiFitness, populasi)
peluang_list = hitungPeluang(fitness_list)
best_fit = max(fitness_list)
if rekam_history:
  fitness_history.append(best_fit)

printTabel(populasi, fitness_list, peluang_list, verbose=verbosity_level)

while iterasi < maks_iterasi and best_fit < treshold:
  # print('Generasi: %d' % i)
  pasangan_index_ortu = seleksiOrtu(peluang_list)

  # regenerasi
  populasi = urutanPopulasi(populasi, fitness_list)
  populasi_baru = []

  for pasangan_idx in pasangan_index_ortu[:min(
      banyak_pasangan, len(pasangan_index_ortu))]:
    pasangan = tuple(populasi[idx] for idx in pasangan_idx)
    k1, k2 = pindahSilang(pasangan)
    populasi_baru.append(Individu(k1))
    populasi_baru.append(Individu(k2))

  l = len(populasi) - len(populasi_baru)
  populasi[l:] = populasi_baru
  mutasi(populasi, peluang_mutasi)

  # kalkulasi fitness
  fitness_list = hitungFitness(fungsiFitness, populasi)
  best_fit = max(fitness_list)
  if rekam_history:
    fitness_history.append(best_fit)

  printTabel(populasi, fitness_list, peluang_list, verbose=verbosity_level)
  iterasi += 1

print('\nBanyak iterasi: %d\n' % iterasi)

# %% hasil
idx = fitness_list.index(best_fit)
x1, x2 = populasi[idx].getFenotip()
print('h(x1, x2) = %f' % h(x1, x2))
print('x1 = %f' % x1)
print('x2 = %f' % x2)

# %% tampilkan graph (jalankan jika diperlukan saja)
from matplotlib import pyplot as plt

if rekam_history:
  plt.title('Fitness History')
  plt.xlabel('Generasi')
  plt.ylabel('Fitness')
  plt.plot(fitness_history)
else:
  print('Tidak ada rekaman')
