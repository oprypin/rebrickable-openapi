#!/bin/bash

set -e -u -x
cd "$(dirname "$0")/.."

mkdir -p rebrickable_api
touch rebrickable_api/__init__.py

node_modules/.bin/prettier --print-width=1000 -w *.yaml

ruff format tests/ example.py
ruff check --fix tests/
