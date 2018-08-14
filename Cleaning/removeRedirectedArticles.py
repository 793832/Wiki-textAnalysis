# -*- coding: utf-8 -*-
"""

@author: Jonathan Hill
"""
import os
import sys
import re

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
    regex = re.compile(r"<redirect\s+title\s*=\s*\".+\">")
    count = 0
    i = 0
    for s in samples:
        # Read file, go through each word
        filePath = os.path.join(samplesDir, s)
        
        try:
            f = open(filePath)
            doc = f.read()
            match = regex.findall(doc)
            f.close()
            if match:
                count += 1
                os.remove(filePath)

        except IOError:
              print("IO Error")
        print_progress(i, sampleLen, prefix = 'Progress:', suffix = 'Complete', length = 50)
        i+=1
    print "\nnumber of files removed: "+str(count)
    
if __name__ == "__main__":
    main()
    
    
    
#    
