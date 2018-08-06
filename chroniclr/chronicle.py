import json
import os


class Chronicle(object):
    def __init__(self):
        self.data = {}


    def isEmpty(self):
        return (len(self.data.keys()) <= 0)

    
    def write(self, filePath: str):
        with open(filePath, 'w', encoding='utf-8') as cFile:
            cFile.write(json.dumps(self.data, indent=4))


    def load(self, filePath: str):
        with open(filePath, 'r', encoding='utf-8') as cFile:
            tdata = json.loads(cFile.read())
        for tyear in tdata:
            self.data[int(tyear)] = tdata[tyear]



    def addYear(self, year: int):
        if year in self.data:
            return False
        else:
            self.data[year] = []
            return True


    def removeYear(self, year: int):
        if not year in self.data:
            return False
        else:
            self.data.pop(year)
            return True


    def addEntry(self, year: int, entry: str):
        if not year in self.data:
            return False
        else:
            self.data[year].append({
                'id': len(self.data[year]),
                'entry': entry
            })
            return True


    def removeEntry(self, year: int, id: int):
        if not year in self.data:
            return False
        else:
            for e in self.data[year]:
                if e['id'] == id:
                    self.data[year].remove(e)
                    return True
            return False