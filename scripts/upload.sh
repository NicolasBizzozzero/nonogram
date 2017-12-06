#/bin/bash

python setup.py sdist bdist_wheel
~/.local/bin/twine upload dist/*
