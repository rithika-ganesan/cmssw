#!/bin/bash

#var=vmr
for var in none all pc mp tp tpd tre dr; do
	bash .truncate_crab.sh $var 10000
	#cd test && crab submit crab_cfg.py
	echo "Submitted ${var^^}"
	echo "  "
	echo "  "
	#cd ..
done
