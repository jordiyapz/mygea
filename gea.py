# %% import
from math import floor
from random import random as rand
import enum
from utils import *

# %% enumerasi
class Stop(enum.Enum):
  MAX_IT = 0      # always on, stop when max iteration reached
  TRESHOLD = 1    # stop if fitness >= treshold value
  NO_IMPROVE = 3  # stop if no improvement for certain generation

# %% classes
class Individu:
  def __init__(self,
                ranges:tuple=((0,1),(0,1)),
                resolusi:int=5,
                kromosom:list=None):

    assert type(ranges) is tuple
    for rg in ranges:
      assert len(rg) is 2

    self.kromosom = kromosom or \
        [round(rand()) for _ in range(resolusi * len(ranges))]
    self.res = resolusi
    self.ranges = ranges

  def getFenotip(self):
    l = self.res
    up = 2**l-1
    return tuple(translate(toDecimal(self.kromosom[l*i:l*(i+1)]),
                                      0, up, ran[0], ran[1]) \
                  for i, ran in enumerate(self.ranges))

class Gea:
  def __init__(self,
               fungsi_fitness:callable,
               ranges:tuple,
               resolusi:int,
               ukuran_populasi=50):

    for rg in ranges:
      assert len(rg) is 2

    self.fungsi_fitness = fungsi_fitness
    self.resolusi = resolusi
    self.ranges = ranges
    self.ukuran_populasi = ukuran_populasi
    self.reset()

  def reset(self):
    self.best_individu = (None, 0)
    self.fitness = 0
    self.populasi = [Individu(self.ranges, self.resolusi)
                     for _ in range(self.ukuran_populasi)]

  def __hitungFitness(self):
    fitness_list = []
    for individu in self.populasi:
      fenotip = individu.getFenotip()
      fit = self.fungsi_fitness(fenotip)
      fitness_list.append(fit)
    return fitness_list

  def __hitungPeluang(self, fitness_list, verbose=False):
    total_fitness = sum(fitness_list)
    peluang_list = list(map(lambda x: x/total_fitness, fitness_list))
    return peluang_list

  def __printTabel(self, fitness_list, peluang_list, verbose=2):
    if verbose > 2:
      print('fen', 'fitness', 'peluang', 'kromosom', sep='\t')
      for individu, fit, peluang in zip(self.populasi,
                                        fitness_list,
                                        peluang_list):
        fen = individu.getFenotip()
        print(tuple('%.2f' % f for f in fen),
              '%.2f' % fit,
              '%.2f' % peluang,
              individu.kromosom,
              sep='\t')
    print('fitness: %.2f' % max(fitness_list))

  def __rouletteWheel(self, peluang_list):
    r = rand()
    batas = 0
    for idx, p in enumerate(peluang_list):
      batas += p
      if r < batas:
        return idx

  def __seleksiOrtu(self, peluang_list, banyak_pasangan):
    return [(self.__rouletteWheel(peluang_list),
            self.__rouletteWheel(peluang_list))
            for _ in range(banyak_pasangan)]

  def __pindahSilang(self, pasangan):
    tipot = floor(rand() * (len(pasangan[0].kromosom) - 1)) + 1
    k1 = pasangan[0].kromosom[:tipot] + pasangan[1].kromosom[tipot:]
    k2 = pasangan[1].kromosom[:tipot] + pasangan[0].kromosom[tipot:]
    return (k1, k2)

  def __mutasi(self, peluang_mutasi):
    for individu in self.populasi:
      if (rand() < peluang_mutasi):
        posisi = floor(rand() * len(individu.kromosom))
        individu.kromosom[posisi] = (individu.kromosom[posisi] + 1) % 2

  def __urutanPopulasi(self, populasi, urutan):
    urutan_list = sorted(range(len(urutan)), key=lambda i: urutan[i])
    urutan_list.reverse()
    populasi_terurut = [populasi[urutan] for urutan in urutan_list]
    return populasi_terurut

  def __routineFitPel(self, verbose):
    fitness_list = self.__hitungFitness()
    peluang_list = self.__hitungPeluang(fitness_list)
    best_fit = max(fitness_list)
    if best_fit > self.best_individu[1]:
      self.best_individu = (self.populasi[fitness_list.index(best_fit)],
                            best_fit)

    if verbose:
      if verbose is 1:
        print('*', end='')
      else :
        self.__printTabel(fitness_list, peluang_list, verbose)

    return (best_fit, peluang_list)

  def __routineRegenerasi(self, peluang_list, crossover_rate):
    banyak_pasangan = round((self.ukuran_populasi * crossover_rate) / 2)
    pasangan_index_ortu = self.__seleksiOrtu(peluang_list, banyak_pasangan)

    self.populasi = self.__urutanPopulasi(self.populasi, peluang_list)
    populasi_baru = []

    for pasangan_idx in pasangan_index_ortu:
      pasangan = tuple(self.populasi[idx] for idx in pasangan_idx)
      kromosom_list = self.__pindahSilang(pasangan)
      for kromosom in kromosom_list:
        populasi_baru.append(Individu(self.ranges,
                                      self.resolusi,
                                      kromosom))

    l = len(self.populasi) - len(populasi_baru)
    self.populasi[l:] = populasi_baru

  def fit(self,
          stopping_crit:tuple=(Stop.MAX_IT,),
          maks_generasi:int=200,
          crossover_rate:float=.5,
          peluang_mutasi:float=.03,
          rekam_history:bool=True,
          verbose=1):
    assert crossover_rate >= 0 and crossover_rate <= 1

    iterasi = 0
    fitness_history = []

    if verbose is 1:
      print('Progress: [', end='')

    best_fit, peluang_list = self.__routineFitPel(verbose)


    if rekam_history:
      fitness_history.append(best_fit)


    while iterasi < maks_generasi:

      # mulai mekanisme stopping
      if stopping_crit[0] == Stop.TRESHOLD:
        if best_fit >= stopping_crit[1]:
          # stop iterasi
          break

      elif stopping_crit[0] == Stop.NO_IMPROVE:
        l = len(fitness_history)
        if l > stopping_crit[1]:
          is_improving = False
          for i in range(stopping_crit[1]):
            if fitness_history[l-1-i] != fitness_history[l-i-2]:
              is_improving = True
              break
          if not is_improving:
            # stop iterasi
            break
      # akhir mekanisme stopping

      self.__routineRegenerasi(peluang_list, crossover_rate)
      self.__mutasi(peluang_mutasi)
      best_fit, peluang_list = self.__routineFitPel(verbose)

      if rekam_history:
        fitness_history.append(best_fit)

      iterasi += 1

    if verbose is 1:
      print(']')

    fenotip = self.best_individu[0].getFenotip()

    return (fenotip, iterasi, fitness_history)
# %%
