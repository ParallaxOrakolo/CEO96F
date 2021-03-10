import json


def readJson(json_to_read):
    with open(json_to_read, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def writeJson(json_local_save, json_data ):
    with open("json_local_save", "w", encoding='utf-8') as jsonFile:
        json.dump(json_data, jsonFile, indent=4)

