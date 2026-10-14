import ROOT
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# load ntuple
path = '../test/L1TrkNtuple.root'
f0 = ROOT.TFile.Open(path, 'r')
tree = f0.Get('L1TrackNtuple/eventTree')
# branches = [branch.GetName() for branch in tree.GetListOfBranches()]
# print(branches)

# options
seeds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, -1]
seed_mapping = {
    8: [1, 2],
    9: [3, -1],
    10: [1, 7],
    11: [4, 7]
}
disp_seeds = seed_mapping.keys()

# functions
def compare_vals(v1, v2, tolerance=0.001):
    if v1 == v2:
        return True
    elif v1 == -v2 and np.abs(v1) == 1:
        return True
    else:
        diff = np.abs(v1 - v2) / ((v1 + v2) / 2)
        if diff <= tolerance:
            return True
        else:
            return False
    
def compare_tracks(i, j, vecs, tolerance):
    
    matchBool = True
    for vec in vecs:
        matchBool = matchBool and compare_vals(vec[i], vec[j], tolerance)

    return matchBool

# set up dataframe
matchCounts = {
    "entry": [],
    "displacedSeed": [],
    "dispTrackIndex": [],
    "promptSeed": [],
    "promptTrackIndex": []
}

# event loop
for i, entry in enumerate(tree):
    if i > -1:
        # load track variables
        trk_pt = entry.trk_pt
        trk_eta = entry.trk_eta
        trk_phi = entry.trk_phi
        trk_charge = entry.trk_charge
        trk_seed = entry.trk_seed

        # load track matchtp variables
        trk_matchtp_pt = entry.trk_matchtp_pt
        trk_matchtp_eta = entry.trk_matchtp_eta 
        trk_matchtp_phi = entry.trk_matchtp_phi
        trk_matchtp_eventid = entry.trk_matchtp_eventid 

        # get indices corresponding to seeds
        track_indices = {}
        for seed in seeds:
            track_indices[seed] = []
        for it in range(len(trk_pt)):
            track_indices[trk_seed[it]].append(it)

        # loop over displaced seeds 
        for ds in disp_seeds:
            indices = track_indices[ds]

            # loop over tracks
            for it in indices:
                # loop over prompt seeds
                for ps in seed_mapping[ds]:
                    # loop over prompt tracks
                    for jt in track_indices[ps]:
                        matchBool = compare_tracks(it, jt, [trk_pt, trk_eta, trk_phi, trk_charge], tolerance=0.05)
                        if matchBool == True:
                            # save values
                            matchCounts["entry"].append(i)
                            matchCounts["displacedSeed"].append(ds)
                            matchCounts["dispTrackIndex"].append(it)
                            matchCounts["promptSeed"].append(ps)
                            matchCounts["promptTrackIndex"].append(jt)


df = pd.DataFrame(matchCounts)

print(df.head)


    
