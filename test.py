import re
import json
import pandas as pd
import numpy as np


class CimEarthData(object):
    def __init__(self, _file, start_year=2004):
        with open('./data/%s.dat' % _file) as f:
            _data = f.read()
            _data = re.sub(r'^ +', '', _data)
            _data = re.sub(r'\n +', '\n', _data)
            _data = re.sub(r'[ \t]+', ',', _data)
            _data = re.sub(r'\n+$', '', _data)
        data_segments = _data.split('\n\n')
        frames = {}
        col_names = []
        multi_count = {}
        self.dims = 3
        multi_new = False
        multi_prev = 0
        multi_frames = {}
        N = 0

        for i in range(len(data_segments)):
            rows = data_segments[i].split('\n')
            _index = ''
            data_items = []
            for j in range(len(rows)):
                row = rows[j].split(',')
                if i == 0 and j == 0:
                    N = len(row)
                    col_names = row[1:]
                row += [np.nan] * (N - len(row))
                if j == 0:
                    try:
                        _index = str(int(row[0]) + start_year)
                    except ValueError:
                        self.dims = 4
                        _index = str(row[0])
                        try:
                            multi_count[_index] += 1
                            if multi_count[_index] > multi_prev:
                                multi_prev += 1
                                multi_new = True
                            else:
                                multi_new = False
                        except KeyError:
                            multi_count[_index] = 0
                else:
                    data_items.append((
                        row[0], np.array(row[1:], dtype=np.float64)
                    ))
            if self.dims == 4 and multi_new:
                multi_frames[str(start_year + multi_prev)] = (
                    pd.Panel(frames).transpose(2, 0, 1)
                )
                frames = {}
            frames[_index] = (pd.DataFrame.from_items(
                data_items, orient='index', columns=col_names
            ))

        if self.dims == 4:
            self.panel = pd.Panel4D(multi_frames).transpose(2, 1, 0, 3)
        else:
            self.panel = pd.Panel(frames).transpose(2, 0, 1)

    def JsonOut(self, reg1=False, reg2=False, com1=False, com2=False):
        if (reg1 or reg2 or com1 or com2) is False:
            print 'Need to choose 1 or 2 regions, and 1 or 2 commodities.'
        else:
            data = {}
            regions = [reg1, reg2]
            commodities = [com1, com2]
            print regions, commodities
            for i in range(len(regions)):
                data['region'+str(i)] = {'name': regions[i]}
                for j in range(len(commodities)):
                    try:
                        this_data = self.panel[regions[i]][commodities[j]]
                        _region = data['region'+str(i)]
                        _region['commodity'+str(j)] = {
                            'name': commodities[j],
                            'data': this_data.T.tolist(),
                        }
                    except KeyError:
                        data['region'+str(i)]['commodity'+str(j)] = False
            return json.dumps(
                data, indent=None, separators=(',', ':')
            )

if __name__ == "__main__":
    ratio = CimEarthData('ratio')
    price = CimEarthData('price')
    json = price.JsonOut(reg1='USA', reg2='RUS', com1='OIL')
    print json