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
maks_iterasi = 200  # batas apabila treshold tidak terpenuhi

# %% hyper parameter
ukuran_populasi = 50
resolusi = 8
peluang_mutasi = .04
treshold = 200
banyak_pasangan = 17  # harus kurang dari setengah ukuran populasi

# %% fungsi hipothesis dan fitness
def h(x1, x2):
  return cos(x1) * sin(x2) - x1 / (x2**2 + 1)

def fungsiFitness(x1, x2):
  return 1 / (h(x1, x2) + 2)

# %% main
gea = Gea(fungsiFitness, (-1, 2), (-1, 1), resolusi, ukuran_populasi)
result, iterasi, fitness_history = gea.fit(treshold=treshold,
                                           maks_iterasi=maks_iterasi,
                                           banyak_pasangan=banyak_pasangan,
                                           peluang_mutasi=peluang_mutasi,
                                           rekam_history=rekam_history,
                                           verbose=verbosity_level)

x1, x2 = result

print('\nBanyak iterasi: %d\n' % iterasi)
print('fitness = %f' % gea.fitness)
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
