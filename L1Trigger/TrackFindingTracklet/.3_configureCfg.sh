#!/bin/bash

var="$1"
nevents=$2
additional="$3"
if [ -n "$additional" ]; then
    additional="_$3"
fi

output_filename="L1TrkNtuple_Truncated${var^^}_$2events$additional.root"
cfgfile='test/L1TrackNtupleMaker_cfg.py'

sed -i "s/fileName = cms\.string('[^']*\.root')/fileName = cms.string('${output_filename}')/" $cfgfile

sed -i "s/process\.maxEvents = .*/process\.maxEvents = cms\.untracked\.PSet(input = cms\.untracked\.int32($nevents))/" $cfgfile
