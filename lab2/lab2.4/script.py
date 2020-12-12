from pymongo import *
from datetime import datetime
import time

def insert(collection, regist):
    inserted_id = collection.insert_one(regist).inserted_id
    print("Inserted with success: " + str(inserted_id) + "\n")

def change(collection, regist, update):

    collection.update_many(regist, update)
    print("Changed with success!")

def search(collection, regist):
    lst = collection.find(regist)
    print("\nFound " + str(lst.count()) + " Results\n")
    return lst


def newIndex(collection, index, n):
    collection.create_index(index, name = n)

def countLocalidades(collection):
    result = collection.aggregate([{"$group": {"_id": "$localidade"}}])
    length = len(list(result))
    print("Number of locations: " + str(length))

def countRestByLocalidade(collection):
    result = collection.aggregate([{"$group": {"_id": "$localidade", "num_restaurants": {"$sum": 1}}}])
    mapa = {}
    for d in list(result):
        mapa[d[("_id")]] = d["num_restaurants"]

    return mapa

def countRestByLocalidadeByGastronomia(collection):
    result = collection.aggregate([{"$group": {"_id": {"localidade": "$localidade","gastronomia": "$gastronomia"}, "num_restaurants": {"$sum": 1}}}])
    mapa = {}
    for d in list(result):
        mapa[str(d["_id"]["localidade"]) + " | " + str(d["_id"]["gastronomia"])] = d["num_restaurants"]
    
    return mapa

def getRestWithNameCloserTo(collection, name):
    result = collection.aggregate([{"$match": {"nome": {"$regex": name}}}])
    lst = []
    for d in list(result):
        lst.append(str(d["nome"]))

    return lst

def main(db):

    #insert test
    insert(db["rest"], {"address": {"building": "43566", "coord": [65.4, 43.56], "rua": "Bairro de Santiago", "zipcode": "3750-314"}, 
                        "localidade": "Aveiro", 
                        "gastronomia": "gast", 
                        "grades": [ {"date": datetime(2019, 7, 11, 1, 1), "grade": "B", "score": 70}, 
                                    {"date": datetime(2020, 1, 1, 2, 2), "grade": "A", "score": 115}],
                        "nome": "Bastos", 
                        "restaurant_id": "4523430"})

    #change test
    change(db["rest"], {"localidade": "Aveiro"},{"$set": {"rua": "Changed Rua"}})

    #indexes test
    print("\nWithout indexes:")
    t0 = time.time()
    search(db["rest"], {"localidade": "Bronx"})
    t1 = time.time()
    print("Elapsed time: " + format(t1 - t0, ".10f"))
    
    newIndex(db["rest"], "localidade", "localidade")
    newIndex(db["rest"], "gastronomia", "gastronomia")
    newIndex(db["rest"],[("nome",TEXT)],"nome")

    print("\nWith indexes:")
    t0 = time.time()
    search(db["rest"], {"localidade": "Bronx"})
    t1 = time.time()
    print("Elapsed time: " + format(t1 - t0, ".10f"))

    print("\n")

    #Number of locations
    countLocalidades(db["rest"])

    #Number of restaurants by location
    print("\nNumero de restaurantes por localidade:")
    mapa = countRestByLocalidade(db["rest"])
    for key in mapa:
        print(str(key) + " -> " + str(mapa.get(key)))

    #Number of restaurants by location and gastronomy
    print("\nNumero de restaurantes por localidade e gastronomia:")
    mapa = countRestByLocalidadeByGastronomia(db["rest"])
    for key in mapa:
        print(str(key) + " -> " + str(mapa.get(key)))
   
    #Get name closer to
    print("\nNome de restaurantes contendo 'Park' no nome:")
    lst = getRestWithNameCloserTo(db["rest"], "Park")
    for x in lst:
        print("> " + x)

if __name__ == '__main__':
    CLIENT = MongoClient()
    db = CLIENT["cbd"]
    main(db)