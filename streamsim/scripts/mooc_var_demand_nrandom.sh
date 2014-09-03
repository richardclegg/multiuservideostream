#!/usr/bin/env bash
# Run from directory ABOVE scripts

OUT_FILE="data/mooc_var_demand_nrandom.out"
IN_FILE="scripts/mooc_var_demand_nrandom.json"
SCRIPT=scripts/meansd.py
RND=$RANDOM
TMPJSONFILE="/tmp/mooc_var_$RND.json"
TMPCOSTFILE="/tmp/mooc_var_cost_$RND.out"
TMPDAYFILE="/tmp/mooc_var_day_$RND.out"
TMPSESSFILE="/tmp/mooc_var_sess_$RND.out"
TMPQOSFILE="/tmp/mooc_var_qos_$RND.out"
rm -f $OUT_FILE
for demand in "1000.0" "2000.0" "3000.0" "4000.0" "5000.0"; do
    sed -e "s/XXXXXX/$demand/g" $IN_FILE | sed -e "s%DAYTMPFILE%$TMPDAYFILE%g" | sed -e "s%COSTTMPFILE%$TMPCOSTFILE%g" | sed -e "s%QOSTMPFILE%$TMPQOSFILE%g" | sed -e "s%SESSTMPFILE%$TMPSESSFILE%g"> $TMPJSONFILE
    src/streamsim.py $TMPJSONFILE
    echo -n $demand "" >> $OUT_FILE
    cat $TMPCOSTFILE | $SCRIPT | tr -d '\n' >> $OUT_FILE
    echo -n " " >> $OUT_FILE
    cat $TMPQOSFILE | $SCRIPT | tr -d '\n'>> $OUT_FILE
    echo -n " " >> $OUT_FILE
    cat $TMPSESSFILE | $SCRIPT | tr -d '\n'>> $OUT_FILE
    echo >> $OUT_FILE
rm -f $TMPJSONFILE $TMPCOSTFILE $TMPDAYFILE $TMPQOSFILE    
done
