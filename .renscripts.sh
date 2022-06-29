#!/bin/bash

# verbose
#rename -v 's/o/1/' ./*.mp3

# dry-run
rename -n 's/o/1/' ./*.mp3
echo "This is only a dry-run."
