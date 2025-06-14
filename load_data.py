import json


def load_closedTraverse_test_data():
    with open("./data/closedTraverse_test_data.json", 'r') as f:
        data = json.load(f)
        return data

def load_user_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
        return data