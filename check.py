def VIP():
    endscore = 0
    for line in open("matrix_test.csv","r"):
        already_followed_VIPs = []
        line = line.split()
        for lines in open("matrix_training.csv","r"):
            lines = lines.split()
            if line[0] == lines[0]:
                already_followed_VIPs.append(lines[1])  # VIPs which the user (of matrix_test) already follows

        value = []
        for word in already_followed_VIPs:
            for popular in open("popular_similarity.csv","r"):
                pop = popular.split()
                if word == pop[0]:
                    popu = [pop[1],pop[2]]
                    value.append(popu)
                if word == pop[1]:
                    popu = [pop[0],pop[2]]
                    value.append(popu)
            sorted_values = sorted(value,key=lambda x: float(x[1]),reverse=True)[0:150]   #VIPs that are most similar to VIPs which the user already follows
        #print('VIPs that are most similar to already_followed_VIPs of:',line[0],':',sorted_values ,'\n')

        VIPs_not_followed_yet = []
        for list in sorted_values:
            if list[0] not in already_followed_VIPs:                #check if user already follows this VIP
                if list[0] not in VIPs_not_followed_yet:
                    VIPs_not_followed_yet.append(list[0])
        #print("Word:",line[0],"similar VIP's:",VIPs_not_followed_yet)

        if line[1] in VIPs_not_followed_yet[0:10]:
            score = 1
        else:
            score = 0 
        print(line[0], line[1], VIPs_not_followed_yet[0:10],score,'\n')     
        endscore = endscore + score
    print(endscore)



VIP()
