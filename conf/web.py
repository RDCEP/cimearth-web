import yaml

YAML = file('./conf/variables.yaml', 'r')
CONF_FILE = yaml.load(YAML)
YAML.close()


class CimEarthWebParser(object):
    def __init__(self, data_table):
        self.default_vector = {}
        self.vectors = self.get_vectors(data_table)

    def checkboxes(self, data_type, vector):
        """
        Build object for HTML checkbox inputs
        ...
        Args
        ----
        data_type: dict(), eg. region, commodity
        vector: str, eg. item, minor, major
        ...
        Returns
        -------
        dict() of checkbox info
        """
        data_set = [t for s in data_type for t in CONF_FILE[s]]
        fieldset = {
            'head': '<h4>%s</h4>' % (
                data_type[0][:1].upper() + data_type[0][1:]
            ),
            'inputs': [],
        }
        for data in data_set:
            tag = {
                'type': 'checkbox',
                'name': vector,
                'id': '%s_%s' % (data_type[0], data['code']),
                'value': data['code'],
                'title': data['name'],
                'checked': False,
            }
            try:
                if data['default']:
                    self.default_vector[vector] = {}
                    self.default_vector[vector]['name'] = data['name']
                    self.default_vector[vector]['code'] = data['code']
                    tag['checked'] = True
            except KeyError:
                pass
            fieldset['inputs'].append(tag)
        return fieldset

    def select_menu(self, data_type, vector):
        """
        Build object for HTML selects
        ...
        Args
        ----
        data_type: dict(), eg. region, commodity
        vector: str, eg. item, minor, major
        ...
        Returns
        -------
        dict() of select info and options
        """
        data_set = [t for s in data_type for t in CONF_FILE[s]]
        fieldset = {
            'head': '<h4>%s</h4>' % (
                data_type[0][:1].upper() + data_type[0][1:].replace('_', ' ')
            ),
            'inputs': {
                'select': {
                    'id': vector,
                    'name': vector,
                    'class': 'data_select',
                },
                'options': [],
            },
        }
        for data in data_set:
            tag = {
                'value': data['code'],
                'html': data['name'],
                'selected': False,
            }
            try:
                if data['default']:
                    self.default_vector[vector] = {}
                    self.default_vector[vector]['name'] = data['name']
                    self.default_vector[vector]['code'] = data['code']
                    tag['selected'] = True
            except KeyError:
                pass
            fieldset['inputs']['options'].append(tag)
        return fieldset

    def get_vectors(self, data_table):
        """
        Build dict of pd.Panel vectors
        ...
        Args
        ----
        data_table: str
        ...
        Returns
        -------
        dict() of vectors, eg. {'item': 'region', 'major': 'commodity',
                                'minor': 'commodity'}
        """
        tables = CONF_FILE['tables']
        defaults = tables['default']['vectors']
        try:
            table_vectors = tables[data_table]['vectors']
        except KeyError:
            table_vectors = {}
        for k, v in defaults.iteritems():
            if k not in table_vectors:
                table_vectors[k] = v
        return table_vectors

    def get_graph_info(self, data_table):
        _dt = CONF_FILE['tables'][data_table]
        return _dt['title'], _dt['unit']
