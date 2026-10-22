# imports

import ROOT
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
plt.style.use('/afs/cern.ch/user/r/rganesan/private/plotting/classic.mplstyle')

# load ntuple
path = '../test/L1TrkNtuple-dispSUSY-200PU-withStubs.root'
f0 = ROOT.TFile.Open(path, 'r')
tree = f0.Get('L1TrackNtuple/eventTree')
branches = [branch.GetName() for branch in tree.GetListOfBranches()]
# print(branches)

# options
d0_cut = 0.1
n_minidenticalstubs = 3

# functions 
def get_track(tracks_, i):
    """Return a single track as a dictionary of scalars."""
    return {key: val[i] for key, val in tracks_.items()}

def load_stubrefs(trk_a, trk_b):
    """Take two individual tracks and return their trk_stubref lists."""
    refs_a = trk_a['trk_stubrefs']   # list of 11 refs (one per layer/disk)
    refs_b = trk_b['trk_stubrefs']
    return refs_a, refs_b

class PairFlags:
    """Stores a boolean for each unordered pair of indices."""

    def __init__(self, default=False):
        self.default = default
        self._data = {}

    @staticmethod
    def _key(i, j):
        return (i, j) if i < j else (j, i)

    def set(self, i, j, value):
        self._data[self._key(i, j)] = bool(value)

    def get(self, i, j):
        return self._data.get(self._key(i, j), self.default)

    def __getitem__(self, ij):
        return self.get(*ij)

    def __setitem__(self, ij, value):
        self.set(*ij, value)

def compare_event_tracks(eventid, tracks):
    flags = PairFlags()
    tracks_ = tracks[eventid]                  
    n_trk = len(tracks_['trk_id'])
    for i in range(n_trk):
        trk_i = get_track(tracks_, i)            
        for j in range(i + 1, n_trk):
            trk_j = get_track(tracks_, j)
            refs_i, refs_j = load_stubrefs(trk_i, trk_j)
            same = 0
            for layer in range(11):
                si, sj = refs_i[layer], refs_j[layer]
                print(si, sj)
                if len(si) > 0 and len(sj) > 0:
                    if si == sj:
                        same += 1
            flags[i, j] = same > n_minidenticalstubs

    return flags 

# store track data in easier structure
track_vars = ['trk_pt', 'trk_eta', 'trk_d0', 'trk_z0']
stub_branches = [f"trk_stubref_ld{il}" for il in range(11)]
tracks = {}   # tracks[event_number] -> dictionary for that event
for i, entry in enumerate(tree):
    vals = {var: np.asarray(getattr(entry, var)) for var in track_vars}
    n_trk = len(vals['trk_pt'])

    layers = [getattr(entry, name) for name in stub_branches]
    stubrefs = [list(refs) for refs in zip(*layers)]

    tracks[i] = {
        'trk_id': np.arange(n_trk),
        **vals,
        'trk_stubrefs': stubrefs,
    }












