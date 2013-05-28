from flask import render_template, request, make_response
from uwsgi_app import app
from cimearth.dat_to_json import DataTable
from conf.web   import select_menu, checkboxes

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = ';khfdalhalyjlahflhvlva'

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/prices/region')
# def prices_region():
#     return render_template('prices/region.html')
#
# @app.route('/prices/commodity')
# def prices_commodity():
#     return render_template('prices/commodity.html')

@app.route('/json/region/<dtype>/<reg>/<com>')
@app.route('/json/commodity/<dtype>/<reg>/<com>')
def json2(dtype, reg, com):
    _data = DataTable(dtype)
    _data.panelize()
    return _data.json_output(
        regions=reg.split(','), commodities=com.split(',')
    )

@app.route('/<dataset>/<cmap>')
def prices_region(dataset, cmap):
    if cmap == 'region':
        item = 'commodity'
    else:
        item = 'region'
    cmap2 = cmap
    if dataset == 'emission_flows':
        item = 'region'
        cmap2 = 'commodity'
    menu, default_menu_name, default_menu_code = select_menu(item)
    checks, default_check_name, default_check_code = checkboxes(cmap, cmap2)

    if dataset == 'prices':
        graph_title = 'Change in prices'
        y_unit = '%%'
    elif dataset == 'emissions':
        graph_title = 'Emissions'
        y_unit = 'unit'
    elif dataset == 'emission_flows':
        graph_title = 'Emissions Flow'
        y_unit = 'unit'

    default_region = None
    default_item = None
    if cmap == 'region':
        default_region = default_check_code
        default_item = default_menu_code
    elif cmap == 'commodity':
        default_region = default_menu_code
        default_item = default_check_code

    return render_template(
        'line_graph.html',
        menu=menu,
        default_title=default_menu_name,
        default_region=default_region,
        default_item=default_item,
        checks=checks,
        dataset=dataset,
        cmap=cmap2,
        graph_title=graph_title,
        y_unit=y_unit,
    )

# @app.route('/emissions/region')
# def emissions_region():
#     return render_template('emissions/region.html')
#
# @app.route('/emissions/commodity')
# def emissions_commodity():
#     return render_template('emissions/commodity.html')
#
# @app.route('/emission_flows/region')
# def emission_flows_region():
#     return render_template('emission_flows/region.html')
#
# @app.route('/emission_flows/commodity')
# def emission_flows_commodity():
#     return render_template('emission_flows/commodity.html')


if __name__ == '__main__':
    app.run()