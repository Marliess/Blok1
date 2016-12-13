def RI():
    with open("testLabel.txt","r") as r:
        Rlabel = [word.strip() for word in r]
    with open("testCluster.txt","r") as c:
        Cluster = [word.strip() for word in c]
    
    data = list()
    for i in range(len(Rlabel)):
        data.append((Rlabel[i],Cluster[i]))
    print(data)
    
    TP = 0
    FP = 0
    FN = 0
    TN = 0
    
    for i in range(len(Rlabel)):
        if Rlabel[i] == Rlabel[i+1] and Cluster[i] == Cluster[i+1]:
            print("TP")
            TP += 1
        if Rlabel[i] != Rlabel[i+1] and Cluster[i] == Cluster[i+1]:
            print("FP")
            FP += 1
        if Rlabel[i] == Rlabel[i+1] and Cluster[i] != Cluster[i+1]:
            print("FN")
            FN += 1
        if Rlabel[i] != Rlabel[i+1] and Cluster[i] != Cluster[i+1]:
            print("TN")
            TN += 1

    #print(TP,FP,FN,TN)
            

    RI = (TP+FP)/(TP+FP+FN+TN)
    print(RI)


RI()
