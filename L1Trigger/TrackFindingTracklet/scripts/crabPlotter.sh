#!/bin/bash

#path='/eos/user/r/rganesan/HTo2LongLivedTo4mu_MH-125_MFF-25_CTau-1500mm_TuneCP5_14TeV-pythia8'
path='/eos/user/r/rganesan/HTo2LongLivedTo4mu_MH-125_MFF-12_CTau-900mm_TuneCP5_14TeV-pythia8'
#path='/eos/user/r/rganesan/DisplacedSUSY_stopToBottom_M-800_50mm_TuneCP5_14TeV-pythia8'
prefix='crab_truncated*10000*'

plotdir='../plots/truncPlots_crab_10k-events_Higgs900'
#mkdir $plotdir
#mkdir $path/modulewiseTruncation_10kevents

echo $(pwd)

for dir in $path/$prefix; do
	name=$(basename $dir)
	count=$(ls $dir/*/0000/*.root | wc -l)
	module=$(echo "$name" | sed -E 's/.*truncated([^_]*)_.*/\1/')

	totalcount=$(python3 getEventCount.py -d "$dir/*/0000/*.root")
	#echo $module $count $totalcount	

	# mergedfile="truncated${module}_${totalcount}events_merged.root"
	mergedfile="truncated${module}_10000events_merged.root"
	echo $module $totalcount $mergedfile


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
	#hadd $path/modulewiseTruncation_50kevents/$mergedfile $dir/*/0000/*.root
	#ls $dir/*.root

	##### check merged file count
	#echo $module $(python3 getEventCount.py -f $path/modulewiseTruncation_50kevents/$mergedfile)
	
	mkdir $plotdir/$module
	cp ../plotMaker/* $plotdir/$module 
	# echo $module
	cd $plotdir/$module

	./makeHists.csh $path/modulewiseTruncation_10kevents/$mergedfile

	# # if [[ "$module" == "DR" || "$module" == "NONE" ]]; then
	# # 	./makeHists.csh $path/modulewiseTruncation_50kevents/$mergedfile
	# # 	echo $module  
	# # fi
	cd ../..
	cd ../scripts



done
