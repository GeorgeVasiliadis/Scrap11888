import os
import pickle

def cacheIn(dir, name, data):

    filename = name+".pickle"
    path = "cache"
    path = os.path.join(path, dir)

    os.makedirs(path, exist_ok=True)

    path = os.path.join(path, filename)
    with open(path, "wb") as file:
        pickle.dump(data, file)

def cacheOut(dir, name):

    filename = name+".pickle"
    path = "cache"
    path = os.path.join(path, dir,filename)

    data = None

    if os.path.isfile(path):
        try:
            with open(path, "rb") as file:
                data = pickle.load(file)
        except:
            print("An error has occured while trying to retrieve pickled data.")

    return data
