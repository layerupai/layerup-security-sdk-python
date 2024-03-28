#!/bin/sh
rm -Rf build
rm -Rf dist
python setup.py sdist bdist_wheel
twine upload dist/*