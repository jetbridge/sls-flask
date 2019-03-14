#!/bin/bash -e

# read -p "What is the name of your app? (lowercase): " name
name=basename $PWD

if [[ -z "$name" ]]; then exit 1; fi

# replace TEMPLATE in files
find TEMPLATE -type f -exec perl -i -pe s/TEMPLATE/$name/ {} \;

mv TEMPLATE $name
