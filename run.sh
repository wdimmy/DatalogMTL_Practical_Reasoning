#!/bin/bash
input=$3
while IFS= read -r line
do
  echo "$line"
  echo $4
  python run_2.py --datapath $1 --rulepath $2 --fact "$line" $4
done < "$input"