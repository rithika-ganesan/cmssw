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

# options
dispSeeds = [8, 9, 10, 11]
promptSeeds = [0, 1, 2, 3, 4, 5, 6, 7]

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
for i, entry in enumerate(tree):
    if i < 10: 
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
        prompt_all, prompt_fail, disp_all, disp_fail, mixed_all, mixed_prompt = 0, 0, 0, 0, 0, 0
        d0s = []
        for itp in range(len(tp_pt)):
            if itp in trk_matchtp_indices:
                trks = trk_matchtp_indices[itp]
                my_seeds = []
                for trk in trks:
                    my_seeds.append(trk_seed[trk])
                uniqueDispSeedCount = len(set(my_seeds) & set(dispSeeds))
                uniquePromptSeedCount = len(set(my_seeds) & set(promptSeeds))
                if uniqueDispSeedCount == 0:
                    prompt_all += 1
                    tp_class = 'prompt_only'
                    if np.abs(tp_d0[itp]) > 0.1:
                            prompt_fail += 1
                        # print(i, itp, tp_d0[itp], len(trks))
                        # for trk in trks:
                        #     print(trk_d0[trk])

                elif uniqueDispSeedCount > 0 and uniquePromptSeedCount == 0:
                    disp_all += 1
                    tp_class = 'displaced_only'
                    if np.abs(tp_d0[itp]) < 0.1:
                        disp_fail += 1
                        # for trk in trks: 
                        #     print(trk_d0[trk], tp_d0[itp])

                else:
                    mixed_all += 1
                    tp_class = 'mixed'
                    if np.abs(tp_d0[itp]) < 0.1:
                        mixed_prompt += 1

        # print(d0s)
        print(f"Prompt: {prompt_fail} / {prompt_all}", f"Displaced: {disp_fail} / {disp_all}", f"Mixed: {mixed_prompt} / {mixed_all}")


                    



