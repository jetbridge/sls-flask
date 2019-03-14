#!/bin/bash -e

# read -p "What is the name of your app? (lowercase): " name
name=`basename $PWD`

if [[ -z "$name" ]]; then exit 1; fi

alias subst=perl -i -pe s/TEMPLATE/$name/

# replace TEMPLATE in files
find TEMPLATE -type f -exec subst {} \;
subst serverless.yml
subst package.json

mv TEMPLATE $name
echo " ---- "
echo ""
echo "Project $name ready!"
echo ""
echo "Next steps:"
echo "  pipenv shell"
echo "  flask run --reload"
echo ""
echo "To deploy:"
echo "  sls deploy"
