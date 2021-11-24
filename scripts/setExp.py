string = "string"
stringSet = set(["string2","string3"])
stringResult = set()

tempSet = set([string])

stringResult = tempSet|stringSet

print(set(stringResult))

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

thisdict["brand"] = set()
thisdict["brand"] = thisdict["brand"]|stringResult

print(set(thisdict["brand"]))

