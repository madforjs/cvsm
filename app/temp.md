
pptokens = []
doclist = []
fildoclist = []
conceptsdict = {}
filwords = []

stop_words = stopWords()
pre_processing(stop_words)
conceptsdict = generating_concepts(pptokens)
#Weighted Matrix
wmatrix = weightedMatrix(conceptsdict, fildoclist)
a = np.matrix(wmatrix)
#Document-Document Matrix
concepts = len(conceptsdict)
docs = len(fildoclist)
b = doc_doc_matrix(concepts, docs, a)
#Document-Relationship Matrix
c = binary_matrix(docs,b)
#Cliques Algorithm
clusterslist = cliques(docs, c)
clusters = simplify(clusterslist)
print(clusters)

'''print("List of tokens:")
print(pptokens)
print("\nList of filtered document names:")
print(fildoclist)'''
'''print("\nConcept arrays for all tokens:\n")
#print(conceptsdict)
for item in conceptsdict:
    print(item, conceptsdict[item])
#print("\nAverage Weighted Matrix:")
#print(a)'''
'''print("Document-Document Matrix")
print(b)'''
'''print("Document-Relationship Matrix")
print(c)'''
