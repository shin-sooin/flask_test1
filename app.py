from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/', methods={'POST','GET'})
def index():  # put application's code here
    if request.method == 'GET':
        t='GET'
        id = str(request.args.get('id'))
    elif request.method == 'POST':
        t='POST'
        id = str(request.form['id'])
    result = {
        'info': id,
        'summary': t,
        'error': 'connect testing'}
    return jsonify(result)

if __name__ == '__main__':
    app.run()
