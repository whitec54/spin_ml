import json

with open("Women's History.json") as file:
    j = json.load(file)
    print(len(j))
    print(j[0]["topic"])
