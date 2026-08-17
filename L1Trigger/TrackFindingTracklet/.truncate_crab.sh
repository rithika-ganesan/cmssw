#!/bin/bash

which_truncate=$1
nevents=$2

bash .1_loadSettings.sh $which_truncate
bash .2_reBuild.sh 
bash .3_configureCfg.sh $which_truncate $nevents "Ht2LLPt4mu-ctau1500mm" 
bash .4_editCrabCfg.sh $which_truncate $nevents

cd test
crab submit crab_cfg.py 
cd .. 
