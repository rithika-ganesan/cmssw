#!/bin/bash

#var=vmr
for var in pc mp tp tpd tre dr; do
	bash .truncate_crab.sh $var 5000
	cd test && crab submit crab_cfg.py
	echo "Submitted ${var^^}"
	echo "  "
	echo "  "
	cd ..
done
