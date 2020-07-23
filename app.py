from flask import Flask, render_template
from flask import request
from flask_table import Table, Col
import json
import time
from modules import rowItem
import gevent
import logging
import http.client


connection = http.client.HTTPSConnection("swapi.dev")

app = Flask(__name__)

class ItemTable(Table):
    """
    Display Table Layout
    """
    classes = ['table', 'table-striped', 'table-bordered', 'table-condensed']
    name = Col('Name')
    gender = Col('Gender')
    speciesName = Col('Species Name')
    averagelifeSpan = Col('Average Lifespan')
    homePlanet = Col('home Planet')
    movieList = Col('Movies')

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def homeDirectory():
    return render_template('homeSearch/index.html')


@app.route('/search')
def searchByName():
    """
    Search function triggered by the search button
    :return: Table string with content
    """
    startTime = time.time()
    name = request.args.get("name")

    ## Validate that name is given and not empty
    if name is None or name == "":
        return render_template('homeSearch/index.html', notfound="Enter a value")
    connection.request('GET', '/api/people/?search=' + name)
    matchList = json.loads(connection.getresponse().read().decode())
    logging.info("Character JSON fetched")

    ## Checks if no records were found
    if matchList["count"] == 0:
        logging.info("No Recrod was found")
        return render_template('homeSearch/index.html', notfound="No Matches found")

    ## Result list
    customizedList = []
    threads = [gevent.spawn(rowItem.ListItem, i) for i in matchList["results"]]
    gevent.joinall(threads)
    [customizedList.append(thread.value) for thread in threads]
    logging.info("Customized List Created")

    logging.info("Over all Execution time : %s", time.time() - startTime)
    return render_template('homeSearch/result.html', table=ItemTable(customizedList))


if __name__ == '__main__':
    app.run()
