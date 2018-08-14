# -*- coding: utf-8 -*-
"""
Author: Jonathan Hill

This script takes a random sample from a subset of wikipedia pages to be used for preliminary development
(Creates copies of the pages and places into another folder)
"""
import argparse
import os
import sys
import random
import shutil

def getArgs():
    parser = argparse.ArgumentParser(description="Perfroms random sampling by creating copies of sample pages (input directory) and placing these into an output directory")
    parser.add_argument('input', help="The directory where samples are stored")
    parser.add_argument('output', help="Where to store new copies")
    parser.add_argument('n', help="Number of samples to take", default="1001")
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

def getMaxSampleSize(inp):
    #return len([name for name in os.listdir(inp) if os.path.isfile(name)])
    return len(next(os.walk(inp))[2])

def checkDirSampleSize(n, s):
    if n == 0:
        print("Input directory has "+str(n)+" files +("+s+")")
        sysExit()

def ConsoleInfo(inp, out, maxSamples, n):
    print("Input Directory: "+inp+"\n")
    print("Output Directory: "+out+"\n")
    print("Number of total samples in input directory: "+str(maxSamples)+"\n")
    print("Samples to copy: "+str(n)+"\n")

def sysExit():
    sys.exit()

def main():
    args = getArgs()
    
    # get input and output directory, check if exists
    inp = args.input if (checkDirExists(args.input, "input")) else sysExit()
    out = args.output if (checkDirExists(args.output, "output")) else sysExit()
    # Check input dir has files and get samples
    maxSamples = getMaxSampleSize(inp)
    checkDirSampleSize(maxSamples, inp)
        
    # create tuple of n random numbers
    n = int(args.n)
    allSamples = os.listdir(inp)
    sampleIndices = tuple(random.randint(1,maxSamples) for _ in xrange(n))
    
    # Give info before copying
    ConsoleInfo(inp, out, maxSamples, n)
    proceed = 0
    copied = 0
    while True:
        try:
            proceed=int(raw_input('Proceed to copy over random sample?: (0: False, 1: True)'))
            if proceed == 0 or proceed ==1: break
        except ValueError:
            print "Type 0 or 1"
    if proceed==1:
        # Copy files into output directory
        errors = []
        for i in sampleIndices:
            filePath = os.path.join(inp, allSamples[i])
            print(filePath+"\n")
            try:
                shutil.copy(filePath, out)
                copied +=1
            except OSError as why:
                errors.append((filePath, out+allSamples[i], str(why)))
            except shutil.Error as err:
                errors.extend(err.args[0])
        print("Sample copying complete ("+str(copied)+"/"+str(n)+" samples successful)")
        try:
            shutil.copystat(inp, out)
        except OSError as why:
            # can't copy file access times on Windows
            if why.winerror is None:
                errors.extend((inp, out, str(why)))
        if errors:
            raise shutil.Error(errors)
    return
    
if __name__ == "__main__":
    main()