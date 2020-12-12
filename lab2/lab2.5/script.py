from pymongo import *
from pymongo.mongo_client import MongoClient
import re
import datetime

# db: rest
# collection: movies

def getMoviesNames(collection, limit):
    return [m for m in collection.find({}, {"_id": 0, "title": 1}).limit(limit)]

def getMovie(collection, name, limit):
    rgx = re.compile('.*' + name + '.*', re.IGNORECASE)  # compile the regex
    return [m for m in collection.find({"title": rgx}).limit(limit)]

def getMovieGenCast(collection, genre, cast):
    return [m for m in collection.find({'genres': genre, "cast": cast})]

def getMovieRatingReleased(collection, rating, date):
    return [m for m in collection.find({'imdb.rating': {"$gt": rating}, "released": {"$gt": date}})]

def getMovieNotGenAwardsSortYear(collection, genre, wins, order):
    return [m for m in collection.find({'genres': {"$ne": genre}, "awards.wins": {"$gt": wins}}).sort("year", order)]

def getMovieVotesNominations(collection, minVotes, maxVotes, nominations):
    return [m for m in collection.find({"$and": [  {"imdb.votes": {"$gt": minVotes}}, {"imdb.votes": {"$lt": maxVotes}}, {"awards.nominations": {"$eq": nominations}}]})]

def getMoviesByCountry(collection):
    return [m for m in collection.aggregate([ {"$group": {"_id": '$rated', "sum_movies": {"$sum": 1}}}])]

def getMoviesByAvgRating(collection, sort):
    return [m for m in collection.aggregate([{"$group": {"_id": '$year',  "avg_rating" :  {"$avg" : '$imdb.rating'}}}, {"$sort": {"avg_rating": sort}}]) ]

def getMoviesByDirectorsWithOnlyNames(collection):
    return [m for m in collection.aggregate([ {"$project": {"directors": 1}}, {"$group": {"_id": "$directors"}} ])]

def getMoviesWithLang(collection, rating):
    return [m for m in collection.aggregate([{"$unwind": "$poster"}, {"$match": {"imdb.rating": {"$gt": rating}}}])]

def getMoviesNotRated(collection):
    return [m for m in collection.aggregate([{"$match": {"rated": "NOT RATED"}}, {"$group": {"_id": "$year"}}, {"$count": "num"}])]

def getMoviesRating(collection, rating):
    return [m for m in collection.aggregate([{"$match": {"imdb.rating": {"$gt": rating}}}, {"$group": {"_id": "$imdb.rating", "sum": {"$sum": 1}}}])]

def getSumAwardWins(collection):
    return [m for m in collection.aggregate([{"$group": {"_id": "$genres", "sum": {"$sum": "$awards.wins"}} }])]

def getNumMoviesByWriterBetweenYears(collection, minYear, maxYear):
    return [m for m in collection.aggregate([{"$match": {"year": {"$gt": minYear, "$lt": maxYear}}}, {"$group": {"_id": "$countries", "num": {"$sum": 1} }}])]



def main(db, collection, limit):

    # REMOVE COMMENTS TO SEE RESULTS

    #All names
    movies = getMoviesNames(collection, limit)
    #for m in movies:        
    #    print("> ", m["title"])

    #Get movies with a specific name
    movies = getMovie(collection, "this", limit)
    #for m in movies:
    #    print("> ", m["title"])

    #Get movies by genres and cast
    movies = getMovieGenCast(collection, "Adventure", "Wallace Beery")
    #for m in movies:
    #    print("> ", m["title"], " | ", m["genres"], " | ", m["cast"])

    #Get movies with higher rating and released date than given
    movies = getMovieRatingReleased(collection, 8.9, datetime.datetime.strptime("2000-10-18T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z"))
    #for m in movies:
    #    print("> ", m["title"], " | ", m["imdb"]["rating"], " | ", m["released"])

    #Get movies without the genre given and with more wins than given, in normal or reversed order
    movies = getMovieNotGenAwardsSortYear(collection, "Drama", 100, 1)
    #for m in movies:
    #    print("> ", m["title"], " | ", m["year"], " | ", m["genres"], " | ", m["awards"]["wins"])

    #get movies with min and max votes and x nominations
    movies = getMovieVotesNominations(collection, 200, 400, 10)
    #for m in movies:
    #    print("> ", m["title"], " | ", m["imdb"]["votes"], " | ", m["awards"]["nominations"])

    #Get movies by state
    movies = getMoviesByCountry(collection)
    #for m in movies:
    #    print("> ", m["_id"], " | ", m["sum_movies"])

    #Get movies grouped by year and sorted by avg rating
    movies = getMoviesByAvgRating(collection, -1)
    #for m in movies:
    #    print("> ", m["_id"], " | ", m["avg_rating"])

    #Get only the directors of the movies grouped by directors 
    movies = getMoviesByDirectorsWithOnlyNames(collection)
    #for m in movies:
    #    print("> ", m["_id"])

    #Get only the movies with posters != none and greater than given rating
    movies = getMoviesWithLang(collection, 9)
    #for m in movies:
    #    print("> ", m["title"])

    #Get number of years with not rated movies
    movies = getMoviesNotRated(collection)
    #print("> ", movies[0]["num"])

    #Get sum of movies with id greater than given
    movies = getMoviesRating(collection, 9)
    #for m in movies:
    #    print("> ", m["_id"], " | ", m["sum"])

    #Get sum of wins in each genre
    movies = getSumAwardWins(collection)
    #for m in movies:
    #    print("> ", m["_id"], " | ", m["sum"])

    #Get num of movies of each country between given dates
    movies = getNumMoviesByWriterBetweenYears(collection, 1920, 1940)
    #for m in movies:
    #    print("> ", m["_id"], " | ", m["num"])
    
if __name__ == '__main__':
    CLIENT = MongoClient()
    db = CLIENT["rest"]
    collection = db["movies"]
    main(db, collection, limit=1000)