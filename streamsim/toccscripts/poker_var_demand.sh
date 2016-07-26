#!/usr/bin/env bash
# Run from directory ABOVE toccscripts

OUT_FILE="toccdata/poker_var_demand_ndynamic.out"
IN_FILE="toccscripts/poker_var_demand_ndynamic.json"
toccscripT=toccscripts/meansd.py
RND=$RANDOM
TMPJSONFILE="/tmp/poker_var_$RND.json"
TMPCOSTFILE="/tmp/poker_var_cost_$RND.out"
TMPDAYFILE="/tmp/poker_var_day_$RND.out"
TMPSESSFILE="/tmp/poker_var_sess_$RND.out"
TMPQOSFILE="/tmp/poker_var_qos_$RND.out"
rm -f $OUT_FILE
for demand in "1000.0" "2000.0" "3000.0" "4000.0" "5000.0"; do
    sed -e "s/XXXXXX/$demand/g" $IN_FILE | sed -e "s%DAYTMPFILE%$TMPDAYFILE%g" | sed -e "s%COSTTMPFILE%$TMPCOSTFILE%g" | sed -e "s%QOSTMPFILE%$TMPQOSFILE%g" | sed -e "s%SESSTMPFILE%$TMPSESSFILE%g"> $TMPJSONFILE
    src/streamsim.py $TMPJSONFILE
    echo -n $demand "" >> $OUT_FILE
    cat $TMPCOSTFILE | $toccscripT | tr -d '\n' >> $OUT_FILE
    echo -n " " >> $OUT_FILE
    cat $TMPQOSFILE | $toccscripT | tr -d '\n'>> $OUT_FILE
    echo -n " " >> $OUT_FILE
    cat $TMPSESSFILE | $toccscripT | tr -d '\n'>> $OUT_FILE
    echo >> $OUT_FILE
rm -f $TMPJSONFILE $TMPCOSTFILE $TMPDAYFILE $TMPQOSFILE    
done
OUT_FILE="toccdata/poker_var_demand_nrandom.out"
IN_FILE="toccscripts/poker_var_demand_nrandom.json"
rm -f $OUT_FILE
for demand in "1000.0" "2000.0" "3000.0" "4000.0" "5000.0"; do
    sed -e "s/XXXXXX/$demand/g" $IN_FILE | sed -e "s%DAYTMPFILE%$TMPDAYFILE%g" | sed -e "s%COSTTMPFILE%$TMPCOSTFILE%g" | sed -e "s%QOSTMPFILE%$TMPQOSFILE%g" | sed -e "s%SESSTMPFILE%$TMPSESSFILE%g"> $TMPJSONFILE
    src/streamsim.py $TMPJSONFILE
    echo -n $demand "" >> $OUT_FILE
    cat $TMPCOSTFILE | $toccscripT | tr -d '\n' >> $OUT_FILE
    echo -n " " >> $OUT_FILE
    cat $TMPQOSFILE | $toccscripT | tr -d '\n'>> $OUT_FILE
    echo -n " " >> $OUT_FILE
    cat $TMPSESSFILE | $toccscripT | tr -d '\n'>> $OUT_FILE
    echo >> $OUT_FILE
rm -f $TMPJSONFILE $TMPCOSTFILE $TMPDAYFILE $TMPQOSFILE    
done
OUT_FILE="toccdata/poker_var_demand_nstatic.out"
IN_FILE="toccscripts/poker_var_demand_nstatic.json"
rm -f $OUT_FILE
for demand in "1000.0" "2000.0" "3000.0" "4000.0" "5000.0"; do
    sed -e "s/XXXXXX/$demand/g" $IN_FILE | sed -e "s%DAYTMPFILE%$TMPDAYFILE%g" | sed -e "s%COSTTMPFILE%$TMPCOSTFILE%g" | sed -e "s%QOSTMPFILE%$TMPQOSFILE%g" | sed -e "s%SESSTMPFILE%$TMPSESSFILE%g"> $TMPJSONFILE
    src/streamsim.py $TMPJSONFILE
    echo -n $demand "" >> $OUT_FILE
    cat $TMPCOSTFILE | $toccscripT | tr -d '\n' >> $OUT_FILE
    echo -n " " >> $OUT_FILE
    cat $TMPQOSFILE | $toccscripT | tr -d '\n'>> $OUT_FILE
    echo -n " " >> $OUT_FILE
    cat $TMPSESSFILE | $toccscripT | tr -d '\n'>> $OUT_FILE
    echo >> $OUT_FILE
rm -f $TMPJSONFILE $TMPCOSTFILE $TMPDAYFILE $TMPQOSFILE    
done
