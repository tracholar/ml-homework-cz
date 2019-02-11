#!/usr/bin/env bash


for i in `seq 10`
do
    python main.py --role worker --server 0.0.0.0:10000  --port 10001 &
done

python main.py --role worker --server 0.0.0.0:10000  --port 10001