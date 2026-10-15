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

# options
tp_vars = ['tp_pt', 'tp_eta', 'tp_phi', 'tp_lxy', 'tp_d0', 'tp_lz', 
           'tp_z0', 'tp_pdgid', 'tp_nmatch', 'tp_nstub', 'tp_eventid', 'tp_charge']
discrete_vars = {'tp_nmatch', 'tp_nstub', 'tp_charge'}
tp_cut = 0.1  
tp_pass = []
tp_fail = []

my_seed_groups = [
    [0, 1, 2, 3, 8, 9],
    [0, 1, 10],
    [0, 4, 7, 11],
    [4, 5, 6]
]

my_mixed_seed_groups = [
    [0, 1, 2, 3, 8, 9],
    [0, 1, 10],
    [0, 4, 7, 11],
    [4, 5, 6]
]

# my_mixed_seed_groups = [
#     [0, 1, 2, 3, 8, 9, 10], 
#     [0, 1, 4, 7, 10, 11],
#     [0, 1, 2, 3, 4, 7, 8, 9, 11],
#     [0, 4, 5, 6, 7, 11]
# ]

# my_mixed_seed_groups = [
#     [0, 1, 2, 3, 8, 9, 10], 
#     [0, 1, 4, 7, 10, 11],
#     [0, 1, 2, 3, 4, 7, 8, 9, 11],
#     [0, 4, 5, 6, 7, 11]
# ]

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



# loop over entries
my_fracs = []
for i, entry in enumerate(tree):
    if i < 1000:
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
        
        n_single_track = 0
        n_pass = 0
        n_mixed = 0
        n_fail = 0
        n_many = 0
        n_weird = 0

        for itp in trk_matchtp_indices:
            trks = trk_matchtp_indices[itp]
            seeds = []
            for trk in trks:
                seeds.append(trk_seed[trk])
            seedvals = np.unique(seeds) # this tracking particle has left stubs that formed these seeds 
            if len(seedvals) == 1:
                n_single_track += 1
            elif len(seedvals) > 1: # and len(seedvals) < 7:
                counter = 0
                for myset in my_seed_groups:
                  if set(seedvals).issubset(set(myset)):
                      counter += 1 
                
                if counter == 0:
                    counter2 = 0
                    for myset in my_mixed_seed_groups:
                        if set(seedvals).issubset(set(myset)):
                            counter2 += 1
                    
                    if counter2 == 0:
                        # print("super fail: ", seedvals)
                        n_fail += 1
                    elif counter2 == 1:
                        n_mixed += 1
                        # print("mixed: ", seedvals)
                    else:
                        # print("weird", seedvals)
                        n_weird += 1

                elif counter == 1:
                    n_pass += 1
                else: 
                    n_weird += 1
                    # print("weird!", seedvals)
            #elif len(seedvals) >= 7:
            #    n_many += 1
        
        # print(n_single_track, n_pass, n_mixed, n_fail, n_many, n_weird)
        frac_sorted =  (n_single_track + n_pass + n_mixed + n_weird) / len(trk_matchtp_indices.keys())
        my_fracs.append(frac_sorted)

fig, ax = plt.subplots()
ax.hist(my_fracs)
ax.set_xlim([0, 1])
fig.savefig('myhisto.pdf')
        

        # for it in range(n_tp):
        #     values = {name: getattr(entry, name)[it] for name in tp_vars}
        #     values['index'] = it  # original index within the event

        #     if abs(values['tp_d0']) > tp_cut:
        #         tp_pass.append(values)
        #     else:
        #         tp_fail.append(values)


# # make plots
# n_bins = 50
# for name in tp_vars:
#     if name not in ['tp_charge', 'tp_eventid', 'tp_pdgid']:
#         pass_vals = np.array([d[name] for d in tp_pass])
#         fail_vals = np.array([d[name] for d in tp_fail])

#         all_vals = np.concatenate([pass_vals, fail_vals])
#         if len(all_vals) == 0:
#             continue

#         # shared bins so pass and fail are directly comparable
#         if name in discrete_vars:
#             bins = np.arange(all_vals.min() - 0.5, all_vals.max() + 1.5, 1)
#         else:
#             bins = np.linspace(all_vals.min(), all_vals.max(), n_bins + 1)

#         fig, ax = plt.subplots(figsize=(12, 8))
#         ax.hist(pass_vals, bins=bins, histtype='step', linewidth=1.8,
#                 label=f'Displaced (N={len(pass_vals)})', color='tab:blue')
#         ax.hist(fail_vals, bins=bins, histtype='step', linewidth=1.8,
#                 label=f'Prompt (N={len(fail_vals)})', color='tab:red')

#         ax.set_xlabel(name)
#         ax.set_ylabel('Entries')
#         ax.set_yscale('log')   # remove if you prefer a linear axis
#         ax.legend()
#         fig.tight_layout()
#         fig.savefig(f'{name}_histogram.pdf', dpi=150)
#         plt.close(fig)