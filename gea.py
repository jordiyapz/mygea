# %% import
from math import cos, sin, floor
from random import random as rand
import functools
from utils import *

# %% class individu
class Individu:
  def __init__(self, kromosom=None, resolusi=5):
    self.kromosom = kromosom or \
        [round(rand()) for _ in range(resolusi*2)]

  def getFenotip(self):
    mid = len(self.kromosom) // 2
    f1 = translate(toDecimal(self.kromosom[:mid]), 0, 2**mid-1, -1, 2)
    f2 = translate(toDecimal(self.kromosom[mid:]), 0, 2**mid-1, -1, 1)
    return (f1, f2)

class Gea:
  def __init__(self, fungsiFitness, resolusi, ukuran_populasi=50):
    self.fungsiFitness = fungsiFitness
    self.populasi = [Individu(resolusi=resolusi)
                     for _ in range(ukuran_populasi)]
    self.fitness = 0

  def __hitungFitness(self):
    fitness_list = []
    for individu in self.populasi:
      x1, x2 = individu.getFenotip()
      fit = self.fungsiFitness(x1, x2)
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

  def __seleksiOrtu(self, peluang_list):
    banyak_pasangan = len(peluang_list) // 2
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
          treshold=200,
          maks_iterasi=200,
          banyak_pasangan=17,
          peluang_mutasi=.03,
          rekam_history=True,
          verbose=2):
    iterasi = 0
    fitness_history = []

    fitness_list = self.__hitungFitness()
    peluang_list = self.__hitungPeluang(fitness_list)
    best_fit = max(fitness_list)

    if rekam_history:
      fitness_history.append(best_fit)

    if verbose:
      self.__printTabel(fitness_list,
                        peluang_list,
                        verbose=verbose)

    while iterasi < maks_iterasi and best_fit < treshold:
      # print('Generasi: %d' % i)
      pasangan_index_ortu = self.__seleksiOrtu(peluang_list)

      # regenerasi
      self.populasi = self.__urutanPopulasi(self.populasi, fitness_list)
      populasi_baru = []

      for pasangan_idx in pasangan_index_ortu[:min(
          banyak_pasangan, len(pasangan_index_ortu))]:
        pasangan = tuple(self.populasi[idx] for idx in pasangan_idx)
        k1, k2 = self.__pindahSilang(pasangan)
        populasi_baru.append(Individu(k1))
        populasi_baru.append(Individu(k2))

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