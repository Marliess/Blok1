import itertools

def RI():
    with open("label.txt","r") as r:
        Rlabel = [word.split()[0] for word in r]
    with open("cluster.txt","r") as c:
        Cluster = [word.strip() for word in c]

    data = list()
    for i in range(len(Rlabel)):
        data.append((Rlabel[i],Cluster[i]))
    #print(data)
    
    TP = 0
    FP = 0
    FN = 0
    TN = 0

    for i in range(1):
        for x,y in itertools.combinations(data,2):
            if x[0] == y[0] and x[1] == y[1]:
                TP += 1
            if x[0] != y[0] and x[1] == y[1]:
                FP += 1
            if x[0] == y[0] and x[1] != y[1]:
                FN += 1
            if x[0] != y[0] and x[1] != y[1]:
                TN += 1

    print('TP:',TP,'FP:',FP,'FN:',FN,'TN:',TN)
    RI = (TP+FP)/(TP+FP+FN+TN)
    print(RI)

RI()

