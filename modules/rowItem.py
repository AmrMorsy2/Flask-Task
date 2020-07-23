import time
import http.client
import json
import concurrent.futures
import logging

connection = http.client.HTTPSConnection("swapi.dev")

class ListItem(object):
    """
    Custom class for the required display parameters
    """
    def __init__(self, character):
        self.name = character["name"]
        self.gender = character["gender"]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.getSpeciesNameSpan, character["species"])
            self.speciesName, self.averagelifeSpan = future.result()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.getHomePlanet, character["homeworld"])
            self.homePlanet = future.result()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.getMoviesList, character["films"])
            self.movieList = future.result()

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
            speciesStr = "Unknown"
        else:
            speciesStr = speciesStr[2:]
        logging.info("getSpeciesNameSpan Execution time : %s", time.time() - startTime)
        return speciesStr, totalAge

    def getHomePlanet(self, homeWorld):
        startTime = time.time()
        if homeWorld is None or len(homeWorld) == 0:
            return "Unknown"
        connection.request('GET', homeWorld)
        planet = json.loads(connection.getresponse().read().decode())["name"]
        logging.info("getHomePlanet Execution time : %s", time.time() - startTime)
        return planet

    def getMoviesList(self, moviesList):
        startTime = time.time()
        movielist = []
        for i in moviesList:
            connection.request('GET', i)
            curMovie = json.loads(connection.getresponse().read().decode())["title"]
            movielist.append(curMovie)

        logging.info("getMoviesList Execution time : %s", time.time() - startTime)
        return movielist
