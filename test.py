import pickle

var = pickle.dumps(['hej'])

var2 = pickle.loads(var)

print(type(var2))