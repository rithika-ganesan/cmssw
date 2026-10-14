# imports

import ROOT
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# load ntuple
path = '../test/L1TrkNtuple-DispSUSY200PU.root'
f0 = ROOT.TFile.Open(path, 'r')
tree = f0.Get('L1TrackNtuple/eventTree')
# branches = [branch.GetName() for branch in tree.GetListOfBranches()]
# print(branches)

# functions
def get_indices_by_variable(variable, list_vars=None):
    if list_vars == None:
        list_vars = np.unique(variable) 

    indices = {}
    for var_ in list_vars:
        indices[var_] = []

    for iv in range(len(variable)):
        indices[variable[iv]].append(iv)

    return indices

# get truth duplicates 
percentages = []
test_pt_cut = 3 
test_d0_cut = 1

saved_pts = []
saved_d0s = []
for i, entry in enumerate(tree):
    if i < 20: 
        # get vars
        trk_matchtp_eventid = entry.trk_matchtp_eventid 
        trk_pt = entry.trk_pt
        trk_eta = entry.trk_eta 
        trk_phi = entry.trk_phi 
        trk_d0 = entry.trk_d0
        trk_seed = entry.trk_seed
        tp_pt = entry.tp_pt 
        tp_eta = entry.tp_eta
        tp_phi = entry.tp_phi 
        tp_d0 = entry.tp_d0 
        tp_nstub = entry.tp_nstub
        tp_pdgid = entry.tp_pdgid
        
        # get tp track indices
        trk_matchtp_indices = get_indices_by_variable(trk_matchtp_eventid)

        # # get stats
        # percent = len(trk_matchtp_indices) * 100 / len(tp_pt)
        # percentages.append(percent)
        # # print(f"Event {i} has {len(trk_matchtp_indices)} tracking particles matched to tracks, and {len(tp_pt)} tracking particles.")

        # look through tracking particles and see what the issues are
        lost_pt, saved_pt = [], []
        lost_d0, saved_d0 = [], []
        for itp in range(len(tp_pt)):
            if itp not in trk_matchtp_indices:
                lostParticle = True
            elif itp in trk_matchtp_indices:
                lostParticle = False
            else:
                print(f"Missing tp at index {itp} in event {i}")
                lostParticle = None

            if lostParticle == True:
                lpt, ld0 = tp_pt[itp], tp_d0[itp]
                if lpt > test_pt_cut and ld0 > test_d0_cut:
                    # lost_pt.append(lpt)
                    # lost_d0.append(ld0)
                    print(i, itp)
                    print(lpt)
                    print(ld0)
                    print(tp_eta[itp])
                    print(tp_phi[itp])
                    print(tp_nstub[itp])
                    print(tp_pdgid[itp])
                    print(" ")

            if lostParticle == False:
                saved_pts.append(tp_pt[itp])
                saved_d0s.append(tp_d0[itp])
                    

        # if len(lost_pt) > 0:
        #     # print(np.median(lost_pt))
        #     # print(np.median(lost_d0))
        #     print(lost_pt)
        #     print(lost_d0)

# print("Minimum:", min(percentages))
# print("Maximum:", max(percentages))
# print("Mean:", np.average(percentages))
# print("Median:", np.median(percentages))