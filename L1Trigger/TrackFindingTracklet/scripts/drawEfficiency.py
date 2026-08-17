import numpy as np
import glob
from ROOT import gStyle
import ROOT

#parser = ArgumentParser()
#parser.add_argument("-i", "--input", dest="input", help="input files")

# styles

gStyle.SetPadLeftMargin(0.1) 
gStyle.SetPadRightMargin(0.16) 
gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadTopMargin(0.05)
gStyle.SetLabelFont(42, "XYZ")
gStyle.SetTextFont(30)

# get files 
cernboxDispSUSY='/eos/user/r/rganesan/DisplacedSUSY_stopToBottom_M-800_50mm_TuneCP5_14TeV-pythia8/modulewiseTruncation_10kevents_dispSUSY/'
cernboxHiggs900='/eos/user/r/rganesan/HTo2LongLivedTo4mu_MH-125_MFF-12_CTau-900mm_TuneCP5_14TeV-pythia8/modulewiseTruncation_10kevents_Higgs900/'

#directoryPath='/eos/user/r/rganesan/DisplacedSUSY_stopToBottom_M-800_50mm_TuneCP5_14TeV-pythia8/crab_truncatedTPDPLUSMP_DispSUSY_1510pre_10000events/260806_185451/0000/'

# options
directoryPath=cernboxHiggs900
plotTitle="Higgs to 2 LLPs to 4mu, ctau 900mm"
widePlot=False

# get files
allVariants=['GLOBAL', 'IR', 'VMR', 'TB', 'MP', 'PC', 'TP', 'TPD', 'DR', 'TRE', 'TPDplusMP', 'ALL', 'NONE']
badEggs=['MP', 'TPD', 'DR', 'TP']
variantLabels={
    'GLOBAL': "No truncation",
    'IR': "InputRouter",
    'VMR': "VMRouter",
    'TB': "TrackBuilder",
    'MP': "MatchProcesser",
    'PC': "ProjectionCalculator",
    'TP': "TrackProcesser",
    'TPD': "TPDisplaced",
    'DR': "DuplicateRemoval",
    'TRE': "TRE",
    'ALL': "Global truncation",
    'NONE': "No truncation"
}


filePaths = {}
files = {}
variants = []

for vr in allVariants:
    searchStem=directoryPath+"output_truncated"+vr+"_*.root"
    mySearch=glob.glob(searchStem)
    if len(mySearch) == 1:
        variants.append(vr)
        filePaths[vr] = mySearch[0]
        files[vr] = ROOT.TFile.Open(filePaths[vr], 'r')
    if len(mySearch) > 1:
        raise Exception("More than one file found for", vr, ".")

# define variables of interest
variables=['eff_d0']

def get_colors(palette, ncolors):
    ROOT.gStyle.SetPalette(palette)#kRainBow, kViridis, kSolar
    palette = ROOT.TColor.GetPalette()
    N_colors = palette.GetSize()

    colors=[]
    for i in range(ncolors):
        idx = int(i * (N_colors - 1) / max(1, ncolors - 1))
        color = palette[idx]
        colors.append(color)

    return colors

colors = get_colors(palette=ROOT.kRainbow, ncolors=len(allVariants))
colorsDict = {}
for i, vr in enumerate(allVariants):
    colorsDict[vr] = colors[i]


# get hists and plot
if widePlot == True:
    canvas = ROOT.TCanvas("c1", "Histogram", 1200, 600)
    legend = ROOT.TLegend(0.85, 0.6, 0.95, 0.9) #(0.8, 0.6, 0.9, 0.9)
else:
    canvas = ROOT.TCanvas("c1", "Histogram", 800, 600)
    legend = ROOT.TLegend(0.8, 0.6, 0.9, 0.9)

    # legend styles
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.SetTextSize(0.025)

for i, vr in enumerate(variants):
    hist = files[vr].Get(variables[0])
    hist.SetTitle(plotTitle)
    hist.SetTitleSize(0.025)
    hist.SetLineColor(colorsDict[vr])
    hist.SetLineWidth(1)
    if vr == "TP":
        hist.SetLineWidth(2)
    hist.SetMarkerColor(colorsDict[vr])
    hist.SetMarkerStyle(8)
    hist.SetMarkerSize(0.8)
    hist.GetXaxis().SetLabelSize(0.035)
    hist.GetXaxis().SetTitleSize(0.0375)
    hist.GetYaxis().SetLabelSize(0.035)
    hist.GetYaxis().SetTitleSize(0.0375)
    hist.GetYaxis().SetTitleOffset(0.0)
    #hist.GetYaxis().SetRangeUser(0.2, 1.0)
    if vr: #in badEggs:
        if i==0:
            hist.Draw("HIST")
        else:
            hist.Draw("HIST SAME")

        legend.AddEntry(hist, variantLabels[vr], "lp")

legend.Draw()
canvas.Draw()
canvas.SaveAs("hist.pdf")
#canvas.SaveAs("modulewiseTruncation_DispSUSY-200PU_eff-d0_betterEffModules.pdf")
