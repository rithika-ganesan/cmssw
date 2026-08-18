import numpy as np
import os
import sys
import ROOT
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default=None, help="Path to a single file.")
parser.add_argument("-d", "--dir", default=None, help="Regex expression to a directory containing a number of files")
parser.add_argument("-t", "--treepath", default="L1TrackNtuple/eventTree")
parser.add_argument("-s", "--sum", default=True, help="If true, returns the sum of all events in the given set of files.")
args = parser.parse_args()

def get_entries(filepath, treepath):
    f = ROOT.TFile.Open(filepath, "READ")
    if not f or f.IsZombie():
        print("Could not open file")
        return None

    obj=f.Get(treepath)
    if not obj:
        print("Treepath not found.")
        f.Close()
        return None

    n = obj.GetEntries()

    f.Close()
    return int(n)

if args.file != None and args.dir == None:
    output = get_entries(args.file, args.treepath)
elif args.file == None and args.dir != None:
    filelist = glob.glob(args.dir)
    output = []
    for file in filelist:
        output_ = get_entries(file, args.treepath)
        if type(output_) == int:
            output.append(output_)
    if args.sum == True:
        output = sum(output)
else:
    raise Exception("Specify either a single file or a directory containing several files.")

print(output)
