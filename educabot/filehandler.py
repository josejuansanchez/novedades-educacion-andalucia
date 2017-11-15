import os
import json

class FileHandler(object):

    def __init__(self):
        pass

    def exists(self, filepath):
        return os.path.exists(filepath)

    def load_file(self, filepath):
        with open(filepath, 'r') as file:
            data = file.read()
        return data

    def load_json(self, filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)
        return data