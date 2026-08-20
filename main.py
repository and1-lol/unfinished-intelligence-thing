import json
import re
import string
import math

ignore = ["if", "what", "of", "a", "an", "and", "is"]

poland = []
austria = []
cmd = "None"
act = 0

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

def analyze_file_for_phrase(file_path, target_phrase, victor):
    file_content = ""
    fact = None
    fact2 = None
    fact4 = None
    current_item2 = "APLACEHOLDEr"
    attributeslist = []

    try:
      with open(file_path, "r") as file:
            file_content = file.read()
            json_data = json.loads(file_content)
            current_item = json_data
      for a in target_phrase:
        if a in ignore:
          continue
        if a in current_item2:
              fact2 = current_item2[a]
              attributeslist.append(fact2)
              continue
        if a in current_item:
            fact = current_item[a]
            current_item2 = fact
            current_item = fact
            fact4 = None
            if '_is_a' in current_item:
                fact4pre = current_item['_is_a']
                fact4 = json_data[fact4pre]

      if fact2 is not None:
              print(f"2: {attributeslist}")
      elif fact4 is not None:
              print(f"4: {fact} {fact4}")
      else:
              print(f"1: {fact}")
    except Exception as e:
        print(f"An error occured during json or a answer might not be known: {e}")
        return

def parse(file_path, terms, act, poland, austria):
  main = None
  codedex = None
  property1 = False
  newterm = None

  try:
    with open(file_path, "r") as file:
            file_content = file.read()
            json_data = json.loads(file_content)
            item = json_data

    for h in terms:
      if h in item:
        main = h
        break

    if main is not None:
      newterm = [main]
      for term_item in terms:
        if term_item != main:
          newterm.append(term_item)
        if 'code' in item[main] and isinstance(item[main]['code'], list):
            codedex = item[main]['code']

    else:
      print("No input detected or main term not found in JSON data.")
      return

    victor = think(codedex, act, poland, austria)

    analyze_file_for_phrase(file_path, newterm, victor)

  except Exception as e:
    print(f"An error occured during parsing: {e}")
    return

def values(value):
  inputs = [0, 0, 0]

  for c in range(len(value)):
    inputs[c] += value[c]

  betterinputs = []

  for d in inputs:
      betterinputs.append(0 if d % 2 == 0 else 1)

  list1 = betterinputs

  return list1

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

def think(o, act, poland, austria):

  for _ in range(3):
    hello1 = values(o)
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
      winner = ins
      finish = f"Number {ins}: {f}"

  return winner

print("------Ken Phase 4/5------")
inquiry = input("Question: ").lower()
process1 = inquiry.translate(str.maketrans('', '', string.punctuation))
word = process1.split()

parse('config.json', word, act, poland, austria)
