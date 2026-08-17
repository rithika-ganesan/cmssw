#!/bin/bash

path='/eos/user/r/rganesan/HTo2LongLivedTo4mu_MH-125_MFF-12_CTau-900mm_TuneCP5_14TeV-pythia8'
#path='/eos/user/r/rganesan/DisplacedSUSY_stopToBottom_M-800_50mm_TuneCP5_14TeV-pythia8'
prefix='crab_truncated*10000*'

plotdir='truncPlots_crab_10k-events_Higgs900'
#mkdir $plotdir
#mkdir $path/modulewiseTruncation_10kevents_Higgs900

for dir in $path/$prefix; do
	name=$(basename $dir)
	count=$(ls $dir/*/0000/*.root | wc -l)
	module=$(echo "$name" | sed -E 's/.*truncated([^_]*)_.*/\1/')
	mergedfile="truncated${module}_10000events_merged.root"
	
	echo $module $count

	#totalcount=0
	##### get file count 
	#for rfile in $dir/*/0000/*.root; do
	#	fname=$(basename $rfile)
	#	fcount=$(./getEventCount.csh $rfile | tail -1)
	#	totalcount=$((totalcount+fcount))
		#echo $fname $fcount 
	#done

	#echo $module $totalcount
	
	##### merge root files inside directory
	#hadd $path/modulewiseTruncation_10kevents_Higgs900/$mergedfile $dir/*/0000/*.root
	#ls $dir/*.root

	##### check merged file count
	#echo $module $(./getEventCount.csh $path/modulewiseTruncation_10kevents_Higgs900/$mergedfile | tail -1)
	
	#mkdir $plotdir/$module
	#cp plotMaker/* $plotdir/$module 
	cd $plotdir/$module
	./makeHists.csh $path/modulewiseTruncation_10kevents_Higgs900/$mergedfile   
	cd ..
	cd ..
	#echo $(pwd)
	#echo "    "


	#mkdir $plotdir/$name

done
