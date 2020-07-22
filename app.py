from flask import Flask, render_template
from flask import request
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/search')
def searchByName():
    name = request.args.get("name")
    if name is None:
        return render_template('homeSearch/index.html')
    matchList = requests.get('https://swapi.dev/api/people/?search='+name).json()
    print(name)
    print(matchList)
    return render_template('homeSearch/index.html')


if __name__ == '__main__':
    app.run()
