import ROOT
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pdgIDs import pdgNames, pdgShortNames

# path='root://xrootd-cms.infn.it//store/mc/Phase2Spring24DIGIRECOMiniAOD/DisplacedSUSY_stopToBottom_M-800_50mm_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_AllTP_140X_mcRun4_realistic_v4-v1/2810000/422e9ac0-0bfb-4bc2-9cea-8022bcc593e0.root'
path='/eos/user/r/rganesan/DisplacedSUSY_stopToBottom_M-800_50mm_TuneCP5_14TeV-pythia8/modulewiseTruncation_10kevents_dispSUSY/truncatedVMR_10000events_merged.root'

file = ROOT.TFile.Open(path, 'r')

tree = file.Get('L1TrackNtuple/eventTree')

branch_names = [branch.GetName() for branch in tree.GetListOfBranches()]
tp_vars = ['tp_pt', 'tp_eta', 'tp_phi', 'tp_lxy', 'tp_d0', 'tp_lz', 'tp_z0', 'tp_pdgid', 'tp_nmatch', 'tp_nstub', 'tp_eventid', 'tp_charge']

# dat = {}
# for vr in tp_vars:
#     dat[vr] = []

# for i, entry in enumerate(tree):
#     if i != 0:
#         continue

#     for vr in tp_vars:
#         for e in getattr(entry, vr):
#             dat[vr].append(e)

def get_event_ids(tree):

    my_ids = []
    for i, entry in enumerate(tree):
        if i > 2: 
            continue

        ids = getattr(entry, 'tp_eventid')
        print(f"Entry {i} tp_eventid vector:")
        print("  ")
        print(ids)
        print("  ")

    return my_ids

print(get_event_ids(tree)) 

# print(dat['tp_eventid'])

# dat = pd.DataFrame(dat)

# e1 = dat[dat['tp_eventid'] == ]

# dat = dat[dat['tp_pt'] > 3]

# mydat = np.unique(dat['tp_pdgid'].to_numpy(), return_counts=True)

# for i, pdgid in enumerate(mydat[0]):
#     print(pdgNames[pdgid]+"s "+pdgShortNames[pdgid]+":", mydat[1][i])

# x = 'tp_d0'
# y = 'tp_lxy'

# fig, ax = plt.subplots()
# ax.scatter(dat[x], dat[y], marker='.', c='k')
# ax.set_xlabel(x)
# ax.set_ylabel(y)
# # ax.set_xlim(-3.14, 3.14)
# # ax.set_ylim([0, 20])
# fig.tight_layout()
# plt.savefig('d0_lxy.pdf')

## pt 

# myVars = ['trk_pt', 'tp_pt', 'matchtrk_pt']

# myHists = {}
# myHists['trk_pt'] = ROOT.TH1F('h_trk_pt', "; p_T [GeV]; Entries", 100, 0, 200)



# for i, entry in enumerate(tree):
#     if i > 5:
#         continue
#     myVec = getattr(entry, 'tp_phi')
#     # for e in myVec:
#     #     print(e)
#     myPtEntries.append(len(myVec))

# # print("For the first few events, the numbers of entries in the 'matchtrk_pt' vector: ")
# print(myPtEntries)


# canvas = ROOT.TCanvas("c1", "Histogram", 1200, 600)
# myHists['trk_pt'].Draw()
# canvas.Draw()
# canvas.SaveAs("dispSUSY_pt.pdf")

# myHistNames = {}
# myHists = {}
# for vr in myVars:
#     myHistNames[vr] = 'h_'+vr #generateHistogramName(vr)
#     myHists[vr] = ROOT.TH1F(myHistNames[vr], "; p_T [GeV]; Entries", 100, 0, 200)

# for entry in tree:
#     for vr in myVars:
#         myHists[vr].Fill(getattr(entry, vr))

# canvas = ROOT.TCanvas("c1", "Histogram", 1200, 600)
# for i, vr in enumerate(myVars):
#     hist = myHists[vr]
#     if i == 0:
#         hist.Draw("HIST")
#     else:
#         hist.Draw("HIST SAME")

# canvas.Draw()
# canvas.SaveAs("dispSUSY_pt.pdf")

# print(branch_names)
# print(branch_entries)