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
    game="notfound"
    if 'game' in request.args:
        game = str(request.args['game'])
    else:
        return "Error: No id field provided. Please specify an id."
    return str(len(game))


if __name__ == '__main__':
    app.run()
