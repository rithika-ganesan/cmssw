#!/bin/tcsh

if ($#argv == 1) then
  set inputFullFileName = $1
else
  echo "Enter the path to a single root file."
  exit(1)
endif

if ( -e $inputFullFileName) then
  echo "Processing ..."
else
  echo "ERROR: Input file $inputFullFileName not found"
  exit(1)
endif

# Get directory name
set dirName = `dirname $inputFullFileName`/
# Get file name without directory name
set fileName = `basename $inputFullFileName`
# Get stem of filename, removing ".root".
set inputFileStem = `echo $fileName | awk -F . '{print $1;}'`

set plotMacro = $CMSSW_BASE/src/L1Trigger/TrackFindingTracklet/scripts/myMacro/makeTrackPlots.C
\root -b -q ${plotMacro}'("'${inputFileStem}'","'${dirName}'")' #> myLog.log
exit