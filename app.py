from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

global x
x = 'test'

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)