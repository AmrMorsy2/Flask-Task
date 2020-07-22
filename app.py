from flask import Flask, render_template
from flask import request
from flask_table import Table, Col
import json
import time
from modules import rowItem
import http.client


connection = http.client.HTTPSConnection("swapi.dev")

app = Flask(__name__)

# Display Table Layout
class ItemTable(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-condensed']
    name = Col('Name')
    gender = Col('Gender')
    speciesName = Col('Species Name')
    averagelifeSpan = Col('Average Lifespan')
    homePlanet = Col('home Planet')
    movieList = Col('Movies')



@app.route('/')
def homeDirectory():
    return render_template('homeSearch/index.html')


# Main search route
# Search function triggered by the search button
@app.route('/search')
def searchByName():
    startTime = time.time()
    name = request.args.get("name")

    if name is None or name == "":
        return render_template('homeSearch/index.html')
    connection.request('GET', '/api/people/?search=' + name)
    matchList = json.loads(connection.getresponse().read().decode())
    print(matchList)
    if matchList["count"] == 0:
        print("NO FOUND TODO ALERT MESSAGE")
        return render_template('homeSearch/index.html', notfound="No Matches found")
    print(matchList)
    print(len(matchList["results"]))
    print("Total found count", len(matchList["results"]))
    customizedList = []
    for i in matchList["results"]:
        customizedList.append(rowItem.ListItem(i))
    endTime = time.time()

    print("Over all Execution time : ", endTime - startTime)
    return render_template('homeSearch/result.html', table=ItemTable(customizedList))


if __name__ == '__main__':
    app.run()
