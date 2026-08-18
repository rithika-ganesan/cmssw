import numpy as np
import os
import sys
import ROOT
import glob

filepath="/eos/user/r/rganesan/DisplacedSUSY_stopToBottom_M-800_50mm_TuneCP5_14TeV-pythia8/crab_truncated*_dispSUSY_1510pre_5000events/"

mylist=glob.glob(filepath)

print(mylist)

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



