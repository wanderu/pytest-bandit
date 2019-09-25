#!/usr/bin/env bash

rm -rf dist
# Assumes running in build venv with twine
python setup.py bdist_wheel
python setup.py sdist
twine upload dist/*
