#GC 

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
def gp_div(a, b): 
   if b==0:
      return a/math.pow(10,-50)
   else:
      return a/b
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

   archivo = open("GC.data","r")

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
      c15 = float(datos[14])
      c16 = float(datos[15])
      c17 = float(datos[16])
      c18 = float(datos[17])
      c19 = float(datos[18])
      c20 = float(datos[19])
      c21 = float(datos[20])
      c22 = float(datos[21])
      c23 = float(datos[22])
      c24 = float(datos[23])
      
      evaluated = eval(code_comp)
      target = float(datos[24])
      error_accum += (target, evaluated)

   archivo.close()

   if fitness==-1 or error_accum.getRMSE()<=fitness:
      fitness = error_accum.getRMSE()
      best_const = const

   return error_accum.getRMSE()

def step_callback(gp_engine):
   if gp_engine.getCurrentGeneration() == 49:
      GTree.GTreeGP.writePopulationDot(gp_engine, "trees_gc.jpg", start=0, end=1)

def main_run():
   global fitness
   global best_const
   genome = GTree.GTreeGP()
   genome.setParams(max_depth=5, method="ramped")
   genome.evaluator.set(eval_func)

   ga = GSimpleGA.GSimpleGA(genome)
   ga.stepCallback.set(step_callback)
   sqlite_adapter = DBAdapters.DBSQLite(identify="exgc")
   ga.setDBAdapter(sqlite_adapter)
   
   ga.setParams(gp_terminals       = [ 'const', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10',
                                       'c11', 'c12', 'c13', 'c14', 'c15', 'c16', 'c17', 'c18', 'c19', 'c20',
                                       'c21', 'c22', 'c23', 'c24'],
                gp_function_prefix = "gp")
   
   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setGenerations(50)
   ga.setMutationRate(0.08)
   ga.setCrossoverRate(1.0)
   ga.setPopulationSize(1000)
   ga.evolve(freq_stats=5)

   print ga.bestIndividual()
   print 'Fitness mejor individuo'
   print fitness
   print 'Valor constante'
   print best_const

if __name__ == "__main__":
   main_run()