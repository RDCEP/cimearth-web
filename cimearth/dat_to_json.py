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
            ('prices', 'price'),
            ('prices2', 'price'),
            ('emissions', 'emissions'),
            ('emission_flows', 'emission_flows'),
            ('expend_sector', 'expend'),
            ('expend_region_import', 'expend'),
            ('expend_sector_import', 'expend'),
            ('ratio_sector', 'ratio'),
            ('ratio_region_import', 'ratio'),
            ('ratio_sector_import', 'ratio'),
        )
        _f = [v[1] for i,v in enumerate(file_type_map) if v[0] == data_table][0]
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

    @property
    def expend_sector(self):
        self.panelize()


    def panelize(self):
        panels = self.get_panel_list()
        frames = {}
        col_names = []
        multi_count = {}
        multi_new = False
        multi_prev = 0
        multi_frames = {}
        N = 0
        for i in range(len(panels)):
            year_index = ''
            data_items = []
            for j in range(len(panels[i])):
                _r = panels[i][j]
                if i == 0 and j == 0:
                    N = len(_r)
                    col_names = _r[1:]
                if j > 1 and (len(_r) > len(panels[i][j-1])):
                    split = [
                        len(panels[i][j-1]), j
                    ]
                _r += [np.nan] * (N - len(_r)) # only for fucked up tables
                if j == 0:
                    try:
                        year_index = str(int(_r[0]) + self.start_year)
                    except ValueError:
                        self.dims = 4
                        year_index = str(_r[0])
                        try:
                            multi_count[year_index] += 1
                            if multi_count[year_index] > multi_prev:
                                multi_prev += 1
                                multi_new = True
                            else:
                                multi_new = False
                        except KeyError:
                            multi_count[year_index] = 0
                else:
                    data_items.append((
                        _r[0], np.array(_r[1:], dtype=np.float64)
                    ))
            if self.dims == 4 and multi_new:
                multi_frames[str(self.start_year + multi_prev)] = (
                    pd.Panel(frames).transpose(1, 0, 2)
                )
                frames = {}
            frames[year_index] = (pd.DataFrame.from_items(
                data_items, orient='index', columns=col_names
            ))
        if self.dims == 4:
            self.panel = pd.Panel4D(multi_frames).transpose(0, 2, 3, 1)
            if self.data_table in ['expend_sector', 'ratio_sector']:
                self.panel = self.panel.ix[:, :, :26, :30]
            if self.data_table in ['expend_sector_import', 'ratio_sector_import']:
                self.panel = self.panel.ix[:, :, :26, 30:]
            if self.data_table in ['expend_region_import', 'ratio_region_import']:
                self.panel = self.panel.ix[:, :, 26:, 30:]
        else:
            self.panel = pd.Panel(frames).transpose(2, 0, 1)

    def json_output2(self, items=(), minors=(), majors=None):
        data = []
        _reg_sectors = itertools.product(items, minors)
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

    def json_output(self, regions=(), commodities=()):
        if len(regions) == 0 or len(commodities) == 0:
            raise Exception(
                'Need to choose 1 or 2 regions, and 1 or 2 commodities.'
            )
        else:
            if self.data_table in ['expend_sector', 'ratio_sector']:
                self.panel = self.panel.ix[:26, :30]
            if self.data_table in ['expend_sector_import', 'ratio_sector_import']:
                self.panel = self.panel.ix[:26, 30:]
            if self.data_table in ['expend_region_import', 'ratio_region_import']:
                self.panel = self.panel.ix[26:, 30:]
            data = []
            _reg_sectors = itertools.product(regions, commodities)
            for region in regions:
                for commodity in commodities:
                    if self.dims == 3:
                        data.append({
                            'region': region,
                            'commodity': commodity,
                            'data_table': self.data_table,
                            'data': list(
                                # self.panel.loc[commodity, :, region].values
                                self.panel.loc[region, :, commodity].values
                            ),
                        })
                    elif self.dims == 4:
                        data.append({
                            'region': region,
                            'commodity': commodity,
                            'data_table': self.data_table,
                            'data': list(
                                self.panel.loc[region, :, commodity, commodity]
                                .T
                            ),
                        })
            return json.dumps(
                data, indent=' ',
            )


if __name__ == '__main__':
    c = DataTable('expend_sector')
    c.panelize()
    print c.panel