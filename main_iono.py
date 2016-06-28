#IONO

from pyevolve import *
import math
import random

error_accum = Util.ErrorAccumulator()
fitness = 0

# This is the functions used by the GP core,
# Pyevolve will automatically detect them
# and the they number of arguments
def gp_add(a, b): return a+b
def gp_sub(a, b): return a-b
def gp_mul(a, b): return a*b
#def gp_sqrt(a):   return math.sqrt(abs(a))
def gp_div(a, b): 
   if b==0:
      return a
   else:
      return a/b
#def gp_exp(a): return math.exp(a)
#def gp_leq(a, b): return a<=b
#def gp_geq(a, b): return a>=b
#def gp_and(a, b): return a and b
#def gp_or(a, b): return a or b
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

def eval_func(chromosome):
   global error_accum
   global fitness
   error_accum.reset()
   code_comp = chromosome.getCompiledCode()

   const = random.random()

   archivo = open("IONO.data","r")

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
      c25 = float(datos[24])
      c26 = float(datos[25])
      c27 = float(datos[26])
      c28 = float(datos[27])
      c29 = float(datos[28])
      c30 = float(datos[29])
      c31 = float(datos[30])
      c32 = float(datos[31])
      c33 = float(datos[32])
      c34 = float(datos[33])
      

      evaluated = eval(code_comp)
      target = float(datos[34])
      error_accum += (target, evaluated)

   archivo.close()

   if fitness==0 or error_accum.getRMSE()<=fitness:
      fitness = error_accum.getRMSE()

   return error_accum.getRMSE()

   #for a in xrange(0, 5):
   #   for b in xrange(0, 5):
         # The eval will execute a pre-compiled syntax tree
         # as a Python expression, and will automatically use
         # the "a" and "b" variables (the terminals defined)
   #      evaluated     = eval(code_comp)
   #      target        = math.sqrt((a*a)+(b*b))
   #      error_accum += (target, evaluated)
   #return error_accum.getRMSE()

def step_callback(gp_engine):
   if gp_engine.getCurrentGeneration() == 4:
      GTree.GTreeGP.writePopulationDot(gp_engine, "trees.jpg", start=0, end=1)

def main_run():
   global fitness
   genome = GTree.GTreeGP()
   genome.setParams(max_depth=5, method="ramped")
   genome.evaluator.set(eval_func)

   ga = GSimpleGA.GSimpleGA(genome)
   ga.stepCallback.set(step_callback)
   # This method will catch and use every function that
   # begins with "gp", but you can also add them manually.
   # The terminals are Python variables, you can use the
   # ephemeral random consts too, using ephemeral:random.randint(0,2)
   # for example.
   ga.setParams(gp_terminals       = [ 'const', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10',
                                       'c11', 'c12', 'c13', 'c14', 'c15', 'c16', 'c17', 'c18', 'c19', 'c20',
                                       'c21', 'c22', 'c23', 'c24', 'c25', 'c26', 'c27', 'c28', 'c29', 'c30',
                                       'c31', 'c32', 'c33', 'c34'],
                gp_function_prefix = "gp")
   # You can even use a function call as terminal, like "func()"
   # and Pyevolve will use the result of the call as terminal
   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setGenerations(5)
   ga.setMutationRate(0.08)
   ga.setCrossoverRate(1.0)
   ga.setPopulationSize(50)
   ga.evolve(freq_stats=5)

   print ga.bestIndividual()
   print fitness

if __name__ == "__main__":
   main_run()