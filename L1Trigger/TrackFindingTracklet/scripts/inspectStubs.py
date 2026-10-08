import ROOT
import array

path = '../test/L1TrkNtuple.root'

f0 = ROOT.TFile.Open(path, 'r')

tree = f0.Get('L1TrackNtuple/eventTree')
# print([branch.GetName() for branch in tree.GetListOfBranches()])

layer_bin_edges=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 11.5, 12.5, 13.5, 14.5, 15.5]
layer_bin_edges=array.array('d', layer_bin_edges)
nbins = len(layer_bin_edges) - 1

for e, entry in enumerate(tree):

    layers = entry.allstub_layer
    
    hist = ROOT.TH1D(f"layer_hist_{e}", 'layers;bin edges;counts', nbins, layer_bin_edges)

    for i in range(len(layers)):
        hist.Fill(layers[i])

    print(f"For entry {e}:")
    print("Bin index : Content")
    for i in range(0, hist.GetNbinsX() + 2):
        content = hist.GetBinContent(i)
        print(f"Bin {i}: {content}")
        

# adr = f0.Get('AnalyzerDR/DR/Counts')
# print(adr.ls())
