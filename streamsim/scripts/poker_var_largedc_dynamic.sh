#!/usr/bin/env bash
# Run from directory ABOVE scripts

OUT_FILE="data/poker_var_largedc_dynamic.out"
IN_FILE="scripts/poker_var_largedc_dynamic.json"
SCRIPT=scripts/meansd.py
RND=$RANDOM
TMPJSONFILE="/tmp/poker_var_$RND.json"
TMPCOSTFILE="/tmp/poker_var_cost_$RND.out"
TMPDAYFILE="/tmp/poker_var_day_$RND.out"
TMPSESSFILE="/tmp/poker_var_sess_$RND.out"
TMPQOSFILE="/tmp/poker_var_qos_$RND.out"
rm -f $OUT_FILE
for servers in `seq 6`; do
    sed -e "s/XXXXXX/$servers/g" $IN_FILE | sed -e "s%DAYTMPFILE%$TMPDAYFILE%g" | sed -e "s%COSTTMPFILE%$TMPCOSTFILE%g" | sed -e "s%QOSTMPFILE%$TMPQOSFILE%g" | sed -e "s%SESSTMPFILE%$TMPSESSFILE%g"> $TMPJSONFILE
    src/streamsim.py $TMPJSONFILE
    echo -n $servers "" >> $OUT_FILE
    cat $TMPCOSTFILE | $SCRIPT | tr -d '\n' >> $OUT_FILE
    echo -n " " >> $OUT_FILE
    cat $TMPQOSFILE | $SCRIPT | tr -d '\n'>> $OUT_FILE
    echo -n " " >> $OUT_FILE
    cat $TMPSESSFILE | $SCRIPT | tr -d '\n'>> $OUT_FILE
    echo >> $OUT_FILE
rm -f $TMPJSONFILE $TMPCOSTFILE $TMPDAYFILE $TMPQOSFILE    
done
