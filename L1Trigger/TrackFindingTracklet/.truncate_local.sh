#!/bin/bash

bash .1_loadSettings.sh $1 $2
bash .2_reBuild.sh
bash .3_configureCfg.sh $1 $2
bash .4_runMaker.sh 
