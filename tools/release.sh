set -xe

rm -rf dist # Clean dist folder
python setup.py sdist # Build package
twine upload dist/* # Upload package
