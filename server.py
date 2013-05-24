from flask import render_template, request, make_response
from uwsgi_app import app
from cimearth.dat_to_json import CimEarthData

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = ';khfdalhalyjlahflhvlva'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/json/<data_type>/<reg1>/<reg2>/<com>')
def json(data_type,reg1, reg2, com):
    _data = CimEarthData(data_type)
    return _data.BetterJsonOut(
        regions=(reg1,reg2), commodities=(com,), data_type=data_type
    )

if __name__ == '__main__':
    app.run()