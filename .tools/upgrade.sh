#!/bin/bash

set -e -u -x

cd "$(dirname "$0")/.."

rm -f package-lock.json

ncu -u
npm update

uv pip compile -q --universal --allow-unsafe --strip-extras --no-annotate --no-header -U requirements.in -o requirements.txt
