import ROOT

path='root://xrootd-cms.infn.it//store/mc/Phase2Spring24DIGIRECOMiniAOD/DisplacedSUSY_stopToBottom_M-800_50mm_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_AllTP_140X_mcRun4_realistic_v4-v1/2810000/422e9ac0-0bfb-4bc2-9cea-8022bcc593e0.root'

file = ROOT.TFile.Open(path, 'r')

tree = file.Get('Events')

print(tree.GetListOfKeys())