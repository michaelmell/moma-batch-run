#!/bin/bash

### Run this to create the conda environment for the build ###
# conda create -n "build__moma_batch_run" python=3.10 pyinstaller=5.6 pyyaml=6.0

conda activate build__moma_batch_run

rm -rf standalone_build/dist/
mkdir -p standalone_build/dist/
pyinstaller -y --clean --workpath standalone_build  --distpath standalone_build/dist/ --name moma_batch_run --onefile moma_batch_run.py
