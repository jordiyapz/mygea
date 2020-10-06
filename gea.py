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

# %% fungsi-fungsi algoritma genetika
def hitungFitness(fungsiFitness, populasi):
  fitness_list = []
  for individu in populasi:
    x1, x2 = individu.getFenotip()
    fit = fungsiFitness(x1, x2)
    fitness_list.append(fit)
  return fitness_list

def hitungPeluang(fitness_list, verbose=False):
  total_fitness = sum(fitness_list)
  peluang_list = list(map(lambda x: x/total_fitness, fitness_list))

  return peluang_list

def printTabel(populasi, fitness_list, peluang_list, verbose=2):
  if verbose > 1:
    print('x1', 'x2', 'fitness', 'peluang', 'kromosom', sep='\t')
    for individu, fit, peluang in zip(populasi,
                                      fitness_list,
                                      peluang_list):
      x1, x2 = individu.getFenotip()
      print('%.2f' % x1, '%.2f' % x2,
            '%.2f' % fit,
            '%.2f' % peluang,
            individu.kromosom,
            sep='\t')
  if verbose > 0:
    print('fitness: %.2f' % max(fitness_list))

def rouletteWheel(peluang_list):
  r = rand()
  batas = 0
  for idx, p in enumerate(peluang_list):
    batas += p
    if r < batas:
      return idx

def seleksiOrtu(peluang_list):
  banyak_pasangan = len(peluang_list) // 2
  return [(rouletteWheel(peluang_list),
           rouletteWheel(peluang_list))
          for _ in range(banyak_pasangan)]

def pindahSilang(pasangan):
  tipot = floor(rand() * (len(pasangan[0].kromosom) - 1)) + 1
  k1 = pasangan[0].kromosom[:tipot] + pasangan[1].kromosom[tipot:]
  k2 = pasangan[1].kromosom[:tipot] + pasangan[0].kromosom[tipot:]
  return (k1, k2)

def mutasi(populasi, peluang_mutasi=.03):
  for i in populasi:
    if (rand() < peluang_mutasi):
      posisi = floor(rand() * len(i.kromosom))
      i.kromosom[posisi] = (i.kromosom[posisi] + 1) % 2

def urutanPopulasi(populasi, fitness_list):
  urutan_list = sorted(range(len(fitness_list)), key=lambda i: fitness_list[i])
  urutan_list.reverse()
  populasi_terurut = [populasi[urutan] for urutan in urutan_list]
  return populasi_terurut