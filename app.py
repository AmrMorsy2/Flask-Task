from flask import Flask, render_template
from flask import request
from flask_table import Table, Col
import requests
import time

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


## Custom class for the required display items
class ListItem(object):
    # decorators to be applied here
    def __init__(self, character):
        self.name = character["name"]
        self.gender = character["gender"]
        self.speciesName, self.averagelifeSpan = self.getSpeciesNameSpan(character["species"])
        self.homePlanet = self.getHomePlanet(character["homeworld"])
        self.movieList = self.getMoviesList(character["films"])

    def getSpeciesNameSpan(self, speciesList):
        startTime = time.time()
        speciesStr = ""
        totalAge = 0
        for i in speciesList:
            curSpecie = requests.get(i).json()["name"]
            age = requests.get(i).json()["average_lifespan"]
            if age.isnumeric():
                totalAge += int(age)
            speciesStr += ", " + curSpecie
        if totalAge == 0:
            totalAge = "Unknown"
        else:
            totalAge = totalAge / len(speciesList)
        if len(speciesStr) == 0:
            speciesStr = "Unkown"
        else:
            speciesStr = speciesStr[2:]

        print("getSpeciesNameSpan Execution time : ", time.time() - startTime)
        return speciesStr, totalAge

    def getHomePlanet(self, homeWorld):
        startTime = time.time()
        if homeWorld is None or len(homeWorld) == 0:
            return "Unkown"
        planet = requests.get(homeWorld).json()["name"]

        print("getHomePlanet Execution time : ", time.time() - startTime)
        return planet

    def getMoviesList(self, moviesList):
        startTime = time.time()
        movielist = []
        for i in moviesList:
            curMovie = requests.get(i).json()["title"]
            movielist.append(curMovie)

        print("getMoviesList Execution time : ", time.time() - startTime)
        return movielist


@app.route('/')
def homeDirectory():
    return render_template('homeSearch/index.html')


# Main search route
@app.route('/search')

# Search function triggered by the search button
def searchByName():
    startTime = time.time()
    name = request.args.get("name")

    if name is None or name == "":
        return render_template('homeSearch/index.html')
    matchList = requests.get('https://swapi.dev/api/people/?search=' + name).json()

    if matchList["count"] == 0:
        print("NO FOUND TODO ALERT MESSAGE")
        return render_template('homeSearch/index.html', notfound="No Matches found")
    print(matchList)
    print(len(matchList["results"]))
    print("Total found count", len(matchList["results"]))
    customizedList = []
    for i in matchList["results"]:
        customizedList.append(ListItem(i))
    endTime = time.time()

    print("Over all Execution time : ", endTime - startTime)
    return render_template('homeSearch/result.html', table=ItemTable(customizedList))


if __name__ == '__main__':
    app.run()
