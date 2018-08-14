# -*- coding: utf-8 -*-
"""

@author: Jonathan Hill

Remove even numbered samples from directory

"""

import argparse
import os
import sys
import re
import shutil

def getArgs():
    parser = argparse.ArgumentParser(description="Remove even numbered samples from directory")
    parser.add_argument('input', help="The directory where samples are stored")
    parser.add_argument('output', help="Where to store new copies")
    return parser.parse_args()

def checkDirExists(d, s):
        if(d):
            if(os.path.isdir(d)):
                return True
            else:
                print(s+" directory does not exist: "+d)
        else:
            print("empty argument given for "+s)
        return False

def getDirSampleSize(inp):
    #return len([name for name in os.listdir(inp) if os.path.isfile(name)])
    return len(next(os.walk(inp))[2])
    
def checkDirSampleSize(n, s):
    if n == 0:
        print("Input directory has "+str(n)+" files +("+s+")")
        sysExit()

def remove_even(s):
    for i in s[:]:
        if int(re.sub('[^0-9]', '',i)) % 2 == 0:
            s.remove(i)
    return s

def sysExit():
    sys.exit()

def main():
    args = getArgs()
    # Input directory
    inp = args.input if (checkDirExists(args.input, "input")) else sysExit()
    out = args.output if (checkDirExists(args.output, "output")) else sysExit()
    totalSamples = getDirSampleSize(inp)
    checkDirSampleSize(totalSamples,inp)
    # Get list of files in directory
    allSamples = remove_even(os.listdir(inp))
    # Make a copy of files in a new directory
    errors = []
    copied = 0
    sampleNum = 0
    print("Copying process started, please wait")
    for i in allSamples:
        filePath = os.path.join(inp, allSamples[sampleNum])
        #print(filePath+"\n")
        try:
            shutil.copy(filePath, out)
            copied +=1
        except OSError as why:
            errors.append((filePath, out+allSamples[i], str(why)))
        except shutil.Error as err:
            errors.extend(err.args[0])
        sampleNum+=1
    print("Sample copying complete ("+str(copied)+"/"+str(len(allSamples))+" samples successful)")
    try:
        shutil.copystat(inp, out)
    except OSError as why:
        # can't copy file access times on Windows
        if why.winerror is None:
            errors.extend((inp, out, str(why)))
    if errors:
        raise shutil.Error(errors)
    
if __name__ == "__main__":
    main()
