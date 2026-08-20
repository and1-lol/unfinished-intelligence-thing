import json

# Define your data structure
data = {
    "python": {
        "year": "1991",
        "founder": "Van Russo",
        "_is_a" : "programming language",
        "code" : [0, 0, 0]
    },
    "javascript": {
        "year" : "1995",
        "founder": "Brendan Eich",
        "_is_a": "programming language",
        "code": [1, 0, 0]
    },
    "kenadian": {
        "_is_a": "youtuber",
        "code": [0, 1, 0]
    },
    "programming language": {
       "definition": "How computers are told to do stuff",
       "code": [0, 0, 1]
    },
    "youtuber": {
      "definition": "The term for someone who posts on youtube",
      "code": [1, 1, 0]
    },
}

# Write to a file named 'config.json'
with open("config.json", "w") as f:
    json.dump(data, f, indent=4)
