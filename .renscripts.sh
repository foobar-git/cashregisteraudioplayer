#!/bin/bash

# verbose
#rename -v 's/0//' ./audio/*.mp3

# dry-run
rename -n 's/0//' ./audio/*.mp3
echo "This is only a dry-run."
