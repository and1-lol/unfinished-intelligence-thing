import math
import json
import random

words = {
    'A': [0,1,0],
    'B': [1,0,1],
    'C': [1,0,0]
}

trains = [
    ([1,0,1], 1),
    ([0,1,0], 0),
    ([1,1,0], 1),
    ([0,0,1], 0),
    ([0,0,0], 0),
    ([1,1,1], 1)
]

trainb = [
    ([0,1,1], 0),
    ([0,1,0], 1),
    ([1,0,1], 0),
    ([1,0,0], 1),
    ([1,1,1], 0),
    ([0,0,0], 1)
]

weights = [
    [23.078551015018338, 0.6704272542401032, 0.6704216602177436],
    [1.010446383998694, 0.660461878567308, -0.314526985129531],
    [2.1084463839986936, -0.21553812143824308, 0.33947301487046905],
    [1.5534463839986938, 0.561461878567308, -0.659526985129531],
    [2.774446383998694, -0.8815381214326921, 1.0054730148704691],
    [1.9854463839986938, 0.040461878558981354, -0.049526985135082115],
    [-0.6765356785427771, -0.6765348978384128, -23.076113011471566],
    [-0.6460668004337061, -0.6460659218195626, -23.089527667758542],
    [-0.6432012639504885, -0.6432003631398238, -23.09075406866647]
]

bias = [
    -12.005813217247425,
    -1.1285097056958926,
    -0.11550970569695468,
    -1.3505097056909847,
    -0.32750970569229926,
    -1.9065097056698515,
    12.011012935568914,
    11.985718111296482,
    11.98331999454279
]

poland = []
austria = []

rate = 0.5
act = 0 #neuron count for system
cmd = None #Set Mode

def check(bias, act):

  for exe in range(200001):
    if act <= 5:
     for val, exp in trains:
      result = neuron(val, act)
      error = exp - result
      for e in range(len(weights[act])):
        we2 = None
        we2 = weights[act]
        we2[e] += rate * error * val[e]

      bias[act] += rate * error

      if exe % 200000 == 0 and exe != 0:
        print(f"{act} > {exe} iteration: {error} << {weights[act]} << {bias[act]} <<")

    if act > 5:
     for val, exp in trainb:
      result = neuron(val, act)
      error = exp - result
      for e in range(len(weights[act])):
        we2 = None
        we2 = weights[act]
        we2[e] += rate * error * val[e]

      bias[act] += rate * error

      if exe % 200000 == 0 and exe != 0:
        print(f"{act} > {exe} iteration: {error} << {weights[act]} << {bias[act]} <<")

  act += 1
  if act < 9: #based on total neurons
    check(bias, act)

def neuron(inputt, act):
    output = 0
    output3 = 0
    for i in range(len(inputt)):
      we = None
      we = weights[act]
      output += inputt[i] * we[i]

    output += bias[act]
    output3 = 1 / ((2.718 ** (output * -1)) + 1)

    return output3

def values(value):
  inputs = [0, 0, 0]

  for a in value:
    if a in words:
      b = words[a]
      for c in range(len(b)):
        inputs[c] += b[c]

  betterinputs = []

  for d in inputs:
      betterinputs.append(0 if d % 2 == 0 else 1)

  list1 = betterinputs

  return list1

def think(act, poland, austria):
  o = input("Input: ").upper()
  p = o.split()

  for _ in range(3):
    hello1 = values(p)
    hello2 = neuron(hello1, act)
    if hello2 is not None:
      poland.append(hello2)
    act += 1

  for _ in range(3):
      hello3 = neuron(poland, act)
      if hello3 is not None:
        austria.append(hello3)
      act += 1

  for _ in range(1): #New layers
    for _ in range(3):
      hello3 = neuron(austria, act)
      del austria[0]
      if hello3 is not None:
        austria.append(hello3)
      act += 1

  final = 0
  ins = 0
  for f in austria:
    ins += 1
    if f > final:
      final = f
      finish = f"Number {ins}: {f}"

  print(f"{austria}")
  print(f"{finish}")


if cmd is None:
  think(act, poland, austria)

else:
  check(bias, act)
