# -*- coding: utf-8 -*-
"""

@author: Jonathan Hill
"""
import numpy as np
np.set_printoptions(threshold=np.nan)
import os
import sys
import xmltodict
import pandas as pd
import re
import HTMLParser
from io import open
from nltk.stem.porter import PorterStemmer

localDir = "C:/Users/Jonat/Documents/Machine Learning Courses/WikiProject 2018/"

stopWordsLoc = os.path.join(localDir,"Cleaning\stopwords_twitter.txt")
samplesDir = os.path.join(localDir,"pages")
storedDataFramesDir = os.path.join(localDir,"stored_dataframes")
brokenKeys = []

loadData = True

def checkDirExists(d, s):
        if(d):
            if(os.path.isdir(d)):
                return True
            else:
                print(s+" directory does not exist: "+d)
        else:
            print("empty argument given for "+s)
        return False


def getStopWords(d):
    try:
        newFile = open(d,'r')
        stopWords = np.genfromtxt(newFile,dtype="string",skip_header=1,delimiter="\n")
        newFile.close()
        return stopWords
    except IOError:
        print("IO Error when getting stopwordse")

def getSampleFiles(d):
    try:
        return next(os.walk(d))[2]
    except IOError:
        print("IO Error when getting sample files")

def wordIterator(txt, stopWords, words):
     #only add if not in stopwords
     for s in txt.split():
         if s not in stopWords:
             # add to array
             words = np.append(words, s)
     return words

def getCategories(txt, curid):
    regex = re.compile(r"\[\[Category:.*\]\]")
    try:
        matches = regex.findall(txt)
        categories = []
        if matches:
            for (i,m) in enumerate(matches):
                if matches[i] not in categories:
                    categories.append(re.sub('\[\[Category:', '', matches[i])[:-2]+"\n")
        return categories
    except TypeError: 
        print("error processing: "+str(curid)+"\n\n"+txt)

def getElementValues(s):
    filePath = os.path.join(samplesDir, s)
    try:
        f = open(filePath, encoding="utf8")
        data = re.sub(r"\<\?xml\s+.+\?\>",'',f.read())
        doc = xmltodict.parse(data)
        f.close()
        
        # get text from fields
        title = doc["mediawiki"]["page"]["title"]
        try:
            text = doc["mediawiki"]["page"]["revision"]["text"]["#text"]
            categories = getCategories(text, s[:-4])
        except KeyError:
            AddBrokenKey(s[:-4])
            text = doc["mediawiki"]["page"]["revision"]["text"]
            categories = []

        return [s[:-4],title,text,categories]
    except IOError:
        print("IO Error")
        sysExit()

def AddBrokenKey(k):
    brokenKeys.append(k)

def createSampleFrames(df, save=False, sampleLmit=1000, cols=[], samples=[]):
    if len(samples) < 1 or not isinstance(samples, list):
        print("no samples given")
        # Get list of sample files
        samples = getSampleFiles(samplesDir) if (checkDirExists(samplesDir, "samples")) else sysExit()
        samples = samples[:sampleLmit]
        
    # Go through each sample file and place fields into dataframe
    df = pd.DataFrame(columns=cols)
    df = df.append([pd.Series(data=getElementValues(sample), index=cols) for sample in samples[:sampleLmit]], ignore_index=True)
    if save:
        saveDataFrames(df,"df_xml_"+str(sampleLmit))
    return df

def loadDataFrames(name):
    return pd.read_pickle(os.path.join(storedDataFramesDir,name+".pkl"))

def saveDataFrames(df, name):
    pd.to_pickle(df,os.path.join(storedDataFramesDir,name+".pkl"))

def sysExit():
    sys.exit()
 
def bagOfWords(data=[],stopWords=[],verbose=False,convertToList=None,minFeatureOccurs=1):
    """
    Creates a vocabulary of unique tokens (e.g Words) from entire set of documents.
    Constructs a feature vector from each document that contains the counts of how often each word occurs in a particular document.
    """
    if isinstance(convertToList, int): data = df_ToList(data, convertToList)
    if data is not None and isinstance(data,list):
        from sklearn.feature_extraction.text import CountVectorizer
        count = CountVectorizer(analyzer = 'word', stop_words=frozenset(stopWords),min_df=minFeatureOccurs)
        data = count.fit_transform(data)
        if verbose: print(str(count.vocabulary_)+"\n\n"+str(data.toarray()))
    else: print("data needed to be in list format, bagOfWords")
    return data

def tfidf(data=[],verbose=False):
    # Check if sparse matric
    if type(data).__module__ == "scipy.sparse.csr":
        if data.shape[0] > 0:
            from sklearn.feature_extraction.text import TfidfTransformer
            tfidf = TfidfTransformer(norm='l2')
            data = tfidf.fit_transform(data)
            if verbose:
                np.set_printoptions(precision=2)
                print((data).toarray())
        else:
            print("no data provided")
        return data
    else:
        print("sparse matrix required")
        return data

def cosineMetric(mat):
    # Calculate cosine similarity for entire list of documents. Returns pandas dataframe
    from sklearn.metrics.pairwise import cosine_similarity
    # Perform cosine function for each document
    def performCos(d, mat):
        if type(d).__module__ == type(mat).__module__ == "scipy.sparse.csr":
            d = cosine_similarity(d, mat)
            print(d)
        else:
            print("document needs to be a list and matrix a sparse matrix\n")
            print("doc: "+str(type(d))+"\n"+str(type(mat).__module__ == "scipy.sparse.csr"))
        return d
    
    df = pd.DataFrame(columns=['bow','cos'])
    df = df.append([pd.Series(data=(d,performCos(d,mat)), index=['bow','cos']) for d in mat], ignore_index=True,sort=False)
    return df

def replaceDiag(df, column, val, verbose=False):
    df_all_cosSimilarity_copy = df.copy()
    for name, row in df_all_cosSimilarity_copy.iterrows():
        if name < df_all_cosSimilarity_copy.shape[0]:
            new = np.append(row[column][0][0:name], np.append(np.array([0]),row[column][0][name+1:]))
            if verbose: print(str(new))
            df['cos'][name] = new
    del df_all_cosSimilarity_copy
    return df
    
def df_ToList(df, axis=0):
    """
    Convert dataframe to list format.
    @params:
        axis:   values kept by rows or column
                column = 1, row = 0  
    """
    if axis in xrange(-1,2):
        # Check if scalar given opposed to vector
        if isinstance(df,unicode):
            print("converting unicode type into list\n")
            print(df)
            df = [df] if axis == 0 else df.flatten()
        # vector given
        else:
            df = df.values.T.tolist() if axis == 0 else df.flatten()
    else: print("axis not equal to [0,1]")
    return df
   
def convertASCII(txt):
    return HTMLParser.HTMLParser().unescape(txt)

def stemming(txt, stopWords=[]):
    ps = PorterStemmer()
    txt = txt.split()
    return ' '.join([ps.stem(word) for word in txt if not word in stopWords]) if txt else txt

def removePunctuation(txt, exceptions=[]):
    return re.sub('[^A-Za-z\']',' ',txt.lower())

def sliceStr(s,start,stop,words=True):
    """
    returns reduced string to number of words or letters
    @params:
        s: The string to reduce
        start: beginning string position
        stop: ending string position (number of words or letters)
        words: default True. Otherwise returns reduced string by character positions.
    """
    return re.split(r"(([^\s]+\s){"+str(stop)+"})",s)[1] if words else s[start:stop]

def fill_series_values(row, val):
    print row.name

def main():
    # Get list of stop words
    stopWords = set(getStopWords(stopWordsLoc))
    
    ## Populate a large table of data:
#    
#    
    #sample_size = 5
#    
#    df_xml = loadDataFrames("df_xml_"+str(sample_size)) if loadData else createSampleFrames("df_xml",save=True,sampleSize=sample_size,cols=['curid', 'title', 'text', 'cat'])
#    df_xml = df_xml.set_index('curid')
#    
#    
#    # Create table easier category searching
#    df_xmlCat = df_xml.copy()#.head(100000)
#    df_xmlCat = df_xmlCat.cat.apply(pd.Series).stack().reset_index(level=1,drop=True).to_frame('cat')
#    df_xmlCat['value'] = 1
#    df_xmlCat = df_xmlCat.pivot(columns='cat', values='value')
#    df_xmlCat = ~df_xmlCat.isnull()
#    
#    # Get a list 
#    catOccurences = df_xmlCat[df_xmlCat == 1].count().sort_values(ascending=False).to_frame('occurence')
    
    # Working with two categories: ['Biotechnology','Nanotechnology']
    df_bio = loadDataFrames("(Biotechnology)")
    df_nano = loadDataFrames("(Nanotechnology)")
    
    # Get page information
    sample_limit = 5
    df_bio = createSampleFrames("df_bio",save=True,sampleLmit=sample_limit,cols=['curid', 'title', 'text', 'cat'], samples=df_ToList(df_bio)[0])
    df_nano = createSampleFrames("df_nano",save=True,sampleLmit=sample_limit,cols=['curid', 'title', 'text', 'cat'], samples=df_ToList(df_nano)[0])
    
    # Clean text
    df_bio['text'] = df_bio['text'].apply(convertASCII).apply(removePunctuation).apply(stemming, args=([stopWords]))
    df_nano['text'] = df_nano['text'].apply(convertASCII).apply(removePunctuation).apply(stemming, args=([stopWords]))
    
    # reduce string to get a small set of words to work with
    df_bio['text'] = df_bio['text'].apply(sliceStr, args=(None,100))
    df_nano['text'] = df_nano['text'].apply(sliceStr, args=(None,100))
    
    # Merge categories into single frame
    df_all = pd.concat([df_bio,df_nano], keys=['bio', 'nano'])
    
    # Create bag of words for individual categories
    df_bio_bow = bagOfWords(df_ToList(df_bio['text']),stopWords,True,minFeatureOccurs=2)
    df_nano_bow = bagOfWords(df_ToList(df_nano['text']),stopWords,True,minFeatureOccurs=2)
    # bag of words for all documents
    df_all_bow = bagOfWords(df_ToList(df_all['text']),stopWords,True,minFeatureOccurs=2)
    
    # Create bag of words for each document
#    df_bio_bow = df_bio['text'].apply(bagOfWords, args=(stopWords,True,0))
#    df_nano_bow = df_nano['text'].apply(bagOfWords, args=(stopWords,True,0))
    
    # Create tf-idf sparse matrix for all documents in categories
    df_bio_tfidf = tfidf(df_bio_bow, verbose=True)
    df_nano_tfidf = tfidf(df_nano_bow, verbose=True)
    # tf-idf for all documents
    df_all_tfidf = tfidf(df_all_bow, verbose=True)
    
    # Calculate cosine similarity between documents
    # Cosine within individual categories
    df_bio_cosSimilarity = cosineMetric(df_bio_tfidf)
    df_nano_cosSimilarity = cosineMetric(df_nano_tfidf)
    # Cosine for all documents
    df_all_rep = cosineMetric(df_all_tfidf)
    
    # Get documents which are most similar
    ## convert same documents ( [docx , docx] ) values from 1 to 0.
    df_all_cosSimilarity = replaceDiag(df_all_rep, 'cos', 0,verbose=True)
    
    ## See which documents have highest cosine similarity scores
    for name, row in df_all_cosSimilarity.iterrows():
        curDoc = df_all.iloc[name]['title']
        simDocInd = (np.argmax(row['cos']))
        maxDoc = df_all.iloc[simDocInd]['title']
        print(curDoc+" ->  "+maxDoc+"\t\t("+str(name)+":"+str(simDocInd)+")")
    
#    df_bio.join(pd.DataFrame({ind:[item] for ind,item in enumerate(similarity_matrix.ravel())}))
    
    ### LDA model
    import gensim
    ## We need to feed in whole integers from our bag or words model (therefore cannot use tf-idf)
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word = dictionary, passes=20)
    
    
    
if __name__ == "__main__":
    main()
    
    
    
#    
