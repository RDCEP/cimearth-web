import yaml
import HTMLParser
import re

htmlp = HTMLParser.HTMLParser()
YAML = file('./conf/variables.yaml', 'r')
CONF_FILE = yaml.load(YAML)
YAML.close()

def checkboxes(dtype, ntype=None):
    if ntype is None:
        ntype = dtype
    dataset = CONF_FILE[dtype]
    _default_name = None
    _default_code = None
    html = '<h4>%s</h4>' % (ntype[:1].upper() + ntype[1:])
    for data in dataset:
        tag = '<input type="checkbox" name="%s" id="%s_%s" value="%s"' % (
            ntype, dtype, data['code'], data['code']
        )
        try:
            if data['default']:
                _default_name = data['name']
                _default_code = data['code']
                tag += ' checked'
        except KeyError:
            pass
        tag += '>\n'
        tag += '<label for="%s_%s">%s</label><br>\n' % (
            ntype, data['code'], data['name']
        )
        html += tag
    return [html, _default_name, _default_code]

def select_menu(dtype, ntype=None):
    if ntype is None:
        ntype = dtype
    dataset = CONF_FILE[dtype]
    _default_name = None
    _default_code = None
    html = '<h4>%s</h4>' % (ntype[:1].upper() + ntype[1:])
    html += '<select id="%s" name="%s" class="data_select">\n' % (
        ntype, ntype
    )
    for data in dataset:
        tag = '<option value="%s"' % data['code']
        try:
            if data['default']:
                _default_name = data['name']
                _default_code = data['code']
                tag += ' selected'
        except KeyError:
            pass
        tag += '>%s</option>\n' % data['name']
        html += tag
    html += '</select>\n'
    return [html, _default_name, _default_code]
