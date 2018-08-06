import json
import os
import math


class Chronicle(object):
    def __init__(self):
        self.data = {}


    def isEmpty(self):
        return (len(self.data.keys()) <= 0)

    
    def write(self, filePath: str):
        with open(filePath, 'w', encoding='utf-8') as cFile:
            cFile.write(json.dumps(self.data, indent=4))


    def htmlExport(self, filePath: str):
        htmlString = ''
        sheets = math.ceil(len(self.data.keys()) / 25) # Max 25 years to a sheet

        htmlString += '<div class="wrapper">\n\t<section class="paper">\n'
        htmlString += '\t\t<h1>The Chronicle of REPLACE_ME</h1>\n'
        htmlString += '\t\t<h3 class="span">This is the chronicle of REPLACE_ME, in which is contained a true and accurate record of it\'s fortunes, glories, and difficulties.</h3>\n\n'

        counter = 0
        for key, year in self.data.items():
            htmlString += '\t\t<section class="date">\n\t\t\t<h2>- {0} -</h2>\n'.format(key)
            for entry in year:
                htmlString += '\t\t\t\t<p>{0}</p>\n'.format(entry['entry'])
            htmlString += '\t\t</section>\n\n'
            counter += 1

            if counter >= 25:
                htmlString += '\t</section>\n</div>\n\n<div class="wrapper">\n\t<section class="paper">\n'
                counter = 0
        htmlString += '\t</section>\n</div>'
        with open(filePath, 'w', encoding='utf-8') as htmlFile:
            htmlFile.write(htmlString)


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