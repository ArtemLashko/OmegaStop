from flask import Flask, render_template
from flask import request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')

# A route to return a next move 1
@app.route('/api/v1/suggest_move', methods=['GET'])
def api_all():
    print(request.args)
    if 'fen' in request.args:
        fen = str(request.args['fen'])
    else:
        return -1
    return "test"


if __name__ == '__main__':
    app.run()
