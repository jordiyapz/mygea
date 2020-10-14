# %% import
from math import cos, sin, floor
from random import random as rand
import enum
import functools
from utils import *

# %% enumerasi
class Stop(enum.Enum):
  MAX_IT = 0
  TRESHOLD = 1
  NO_IMPROVE = 3

# %% classes
class Individu:
  def __init__(self,
                range1:tuple=(0,1),
                range2:tuple=(0,1),
                resolusi:int=5,
                kromosom:list=None):
    assert type(range1) is tuple and len(range1) is 2
    assert type(range2) is tuple and len(range2) is 2

    self.kromosom = kromosom or \
        [round(rand()) for _ in range(resolusi*2)]
    self.ranges = (range1, range2)

  def getFenotip(self):
    mid = len(self.kromosom) // 2
    up = 2**mid-1
    f1 = translate(toDecimal(self.kromosom[:mid]),
                   0, up,
                   self.ranges[0][0],
                   self.ranges[0][1])
    f2 = translate(toDecimal(self.kromosom[mid:]),
                   0, up,
                   self.ranges[1][0],
                   self.ranges[1][1])
    return (f1, f2)

class Gea:
  def __init__(self,
               fungsi_fitness:callable,
               range1:tuple,
               range2:tuple,
               resolusi:int,
               ukuran_populasi=50):
    assert type(range1) is tuple and len(range1) is 2
    assert type(range2) is tuple and len(range2) is 2

    self.fungsi_fitness = fungsi_fitness
    self.resolusi = resolusi
    self.ranges = (range1, range2)
    self.ukuran_populasi = ukuran_populasi
    self.reset()

  def reset(self):
    self.fitness = 0
    range1, range2 = self.ranges
    self.populasi = [Individu(range1, range2, self.resolusi)
                     for _ in range(self.ukuran_populasi)]

  def __hitungFitness(self):
    fitness_list = []
    for individu in self.populasi:
      x1, x2 = individu.getFenotip()
      fit = self.fungsi_fitness(x1, x2)
      fitness_list.append(fit)
    return fitness_list

  def __hitungPeluang(self, fitness_list, verbose=False):
    total_fitness = sum(fitness_list)
    peluang_list = list(map(lambda x: x/total_fitness, fitness_list))
    return peluang_list

  def __printTabel(self, fitness_list, peluang_list, verbose=2):
    if verbose > 0:
      print('x1', 'x2', 'fitness', 'peluang', 'kromosom', sep='\t')
      for individu, fit, peluang in zip(self.populasi,
                                        fitness_list,
                                        peluang_list):
        x1, x2 = individu.getFenotip()
        print('%.2f' % x1, '%.2f' % x2,
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
    for i in self.populasi:
      if (rand() < peluang_mutasi):
        posisi = floor(rand() * len(i.kromosom))
        i.kromosom[posisi] = (i.kromosom[posisi] + 1) % 2

  def __urutanPopulasi(self, populasi, fitness_list):
    urutan_list = sorted(range(len(fitness_list)), key=lambda i: fitness_list[i])
    urutan_list.reverse()
    populasi_terurut = [populasi[urutan] for urutan in urutan_list]
    return populasi_terurut

  def fit(self,
          stopping_crit:tuple=(Stop.MAX_IT,),
          maks_generasi:int=200,
          banyak_pasangan:int=17,
          crossover_rate:float=.5,
          peluang_mutasi:float=.03,
          rekam_history:bool=True,
          verbose=2):
    assert crossover_rate >= 0 and crossover_rate <= 1

    iterasi = 0
    fitness_history = []

    fitness_list = self.__hitungFitness()
    peluang_list = self.__hitungPeluang(fitness_list)
    best_fit = max(fitness_list)
    self.fitness = best_fit

    if rekam_history:
      fitness_history.append(best_fit)

    if verbose:
      self.__printTabel(fitness_list,
                        peluang_list,
                        verbose=verbose)

    while iterasi < maks_generasi:
      if stopping_crit[0] == Stop.TRESHOLD:
        if self.fitness >= stopping_crit[1]:
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
            # stop iteration
            break

      banyak_pasangan = round((self.ukuran_populasi * crossover_rate) / 2)
      assert banyak_pasangan < self.ukuran_populasi / 2
      pasangan_index_ortu = self.__seleksiOrtu(peluang_list, banyak_pasangan)

      # regenerasi
      self.populasi = self.__urutanPopulasi(self.populasi, fitness_list)
      populasi_baru = []

      for pasangan_idx in pasangan_index_ortu:
        pasangan = tuple(self.populasi[idx] for idx in pasangan_idx)
        kromosom_list = self.__pindahSilang(pasangan)
        for kromosom in kromosom_list:
          populasi_baru.append(Individu(
            self.ranges[0],
            self.ranges[1],
            self.resolusi,
            kromosom
          ))

      l = len(self.populasi) - len(populasi_baru)
      self.populasi[l:] = populasi_baru
      self.__mutasi(peluang_mutasi)

      # kalkulasi fitness
      fitness_list = self.__hitungFitness()
      best_fit = max(fitness_list)
      self.fitness = best_fit

      if rekam_history:
        fitness_history.append(best_fit)

      if verbose:
        self.__printTabel(fitness_list,
                          peluang_list,
                          verbose=verbose)

      iterasi += 1

    idx = fitness_list.index(best_fit)
    x1, x2 = self.populasi[idx].getFenotip()

    return ((x1, x2), iterasi, fitness_history)
# %%
