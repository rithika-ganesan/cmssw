#!/bin/bash

which_truncate="$1"

which_file="interface/Settings.h"
cmssrc='/afs/cern.ch/user/r/rganesan/private/CMSSW_15_1_0_pre4/src/'
tft="/afs/cern.ch/user/r/rganesan/private/CMSSW_15_1_0_pre4/src/L1Trigger/TrackFindingTracklet/"

#bash loadTruncationSettings.sh $which_truncate $which_file # change vals in Settings.h to desired truncation lengths
cd $cmssrc && scram b -j 8 && cd $tft # recompile 
