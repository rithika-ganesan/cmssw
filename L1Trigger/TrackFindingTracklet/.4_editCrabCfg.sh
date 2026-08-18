#!/bin/bash

### Load truncation settings

which_truncate="$1"
nevents=$2
crabfile="crab_cfg.py"
sample_name="$3"

cd test
# edit request name
sed -i "s/config\.General\.requestName =.*/config\.General\.requestName = 'truncated${which_truncate^^}_${sample_name}_1510pre_${nevents}events'/" $crabfile 
# edit number of events
sed -i "s/config\.Data\.totalUnits =.*/config\.Data\.totalUnits = $nevents/" $crabfile
