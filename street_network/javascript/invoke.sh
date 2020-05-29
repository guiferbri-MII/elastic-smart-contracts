
#!/bin/bash


./register.sh $1 &
WA=$!
wait $WA
node listener.js launchListener -n $1 -m $2 &
for i in $(seq 1 1 $1)
do 
    node invoke.js launchDetections -n $1 -m $2 -s $i
done