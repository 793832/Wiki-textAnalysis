# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 12:20:43 2018

@author: Jonathan HIll
"""

import os
import sys
import xmltodict

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

def getSampleFiles(d):
    try:
        return next(os.walk(d))[2]
    except IOError:
        print("IO Error when getting sample files")

def getElementValues(s):
        filePath = os.path.join(samplesDir, s)
        try:
            f = open(filePath)
            doc = xmltodict.parse(f.read())
            
            # get id from fields
            curid = doc["mediawiki"]["page"]["id"]
            f.close()
            if not curid:
                curid = s
            return curid+".xml"
        except IOError:
           print("IO Error")
            
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

def sysExit():
    sys.exit()
    
def main():
    # Get list of sample files
    samples = getSampleFiles(samplesDir) if (checkDirExists(samplesDir, "samples")) else sysExit()
    sampleLen = len(samples)
    # Go through each sample file
    count = 0
    for s in samples:
        # Read file, go through each word
        os.rename(os.path.join(samplesDir, s), os.path.join(samplesDir,getElementValues(s)))
        print_progress(count, sampleLen, prefix = 'Progress:', suffix = 'Complete', length = 50)
        count+=1
    
if __name__ == "__main__":
    main()
    
    
    