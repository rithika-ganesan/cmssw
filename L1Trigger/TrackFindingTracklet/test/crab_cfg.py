from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'truncatedTPDPLUSMP_DispSUSY_1510pre_10000events'
config.General.workArea = 'l1TF_displacedTracking_crab'                                                              ## folder that will be created in the work area, will contain the folder above. Can stay the same for all your submissions in principle
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'L1TrackNtupleMaker_cfg.py'  ## cfg file that will be run (e.g. the one you pass to cmsRun xx_cfg.py)
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 4000                      ## increase of the default mem request as these jobs are quite heavy
config.JobType.numCores = 4                           ## run multithread

config.Data.inputDataset = '/DisplacedSUSY_stopToBottom_M-800_50mm_TuneCP5_14TeV-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_AllTP_140X_mcRun4_realistic_v4-v1/GEN-SIM-DIGI-RAW-MINIAOD' 
#config.Data.inputDataset = '/HTo2LongLivedTo4mu_MH-125_MFF-12_CTau-1500mm_TuneCP5_14TeV-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/GEN-SIM-DIGI-RAW-MINIAOD'
#config.Data.inputDataset = '/HTo2LongLivedTo4mu_MH-125_MFF-12_CTau-900mm_TuneCP5_14TeV-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/GEN-SIM-DIGI-RAW-MINIAOD'
## for fnal and normal eos
config.Data.outLFNDirBase = '/store/user/rganesan'   ## output folder on the storage element (which is eos on lxplus, so everything after /eos/cms/)


config.Data.splitting = 'Automatic'                        ## each job will process one input file
config.Data.totalUnits = 10000
#config.Data.unitsPerJob = 1
#config.Data.totalUnits = 10000
config.Data.publication = False

config.Site.storageSite = 'T3_CH_CERNBOX'                 ## where to store the output, in this case eos lxplus   


