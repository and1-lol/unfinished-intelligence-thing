import json
import re
import string
import math

vocab = {
  "python": [1,1,0,1,1,0],
  "javascript": [1,1,0,1,1,1],
  "kenadian": [1,1,1,0,0,0],
  "programming language": [1,1,1,0,0,1],
  "youtuber": [1,1,1,0,0,1],
  "founder": [1,1,1,0,1,0],
  "is": [1,0,0,1,0,1],
  "end": [1,1,1,1,1,1],
  "output": [1,1,1,1,1,0],
  "year": [1,0,0,1,0,0],
  "what": [0, 0, 0, 0, 0, 1],
  "how": [0, 0, 0, 0, 1, 0],
  "why": [0, 0, 0, 0, 1, 1],
  "who": [0, 0, 0, 1, 0, 0],
  "where": [0, 0, 0, 1, 0, 1],
  "when": [0, 0, 0, 1, 1, 0],
  "which": [0, 0, 0, 1, 1, 1],
  "whose": [0, 0, 1, 0, 0, 0],
  "whom": [0, 0, 1, 0, 0, 1],
  "whether": [0, 0, 1, 0, 1, 0],
  "and": [0, 0, 1, 0, 1, 1],
  "but": [0, 0, 1, 1, 0, 0],
  "or": [0, 0, 1, 1, 0, 1],
  "so": [0, 0, 1, 1, 1, 0],
  "because": [0, 0, 1, 1, 1, 1],
  "although": [0, 1, 0, 0, 0, 0],
  "unless": [0, 1, 0, 0, 0, 1],
  "while": [0, 1, 0, 0, 1, 0],
  "since": [0, 1, 0, 0, 1, 1],
  "though": [0, 1, 0, 1, 0, 0],
  "of": [0, 1, 0, 1, 0, 1],
  "to": [0, 1, 0, 1, 1, 0],
  "in": [0, 1, 0, 1, 1, 1],
  "for": [0, 1, 1, 0, 0, 0],
  "on": [0, 1, 1, 0, 0, 1],
  "with": [0, 1, 1, 0, 1, 0],
  "at": [0, 1, 1, 0, 1, 1],
  "by": [0, 1, 1, 1, 0, 0],
  "from": [0, 1, 1, 1, 0, 1],
  "about": [0, 1, 1, 1, 1, 0],
  "through": [0, 1, 1, 1, 1, 1],
  "between": [1, 0, 0, 0, 0, 0],
  "under": [1, 0, 0, 0, 0, 1],
  "against": [1, 0, 0, 0, 1, 0],
  "the": [1, 0, 0, 0, 1, 1],
  "a": [1, 0, 0, 1, 0, 0],
  "an": [1, 0, 0, 1, 0, 1],
  "this": [1, 0, 1, 1, 0, 0],  
  "that": [1, 0, 0, 1, 1, 1],
  "these": [1, 0, 1, 0, 0, 0],
  "those": [1, 0, 1, 0, 0, 1],
  "it": [1, 0, 1, 0, 1, 0],
  "its": [1, 0, 1, 0, 1, 1],
  "they": [1, 0, 1, 1, 0, 0],
  "them": [1, 0, 1, 1, 0, 1],
  "their": [1, 0, 1, 1, 1, 0],
  "is": [1, 0, 1, 1, 1, 1],
  "am": [1, 1, 0, 0, 0, 0],
  "are": [1, 1, 0, 0, 0, 1],
  "was": [1, 1, 0, 0, 1, 0],
  "were": [1, 1, 0, 0, 1, 1]
}

# Define your data structure
data = {
    "python": {
        "definition": "a popular computer language",
        "year": "1991",
        "founder": "Van Russo",
        "_is_a" : "programming language",
        "code" : [1, 0, 0, 0, 0, 0],
    },
    "javascript": {
        "definition": "a popular computer language",
        "year" : "1995",
        "founder": "Brendan Eich",
        "_is_a": "programming language",
        "code": [1, 0, 0, 0, 0, 1],
    },
    "kenadian": {
        "definition": "content creator",
        "_is_a": "youtuber",
        "code": [0, 1, 0, 0, 0, 0],
    },
    "programming language": {
       "definition": "How computers are told to do stuff",
       "code": [1, 0, 0, 0, 1, 0],
    },
    "youtuber": {
      "definition": "someone who posts on youtube",
      "code": [0, 1, 0, 0, 0, 0],
    },
}

ignore = ["if", "what", "of", "a", "an", "and", "is"]

act = 0
count = 0

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

weights2 = [
  [10.803009202493115, 7.741692064928607, -3.9980048891784388],
  [14.820763705375654, -4.120964738645601, -5.950730866885619],
  [9.81092086528214, 7.110834918661597, -3.945579173488027]
]

bias2 = [
  -27.78368730353716,
  -22.849621581435137,
  -25.08207551760522
]

def fileread(file):
  with open(file, "r") as file:
            file_content = file.read()
            content = json.loads(file_content)
  return content

def generate(prev_word, answer, worddef, isa):
  act = 0
  response = []
  toggle = True

  response.append(prev_word)
  vocabulary = fileread('vocab.json')
  
  while toggle:
    prev_val = vocabulary[prev_word]
    word = finder(prev_val)
    if len(response) > 10:
      word = worddef
      toggle = False
    if word == "end":
      toggle = False
    if word == "output":
      if worddef is not None and isa is not None:
        word = f"{worddef} and {isa}"
      elif worddef is not None:
        word = worddef
      elif isa is not None:
        word = isa
      else:
        if isinstance(word, list):
          word = " ".join(word)
        else:
          word = word.strip("[]''")
      toggle = False
    response.append(word)
    prev_word = word
    
  response_final = " ".join(response)
  print(f"{response_final}")
  return

def neuron2(input):
    global act, count
      
    output = 0
    output3 = 0
    for i in range(3):
      we = None
      we = weights2[act]
      output += input[i] * we[i]
    for i in range(3):
      we = None
      we = weights2[act]
      output += input[i + 3] * we[i]

    output += bias2[act]
    output3 = 1 / ((2.718 ** (output * -1)) + 1)

    return output3
    
def finder(value):
  global act
  predictions = {}
  outputs = []
  decimals = []
  vocablist = None
  
  for a in vocab:
    vocablist = vocab[a].copy()
    
    for c in range(len(value)):
      vocablist[c] += value[c]

    betterinputs = []
    for d in vocablist:
      betterinputs.append(0 if d % 2 == 0 else 1)

    result = neuron2(betterinputs)
    predictions[f"{a}"] = f"{result}"
    outputs.append(a)
    decimals.append(result)

  softmax = lambda x: [math.exp(i - max(x)) / sum(math.exp(j - max(x)) for j in x) for i in x] #just staight up stole this :)
  finals = softmax(decimals)
  
  for b in range(len(finals)):
    predictions[f"{outputs[b]}"] = f"{finals[b]}"
    #predictions[f"{outputs[b]}"] = f"{decimals[b]}"

  greatest = 0
  next_word = None
  for c in predictions:
    candid = 0
    candid = predictions[c]
    candid = float(candid)
    if candid > greatest:
      greatest = candid
      next_word = c

  #woah = predictions[next_word]
  #print(f"{next_word}: {woah}")

  if act == 1:
      act = 2
  elif act == 2:
      act = 0
  else:
      act = 1

  return next_word
  
def analyze(file_path, target_phrase1, victor):
    file_content = ""
    fact = None
    fact2 = None
    current_item2 = "APLACEHOLDEr"
    attributeslist = []
    attributeslist2 = []
    target_phrase = []
    worddef = None
    isa = None
  
    try:
        with open(file_path, "r") as file:
            file_content = file.read()
            json_data = json.loads(file_content)
            current_item = json_data
        win = victor - 1
        for item in target_phrase1:
         if target_phrase1[win] != 0:
           target_phrase2 = target_phrase1[win]
           target_phrase.append(target_phrase2)
           break
         else:
           win += 1
           continue
        for w in target_phrase1:
	        target_phrase.append(w)
        if target_phrase2 == "0":
          for object in target_phrase:
            if object != "0":
              target_phrase2 = object

        for a in target_phrase:
             if a in ignore:
                continue
             if a in current_item2:
                fact2 = current_item2[a]
                specs = fact2
                attributeslist.append(fact2)
                attributeslist2.append(fact2)
                continue
             if a in current_item:
                fact = current_item[a]
                attributeslist.append(fact)
                current_item2 = fact
                current_item = fact
                fact4 = None
                if 'definition' in current_item:
                    worddef = current_item['definition']
                if '_is_a' in current_item:
                    fact4pre = current_item['_is_a']
                    fact4 = json_data[fact4pre]
                    isa = fact4['definition']
                    attributeslist.append(fact4)
                if '_sentence' in current_item:
                  setup = current_item['_sentence']

        if attributeslist:
          if fact2 is not None:
            attributeslist = f"{attributeslist2}"
         
          return attributeslist, worddef, isa, target_phrase2

        else:
          print("No response found.")
          return None
          
    except Exception as e:
        print(f"An error occurred during json or a answer might not be known: {e}")
        return None

def parse(terms):
  main = None
  codedex = None
  property1 = False
  newterm = None

  try:
    item = fileread('config.json')

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
      for _ in range(2):
        newterm.append("0")

    else:
      print("No input detected or main term not found in JSON data.")
      return

    return newterm, codedex
    
  except Exception as e:
    print(f"An error occured during parsing: {e}")
    return

def values(value):
  inputs = [0, 0, 0, 0, 0, 0]

  for c in range(len(value)):
    inputs[c] += value[c]

  betterinputs = []

  for d in inputs:
      betterinputs.append(0 if d % 2 == 0 else 1)

  list1 = betterinputs

  return list1

def neuron(inputt, setcheck, act):
    output = 0
    output3 = 0
    austria = []
    poland = []

    for i in range(3):
      we = None
      we = weights[act]
      output += inputt[i] * we[i]
      
    if len(setcheck) < 3:
      for i in range(3):
        we = None
        we = weights[act]
        output += inputt[i + 3] * we[i]

    output += bias[act]
    output3 = 1 / ((2.718 ** (output * -1)) + 1)

    return output3

def think(o):
  global act

  poland = []
  austria = []
  
  for _ in range(3):
    hello1 = values(o)
    hello2 = neuron(hello1, poland, act)
    if hello2 is not None:
      poland.append(hello2)
    act += 1
    
  for _ in range(3):
      hello3 = neuron(poland, poland, act)
      if hello3 is not None:
        austria.append(hello3)
      act += 1

  for _ in range(1): #New layers
    for _ in range(3):
      hello3 = neuron(austria, poland, act)
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
  act = 0
 
  return winner
  
def command(processed):
  
    newterm, codedex = parse(processed)
    print("Request Parsed!")
  
    victor = think(codedex)
    print("Priorities Found!")

    results, worddef, isa, target_phrase2 = analyze("config.json", newterm, victor)
    print("Data Retrieved!")
    
    finish = generate(target_phrase2, results, worddef, isa)
  
def start():
  print("------Ken v.1------")
  #inquiry = inpt("Question: ").lower()
  inquiry = "python"
  process1 = inquiry.translate(str.maketrans('', '',string.punctuation))
  processed = process1.split()

  command(processed)

with open("config.json", "w") as g:
    json.dump(data, g, indent=4)
  
with open("vocab.json", "w") as f:
    json.dump(vocab, f, indent=4)
    
start()
