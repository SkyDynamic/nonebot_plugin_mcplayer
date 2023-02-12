import json
import os

class Config:
    def __init__(self):
        if os.path.exists('./data/mcplayer/data.json') == False:
            os.makedirs('./data/mcplayer/')
            with open('./data/mcplayer/data.json', 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=4)
    
    def read(self) -> dict:
        with open('./data/mcplayer/data.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    def write(self, data):
        with open('./data/mcplayer/data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)