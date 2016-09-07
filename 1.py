import pickle

def make_dictio():
    f = open("docs.txt", "r")
    docs = {}
    for line in f:
        line = line.split('\t')
        docs[line[0]] = tuple(line[1::])
    with open('docs.pickle','wb') as p:
        pickle.dump(docs,p)

if __name__ == "__main__":
    make_dictio()
