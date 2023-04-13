#!/usr/bin/env bash

python3 -m jupyter nbconvert \
    --to pdf \
    --template default.tplx \
    --output-dir dist \
    ./labs/MP_Lesson4_2023_Peshekhonov_Ivan.ipynb