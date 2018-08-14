# -*- coding: utf-8 -*-
"""

@author: Jonathan Hill
"""

import os
import sys
import re
import pandas as pd

samplesDir = "G:\WikiProject 2018\pages"

def checkDirExists(d, s):
        if(d):
            if(os.path.isdir(d)):
                return True
            else:
                print(s+" directory does not exist: "+d)
        else:
            print("empty argument given for "+s)
        return False

def getMaxSampleSize(inp):
    #return len([name for name in os.listdir(inp) if os.path.isfile(name)])
    return len(next(os.walk(inp))[2])

def sysExit():
    sys.exit()

def saveCatToFile(location, name, cat):
    try:
        newFile = open(os.path.join(location,name),'w')
        newFile.writelines(cat)
        newFile.close()
        print("Saved categories to file")
    except IOError:
        print("IO Error when saving to file")

# Print iterations progress
def print_progress(iteration, total, prefix='', suffix='', decimals=1, length=100):
    """
    Call in a loop to create terminal progress bar

    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def main():
    # Input directory
    inp = "G:\Data Science MSc\__RANDSAMPLES" if (checkDirExists("G:\Data Science MSc\pages_sample_original", "input")) else sysExit()
    samples = os.listdir(inp)
    # Create array for categories
    categories = []
    # Open all files to read categories
    sampleNum = 0
    regex = re.compile(r"\[\[Category:.*\]\]")
    for i in samples:
        filePath = os.path.join(inp, samples[sampleNum])
        try:
            f = open(filePath)
            txt = f.read()
            matches = regex.findall(txt)
            f.close()
            if matches:
                # Remove template string & Add to categories list of not already in it
                for (i,m) in enumerate(matches):
                    if matches[i] not in categories:
                        categories.append(re.sub('\[\[Category:', '', matches[i])[:-2]+"\n")
        except IOError:
              print("IO Error")
        sampleNum+=1
    #for c in categories:
    #    print(c+"\n")
    saveCatToFile("G:\Data Science MSc","Categories",categories)

def saveDataFrames(df, name):
    pd.to_pickle(df,os.path.join("G:\WikiProject 2018\stored_dataframes",name+".pkl"))

def fillDataFrameCats(s, cats, re):
    filePath = os.path.join(samplesDir, s)
    try:
        f = open(filePath)
        txt = f.read()
        f.close()
        for c,r in cats,re:
            print (s+":\t"+c)
#        
#        # get text from fields
#        title = doc["mediawiki"]["page"]["title"]
#        try:
#            text = doc["mediawiki"]["page"]["revision"]["text"]["#text"]
#            categories = getCategories(text, s[:-4])
#        except KeyError:
#            AddBrokenKey(s[:-4])
#            text = doc["mediawiki"]["page"]["revision"]["text"]
#            categories = []
#
#        return [s[:-4],title,text,categories]
    except IOError:
        print("IO Error")
        sysExit()

def collectArticleListbyCat():
    inp = "G:\WikiProject 2018\pages" if (checkDirExists("G:\WikiProject 2018\pages", "input")) else sysExit()
#    catToFind = ['Biotechnology','Nanotechnology']
    catToFind = ['Biotechnology']
    cats = ''.join(["("+cat+")|" for cat in catToFind])[:-1]
    regex = re.compile(r"\[\[Category:\s*("+ cats +")\]\]")
    
    pagesWithCategories = []
    samples = os.listdir(inp)
    sampleLen = len(samples)
    count = 0
    
    #df = pd.DataFrame(columns=catToFind)
    
    # Get all pages with categories
    for s in samples:
        filePath = os.path.join(inp, s)
        try:
            f = open(filePath)
            txt = f.read()
            matches = regex.findall(txt)
            f.close()
            if matches:
                pagesWithCategories.append(s)
            print_progress(count, sampleLen, prefix = 'Progress:', suffix = 'Complete', length = 50)
            count +=1
        except IOError:
              print("IO Error")
    
    # populate dataframe
    regexes = []
    [regexes.append("\[\[Category:\s*("+ c +")\]\]") for c in catToFind]
    df = df.append([pd.Series(data=fillDataFrameCats(s, catToFind, regexes), index=catToFind) for s in pagesWithCategories], ignore_index=True)
    
    # Save categories to file
    df = pd.DataFrame(pagesWithCategories)
    saveDataFrames(df, cats)

if __name__ == "__main__":
    main()