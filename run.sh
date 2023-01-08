#!/bin/bash
input=$3
while IFS= read -r line
do
  python run_2.py --datapath $1 --rulepath $2 --fact "$line"
done < "$input"