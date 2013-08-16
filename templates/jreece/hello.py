from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import json
import random
import playground
import prototype

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/base')
def base_page():
    return 'base page'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/input')
def form_write():
    return render_template('input.html')

@app.route('/output', methods=['GET', 'POST'])
def output():
	data = request.json
	idarr = [] 
	for i in data:
		if 'scenario' in i:
			id = str(random.randrange(0,1000000))
			prototype.ascefWrite('ascef-1.5.5', data['model'], playground.df(data[i], playground.r), id)
			idarr.append(id)
	print jsonify(something="hello", id=id)
	return jsonify(something="hello", id=idarr)
	#render_template('output.html', something=data)

@app.route('/output2', methods=['GET', 'POST'])
def output2():
	baz = request.form.to_dict()
	return render_template('output2.html', thing2=baz)

@app.route('/scenform')
def index():
	return render_template('jreece/scenform.html')

@app.route('/scenformcopy')
def whatev():
	return render_template('jreece/experimental/scenformcopy.html')

@app.route('/forms')
def form():
	arb = request.form
	return render_template('forms.html', formthing=arb)

@app.route('/rdcep')
def rdcep():
	return render_template('rdcep-style.html')

if __name__ == '__main__':
    app.run(debug=True)

# Remember: you must enter virtualenv to do all this stuff. Type '. /venv/bin/activate'