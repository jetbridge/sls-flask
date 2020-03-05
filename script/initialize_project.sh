#!/bin/bash -e

DEFAULT_NAME=`basename $PWD`
read -p "What is the name of your app? [$DEFAULT_NAME]: " name
name=${name:-$DEFAULT_NAME}

if [[ -z "$name" ]]; then exit 1; fi

subst="perl -i -pe s/TEMPLATE/$name/g"

# replace TEMPLATE in files
find TEMPLATE -type f -exec $subst {} \;
$subst serverless.yml package.json app.py tox.ini README.md .github/workflows/pythonapp.yml doc/conf.py doc/Makefile Makefile mypy.ini pyproject.toml

# rename
mv TEMPLATE $name
mv api.paw ${name}.paw

poetry install

echo ""
echo "Project $name ready!"
echo ""
echo "Next steps:"
echo "  $ make run"
echo "  Open http://127.0.0.1:5000/api/swagger in browser"
echo ""
echo "To deploy:"
echo "  $ sls deploy"
echo ""
