# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 21:35:40 2018

@author: Jonathan Hill

Rename sample pages to their curID's
"""

import argparse
import os
import sys
import re
import shutil
import xmltodict

samplesDir = "..\__RANDSAMPLES"

def checkDirExists(d, s):
        if(d):
            if(os.path.isdir(d)):
                return True
            else:
                print(s+" directory does not exist: "+d)
        else:
            print("empty argument given for "+s)
        return False

def getSampleList(inp):
    return next(os.walk(inp))[2]

def printDirSampleSize(n, s):
    print("Input directory has "+str(n)+" files +("+s+")")
    if n == 0: sysExit()

def getSampleCurID(s):
    filePath = os.path.join(samplesDir, s)
    try:
        f = open(filePath)
        doc = xmltodict.parse(f.read())
        curid = doc["mediawiki"]["page"]["id"]
        f.close()
        return curid
    except IOError:
        print("IO Error in getSampleCurID")

def sysExit():
    sys.exit()

def main():
    samples = getSampleList(samplesDir)
    printDirSampleSize(len(samples),samplesDir)
    print("renaming all samples")
    # loop through all samples
    for s in samples:
        # get the curID for each
        curID = getSampleCurID(s)+".xml"
        # rename that file
        os.rename(os.path.join(samplesDir,s), os.path.join(samplesDir,curID))
    
if __name__ == "__main__":
    main()