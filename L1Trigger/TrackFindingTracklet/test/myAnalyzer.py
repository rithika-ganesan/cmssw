import numpy
import ROOT

path = 'L1TrkNtuple_TruncatedNONE_100events_higgs900.root'

file = ROOT.TFile.Open(path, 'r')
tree = file.Get("L1TrackNtuple/eventTree")
branches = [b.GetName() for b in tree.GetListOfBranches()]

print(branches)

#print(dir(tree))

#tp_pt = tree.GetBranch('tp_pt')  #.GetEntries()

matchtrk_pt=[]
tp_pt=[]

for entry in tree:
    tp_pt.append(entry.tp_pt)
    matchtrk_pt.append(entry.trk_matchtp_pt)

print(matchtrk_pt[0])
print(tp_pt[0])

#print(tp_pt.GetFirstEntry())
#print(tp_pt.Print())
