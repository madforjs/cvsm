import cgi
import io
import glob
import os
import json
from bottle import route, run, template, post, request
from requests import get

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

stop_words = []
files = []
fcontent = {}
fildoclist = []
filwords =[]
pptokens =[]
c_dict = {}

def stopWords(words):
    stop_words = stopwords.words('english')
    for w in words:
        stop_words.append(w)
    print(stop_words)
    return stop_words

@post('/sw') # or @route('/login', method='POST')
def do_sw():
    words = request.json['words']
    words = words.split(',')
    print(words)
    global stop_words
    stop_words = stopWords(words)
    str = ','.join(stop_words)
    str = "{'data':'stopwords','words':'" + str + "'}"
    return str

@post('/swget') # or @route('/login', method='POST')
def do_sw():
    global stop_words
    str = ','.join(stop_words)
    str = "{'data':'stopwords','words':'" + str + "'}"
    return str

@route('/exec/upload', method='POST')
def do_upload():
    global files
    global fcontent
    files = request.files.getall('files')
    print(request.files)
    for f in files:
        fcontent[f.filename] = f.file.read()
    print(fcontent)
    return "Upload success"

@route('/exec/pp', method='POST')  
def do_pp():
    global stop_words
    global fcontent
    global fildoclist
    c = 0
    for file_name in fcontent:
        # Tokenization
        word_tokenize_list = word_tokenize(fcontent[file_name])
        # Stop word Removal
        filteredfilename = "filtered_docs" + "/" + "filter%d.txt" % c
        fildoclist.append(os.path.basename(filteredfilename))
        file2 = open(filteredfilename,'w+')
        for r in word_tokenize_list:
            if not r in stop_words:
                file2.write(r.lower()+" ")
        file2.close()
        collect_tokens(c)
        c+=1
    return "Preprocess sucesss"
    
def collect_tokens(c):
    global fildoclist
    global pptokens
    global filwords
    for f_file_name in fildoclist:
        f_fi = open(f_file_name,'r')
        f_file_content = f_fi.read()
        tokens = f_file_content.split()
        uniquetokens = []
        for i in tokens:
            if i not in uniquetokens:
                uniquetokens.append(i)
        # add each token to pptokens list
        filwords.append(uniquetokens)
        for i in uniquetokens:
            if i not in pptokens:
                pptokens.append(i)
    print(pptokens)

def generating_concepts():
    global pptokens
    global c_dict
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
    print (c_dict)
    return c_dict

### Localhost process
run(host='localhost', port=3000, debug=True)