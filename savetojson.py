import json


def save_to_json(data, file="data.json"):
    with open(file, "w") as file:
        json.dump(data, file, indent=4)
    print(data)
