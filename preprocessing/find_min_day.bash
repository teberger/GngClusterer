#!/bin/bash

if [ -e .temp_minday ]
then
    rm .temp_minday
fi

for i in $(ls -w 1 '../data')
do
    tail -1 ../data/$i >> .temp_minday
done

cat .temp_minday | sort | head -1
