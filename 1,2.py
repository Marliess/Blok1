import pickle
import sys


def read_lines(sys):
    print("Please enter the key: ")
    docs = pickle.load(open('docs.pickle','rb'))
    for zin in sys.stdin:
        if zin in docs.keys():
            sys.stdout(zin)



if __name__ == "__main__":
    read_lines(sys)
