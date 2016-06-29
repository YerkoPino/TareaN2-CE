#AUS 

from pyevolve import *
import math
import random

error_accum = Util.ErrorAccumulator()
fitness = -1
best_const = 0

#Funciones
def gp_add(a, b): return a+b
def gp_sub(a, b): return a-b
def gp_mul(a, b): return a*b
def gp_exp(a):
   if a<100:
      return math.exp(a)
   else:
      return math.exp(100)
def gp_if_geq_else(a, b, c, d):
   if a>=b:
      return c
   else:
      return d
def gp_if_leq_else(a, b, c, d):
   if a<=b:
      return c
   else:
      return d

#Fitness
def eval_func(chromosome):
   global error_accum
   global fitness
   global best_const
   error_accum.reset()
   code_comp = chromosome.getCompiledCode()

   const = random.random()

   archivo = open("AUS.dat","r")

   for linea in archivo.readlines():
      datos = linea.split(" ")
      
      c1 = float(datos[0])
      c2 = float(datos[1])
      c3 = float(datos[2])
      c4 = float(datos[3])
      c5 = float(datos[4])
      c6 = float(datos[5])
      c7 = float(datos[6])
      c8 = float(datos[7])
      c9 = float(datos[8])
      c10 = float(datos[9])
      c11 = float(datos[10])
      c12 = float(datos[11])
      c13 = float(datos[12])
      c14 = float(datos[13])
      
      evaluated = eval(code_comp)
      target = float(datos[14])
      error_accum += (target, evaluated)

   archivo.close()

   if fitness==-1 or error_accum.getRMSE()<=fitness:
      fitness = error_accum.getRMSE()
      best_const = const

   return error_accum.getRMSE()

def main_run():
   global fitness
   global best_const
   genome = GTree.GTreeGP()
   genome.setParams(max_depth=5, method="ramped")
   genome.evaluator.set(eval_func)

   ga = GSimpleGA.GSimpleGA(genome)
   sqlite_adapter = DBAdapters.DBSQLite(identify="exaus")
   ga.setDBAdapter(sqlite_adapter)

   ga.setParams(gp_terminals       = [ 'const', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10',
                                       'c11', 'c12', 'c13', 'c14'],
                gp_function_prefix = "gp")

   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setGenerations(50)
   ga.setMutationRate(0.08)
   ga.setCrossoverRate(1.0)
   ga.setPopulationSize(1000)
   ga.evolve(freq_stats=5)

   best = ga.bestIndividual()
   best.writeDotImage("best_aus.jpg")

   print best
   print 'Fitness mejor individuo'
   print fitness
   print 'Valor constante'
   print best_const

if __name__ == "__main__":
   main_run()