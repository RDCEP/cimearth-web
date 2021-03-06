from flask import render_template, request, make_response
from uwsgi_app import app
from cimearth.dat_to_json import DataTable
from conf.web import CimEarthWebParser

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = ';khfdalhalyjlahflhvlva'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/json/<_set>/<_table>/<_item>/<_minor>')
def json3(_set, _table, _item, _minor):
    _data = DataTable(_table, _data_set=_set)
    return _data.json_output2(
        items=_item.split(','), minors=_minor.split(',')
    )

@app.route('/json/<_set>/<_table>/<_item>/<_minor>/<_major>')
def json4(_set, _table, _item, _minor, _major):
    _data = DataTable(_table, _data_set=_set)
    return _data.json_output2(
        items=_item.split(','), minors=_minor.split(','), majors=_major.split(',')
    )

@app.route('/<data_set>/<data_table>/<check_type>')
def line_graph(data_set, data_table, check_type):
    parser = CimEarthWebParser(data_table)
    _c = None
    _s = []
    for k, v in parser.vectors.iteritems():
        if v[0] != check_type or _c is not None:
            try:
                _s.append(parser.select_menu(v, k))
            except:
                pass
        else:
            _c = parser.checkboxes(v, k)
            check_axis = k
    title, unit = parser.get_graph_info(data_table)
    return render_template(
        'line_graph.html',
        menus=_s,
        checks=[_c],
        vector_info=parser.default_vector,
        check_axis=check_axis,
        data_set=data_set,
        data_table=data_table,
        title=title,
        unit=unit,
    )


if __name__ == '__main__':
    app.run()