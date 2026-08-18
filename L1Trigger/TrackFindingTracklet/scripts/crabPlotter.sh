#!/bin/bash

path='/eos/user/r/rganesan/HTo2LongLivedTo4mu_MH-125_MFF-12_CTau-900mm_TuneCP5_14TeV-pythia8'
#path='/eos/user/r/rganesan/DisplacedSUSY_stopToBottom_M-800_50mm_TuneCP5_14TeV-pythia8'
prefix='crab_truncated*'

plotdir='../plots/truncPlots_crab_10k-events_Higgs900'
#mkdir $plotdir
#mkdir $path/modulewiseTruncation_10kevents

for dir in $path/$prefix; do
	name=$(basename $dir)
	count=$(ls $dir/260817*/0000/*.root | wc -l)
	module=$(echo "$name" | sed -E 's/.*truncated([^_]*)_.*/\1/')
	mergedfile="truncated${module}_10000events_merged.root"
	
	#echo $module $count

	#totalcount=$(python3 getEventCount.py -d "$dir/260817*/0000/*.root")
	#echo $module $count $totalcount	

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
	#hadd $path/modulewiseTruncation_10kevents/$mergedfile $dir/260817*/0000/*.root
	#ls $dir/*.root

	##### check merged file count
	echo $module $(python3 getEventCount.py -f $path/modulewiseTruncation_10kevents/$mergedfile)
	
	#mkdir $plotdir/$module
	#cp ../plotMaker/* $plotdir/$module 
	#cd $plotdir/$module
	#./makeHists.csh $path/modulewiseTruncation_10kevents/$mergedfile   
	#cd ..
	#cd ..



done
