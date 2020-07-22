import time
import http.client
import json

connection = http.client.HTTPSConnection("swapi.dev")

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
            connection.request('GET', i)
            jsonObj = json.loads(connection.getresponse().read().decode())
            curSpecie = jsonObj["name"]
            age = jsonObj["average_lifespan"]
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
        connection.request('GET', homeWorld)
        planet = json.loads(connection.getresponse().read().decode())["name"]
        print("getHomePlanet Execution time : ", time.time() - startTime)
        return planet

    def getMoviesList(self, moviesList):
        startTime = time.time()
        movielist = []
        for i in moviesList:
            connection.request('GET', i)
            curMovie = json.loads(connection.getresponse().read().decode())["title"]
            movielist.append(curMovie)

        print("getMoviesList Execution time : ", time.time() - startTime)
        return movielist
