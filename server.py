from flask import Flask, request, jsonify

from main import process1, process2


app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome'})

@app.route('/process1', methods=['POST'])
def run_process1():
    data = request.get_json()
    result = process1(data)
    return jsonify(result)

@app.route('/process2', methods=['POST'])
def run_process2():
    data = request.get_json()
    result = process2(data)
    return jsonify(result)