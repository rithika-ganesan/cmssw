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

def compare_seed_mappings(seeds, counts, seed_mapping=seed_mapping):

    output = {}

    for ds in seed_mapping.keys():
        prompt_seeds = seed_mapping[ds]
        prompt_counts = [counts[ps] for ps in prompt_seeds]

        if sum(prompt_counts) > 0:
            output[ds] = [True, prompt_counts]

    if len(output.keys()) == 0:
        return None
    else:
        return output

# set up dict
all_events = {}



# event loop

n_trk_matchtp_all = [] 
n_trk_matchtp_sel = []

for i, entry in enumerate(tree):
    if i < 101:
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

        # get track indices corresponding to the tp event id
        track_indices = {}
        for eid in np.unique(trk_matchtp_eventid):
            track_indices[eid] = []
        for it in range(len(trk_pt)):
            track_indices[trk_matchtp_eventid[it]].append(it)

        # loop over matched tracking particles
        matchedtps = {}
        trk_matchtp_sel_count = 0
        for eid in track_indices.keys():
            tp_track_indices = track_indices[eid] 
            track_seeds = []
            for tid in tp_track_indices:
                track_seeds.append(trk_seed[tid])
            
            counts = []
            for seed in seeds:
                counts.append(np.sum(track_seeds == seed))
            matchedtps[eid] = [seeds, counts]
            match_output = compare_seed_mappings(seeds, counts)
            if match_output != None:
                trk_matchtp_sel_count += 1

        n_trk_matchtp_all.append(len(track_indices)) 
        n_trk_matchtp_sel.append(trk_matchtp_sel_count)

        all_events[i] = matchedtps


# analyze 

fig, ax = plt.subplots()

bins=50
# ax.hist(n_trk_matchtp_all, bins=bins, alpha=0.8)
ax.hist(n_trk_matchtp_sel, bins=bins, alpha=0.8)

fig.savefig('myhisto.pdf')
        






#         # get indices corresponding to seeds
#         track_indices = {}
#         for seed in seeds:
#             track_indices[seed] = []
#         for it in range(len(trk_pt)):
#             track_indices[trk_seed[it]].append(it)

#         # loop over displaced seeds 
#         for ds in disp_seeds:
#             indices = track_indices[ds]

#             # loop over tracks
#             for it in indices:
#                 # loop over prompt seeds
#                 for ps in seed_mapping[ds]:
#                     # loop over prompt tracks
#                     for jt in track_indices[ps]:
#                         matchBool = compare_tracks(it, jt, [trk_pt, trk_eta, trk_phi, trk_charge], tolerance=0.05)
#                         if matchBool == True:
#                             # save values
#                             matchCounts["entry"].append(i)
#                             matchCounts["displacedSeed"].append(ds)
#                             matchCounts["dispTrackIndex"].append(it)
#                             matchCounts["promptSeed"].append(ps)
#                             matchCounts["promptTrackIndex"].append(jt)


# df = pd.DataFrame(matchCounts)

# print(df.head)


    
