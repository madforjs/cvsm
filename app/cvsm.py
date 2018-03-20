def generating_concepts(pptokens):
    c_dict = {}
    for word in pptokens:
        synonyms = []
        synunique = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())
        for i in synonyms:
            if i not in synunique:
                synunique.append(i)
        c_dict[word] = synunique
    return c_dict

def weightedMatrix(conceptsdict, fildoclist):
    wmatrix = []
    for i in conceptsdict:
        a = []
        #print(i)
        for j in fildoclist:
            f = open("filtered_docs"+"/"+j,'r')
            #print(f)
            ftokens = f.read().split()
            value,wvalue,wfreq,svalue,sfreq,count = 0,0,0,0,0,0
            if i in ftokens:
                wvalue = 1
                wfreq = ftokens.count(i)
                count = count+1
            for s in conceptsdict[i]:
                if s in ftokens:
                    svalue = svalue+1
                    sfreq = sfreq+ftokens.count(s)
                    count = count+1
            value = (wfreq*1)+(sfreq*0.5)
            if(count==0):
                count = 1
            a.append(value/count)
            f.close()
        wmatrix.append(a)
    return wmatrix

def doc_doc_matrix(concepts, docs,a):
    b = np.zeros(shape=(docs,docs))
    for i in range(docs):
        for j in range(docs):
            if(i==j):
                b[i,j] = -1
            elif(b[i,j]==0):
                m=0
                for x in range(concepts):
                    m = m+(a[x,i]*a[x,j])
                b[i,j] = m
                b[j,i] = m
            else:
                n=1
    return b


def binary_matrix(docs,b):
    c = np.zeros(shape=(docs,docs))
    threshold = 0
    thr = 0
    nt = 0
    for i in range(docs):
        for j in range(docs):
            if(i<j):
                thr = thr + b[i,j]
                nt = nt + 1
    threshold = thr/nt
    #print(threshold)
    for i in range(docs):
        for j in range(docs):
            if(i==j):
                c[i,j] = -1
            elif(b[i,j]>=threshold):
                c[i,j] = 1
            else:
                c[i,j] = 0
    return c

def cliques(docs, c):
    m=docs-1
    i=0
    j=0 #class count
    classes = {}
    while(i!=m):
        #f3
        #print(i)
        classes[j] = []
        classes[j].append(i)
        r=i+1
        k=i+1
        #print('k',k)
        while(1):
            #f1
            count = 0
            #if(k<=m):
            for x in classes[j]:
                #print('x',x)
                if(c[k,x]==1):
                    count=count+1
                else:
                    break
            if(count == len(classes[j])):
                classes[j].append(k)
            #
            #print(classes)
            k=k+1
            if(k>m):
                r=r+1
                if(r!=m):
                    k=r
                    j=j+1
                    classes[j] = []
                    classes[j].append(i)
            #f1
            if(k>m and r==m):
                 #f2
                 if(classes[j] == [i]):
                     #print('*')
                     del(classes[j])
                 #i=i+1
                 break
            if(k>m):
                break
        i,j = i+1,j+1
    clusterslist = []
    for key in classes:
        clusterslist.append(classes[key])
    return(clusterslist)

def simplify(l):
    i = 0
    while i < len(l):
        s = set(l[i])
        for x in range(len(l)):
            if x == i: continue
            if s <= set(l[x]):
                l.pop(i)
                i -= 1
                break
        i += 1
    return l