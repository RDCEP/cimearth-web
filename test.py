import re
import pandas as pd
import numpy as np

_file = 'ratio'
with open('./data/%s.dat' % _file) as f:
    _data = f.read()
    _data = re.sub(r'^ +', '', _data)
    _data = re.sub(r'\n +', '\n', _data)
    _data = re.sub(r'[ \t]+', ',', _data)
    _data = re.sub(r'\n+$', '', _data)

data_segments = _data.split('\n\n')
start_year = 2004
frames = {}
col_names = []
multi_count = {}
multi = False
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
                if not multi:
                    multi = True
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
            data_items.append((row[0], row[1:]))

    if multi and multi_new:
        multi_frames[str(start_year + multi_prev)] = (
            pd.Panel(frames).transpose(2, 0, 1)
        )
        frames = {}
    frames[_index] = (
        pd.DataFrame.from_items(data_items, orient='index', columns=col_names)
    )

if multi:
    panel = pd.Panel4D(multi_frames).transpose(2, 1, 0, 3)
else:
    panel = pd.Panel(frames).transpose(2, 0, 1)
print panel.USA