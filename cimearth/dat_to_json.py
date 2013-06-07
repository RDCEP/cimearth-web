import re
import zipfile
import itertools
import simplejson as json
import pandas as pd
import numpy as np


class DataFile(object):
    def __init__(self, data_table, _data_set='BAU', start_year=2004):
        Z = zipfile.ZipFile('./data/%s.zip' % _data_set)
        file_type_map = (
            ('prices', 'price', None),
            ('prices2', 'price', None),
            ('emissions', 'emissions', None),
            ('emission_flows', 'emission_flows', None),
            ('expend_sector', 'expend', 'top_left'),
            ('expend_region_import', 'expend', 'bottom_right'),
            ('expend_sector_import', 'expend', 'bottom_left'),
            ('ratio_sector', 'ratio', 'top_left'),
            ('ratio_region_import', 'ratio', 'bottom_right'),
            ('ratio_sector_import', 'ratio', 'bottom_left'),
        )
        _f, self.triple_position = [v[1:] for i,v in enumerate(file_type_map) if v[0] == data_table][0]
        _data = Z.read('%s.dat' % _f)
        _data = re.sub(r'^ +', '', _data) # Kill initial whitespace
        _data = re.sub(r'\n +', '\n', _data) # Kill end of line whitespace
        _data = re.sub(r'[ \t]+', ',', _data) # Spaces to commas
        _data = re.sub(r'\n+$', '', _data) # Kill end of file whitespace
        self._data = _data
        self.start_year = start_year
        self.dims = 3
        self.data_table = data_table

    def get_panel_list(self):
        # data_segments = _data.split('\n\n')
        return [[[cell for cell in row.split(',')] for row in panel.split('\n')] for panel in self._data.split('\n\n')]


class DataTable(DataFile):
    def grouper(self, iterable, n, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
        args = [iter(iterable)] * n
        return itertools.izip_longest(fillvalue=fillvalue, *args)

    def get_triple_panel(self, position):
        vs0, vs1, hs0, hs1 = 1, 31, 1, 27
        if position == 'bottom_left':
            vs0, vs1, hs0, hs1 = 31, 47, 1, 27
        elif position == 'bottom_right':
            vs0, vs1, hs0, hs1 = 31, 47, 27, 43
        groups = self.grouper([
            [
                [c for c in np.array(r.split(','))[range(0, 1) + range(hs0, hs1)]] for r in np.array(p.split('\n'))[range(0, 1) + range(vs0, vs1)]
            ] for p in sorted(
                sorted(
                    self._data.split('\n\n'),
                    key=lambda x: int(x.split('\n')[0].split(',')[-1])  # Sort by year
                ),
                key=lambda x: x.split('\n')[0].split(',')[0]  # Sort by region
            )
        ], 21)
        panels = {}
        for group in groups:
            g = np.array(group)
            panels[g[0, 0, 0]] = pd.Panel(
                g[:, 1:, 1:].astype(np.float64),
                items=[y + self.start_year for y in range(len(group))],
                major_axis=g[0, 1:, 0],
                minor_axis=g[0, 0, 1:],
            )
        return pd.Panel4D(
            panels
        ).transpose(1, 0, 2, 3)

    def get_simple_panel(self):
        group = [
            [
                [c for c in np.array(r.split(','))[:]] for r in np.array(p.split('\n'))[:47]
            ] for p in self._data.split('\n\n')
        ]
        g = np.array(group)
        return pd.Panel(
            g[:, 1:, 1:].astype(np.float64),
            items=[y + self.start_year for y in range(len(group))],
            minor_axis=g[0, 0, 1:], #horiz
            major_axis=g[0, 1:, 0], #vert
        ).transpose(2, 0, 1)

    def json_output2(self, items=(), minors=(), majors=None):
        if majors is not None:
            self.panel = self.get_triple_panel(self.triple_position)
            self.dims = 4
        else:
            self.panel = self.get_simple_panel()
            self.dims = 3
        data = []
        # _reg_sectors = itertools.product(items, minors)
        for item in items:
            for minor in minors:
                if self.dims == 3:
                    data.append({
                        'item': item,
                        'minor': minor,
                        'data_table': self.data_table,
                        'data': list(
                            # self.panel.loc[commodity, :, region].values
                            self.panel.loc[item, :, minor].values
                        ),
                    })
                if self.dims == 4:
                    for major in majors:
                        data.append({
                            'item': item,
                            'minor': minor,
                            'major': major,
                            'data_table': self.data_table,
                            'data': list(
                                # self.panel.loc[commodity, :, region].values
                                self.panel.loc[:, item, major, minor].values
                            ),
                        })
        return json.dumps(
            data, indent=' ',
        )

if __name__ == '__main__':
    pass
    c = DataTable('expend_sector_import')
    print c.get_triple_panel('bottom_left')
    # c = DataTable('prices')
    # print c.get_simple_panel()
    # import timeit
    # print timeit.timeit('c = DataTable("prices");p = c.get_simple_panel()', setup="from __main__ import DataTable", number=50)
    # print timeit.timeit('c = DataTable("prices");p = c.panelize()', setup="from __main__ import DataTable", number=50)
    # print timeit.timeit('c = DataTable("expend_sector_import");p = c.get_triple_panel("bottom_left")', setup="from __main__ import DataTable", number=10)
    # print timeit.timeit('c = DataTable("expend_sector_import");p = c.panelize()', setup="from __main__ import DataTable", number=10)