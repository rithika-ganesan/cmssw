# imports

import ROOT
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
plt.style.use('/afs/cern.ch/user/r/rganesan/private/plotting/classic.mplstyle')

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

nmatches_pts = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: []
}

for i, entry in enumerate(tree):
    if i < 1: 
        # get vars
        trk_matchtp_eventid = entry.trk_matchtp_eventid 
        trk_pt = entry.trk_pt
        trk_eta = entry.trk_eta 
        trk_phi = entry.trk_phi 
        trk_d0 = entry.trk_d0
        trk_genuine = entry.trk_genuine
        trk_seed = entry.trk_seed
        tp_pt = entry.tp_pt 
        tp_eta = entry.tp_eta
        tp_phi = entry.tp_phi 
        tp_d0 = entry.tp_d0 
        tp_nstub = entry.tp_nstub
        tp_pdgid = entry.tp_pdgid
        tp_nmatch = entry.tp_nmatch
        
        # get tp track indices
        trk_matchtp_indices = get_indices_by_variable(trk_matchtp_eventid)

        # loop through tps
        for itp in range(len(tp_pt)):
            nmatch = tp_nmatch[itp]
            nmatches_pts[nmatch].append(tp_pt[itp])

fig, ax = plt.subplots(figsize=(10, 7))

for nmatch in nmatches_pts.keys():
    ax.hist(nmatches_pts[nmatch], alpha=0.5, label=f"{nmatch} matched tracks", bins=np.linspace(0, 350, 51))

ax.set_yscale('log')
ax.legend(loc='best')
ax.set_xlabel('TP pt [GeV]')
fig.savefig('myhisto.pdf')