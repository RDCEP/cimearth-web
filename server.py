from flask import render_template, request, make_response
from uwsgi_app import app
from cimearth.dat_to_json import DataTable

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = ';khfdalhalyjlahflhvlva'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prices/region')
def prices_region():
    return render_template('prices/region.html')

@app.route('/prices/commodity')
def prices_commodity():
    return render_template('prices/commodity.html')

@app.route('/json/region/<dtype>/<reg>/<com>')
@app.route('/json/commodity/<dtype>/<reg>/<com>')
def json2(dtype, reg, com):
    _data = DataTable(dtype)
    _data.panelize()
    return _data.json_output(
        regions=reg.split(','), commodities=com.split(',')
    )

if __name__ == '__main__':
    app.run()