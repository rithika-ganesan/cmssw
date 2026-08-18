#!/bin/bash

cd test
runFile=L1TrackNtupleMaker_cfg.py
outputName=$(grep -oP "cms\.string\('\K[^']*" $runFile)
dirName="${outputName%.root}"

cmsRun $runFile 

./makeHists.csh $outputName

mkdir temp
mv *.root temp/
mv MVA_plots temp/
mv FitResults temp/
mv results.out temp/
mv TrkPlots temp/

ls -alhX temp

mv temp ../myruns/$dirName 

