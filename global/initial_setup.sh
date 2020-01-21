#!/bin/bash

EXE=guess
if [ -L "$EXE" ]; then
    rm $EXE
fi

ln -s ../../src/guess_4.0.1/guess $EXE

if [ -d "output" ]; then
    rm -rf output
    mkdir output
fi

if [ -d "logs" ]; then
    rm -rf logs
    mkdir logs
fi
