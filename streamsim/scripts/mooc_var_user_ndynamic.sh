#!/usr/bin/env bash
# Run from directory ABOVE scripts

OUT_FILE="data/mooc_var_user_ndynamic.out"
IN_FILE="scripts/mooc_var_user_ndynamic.json"
SCRIPT=scripts/meansd.py
RND=$RANDOM
TMPJSONFILE="/tmp/mooc_var_$RND.json"
TMPCOSTFILE="/tmp/mooc_var_cost_$RND.out"
TMPDAYFILE="/tmp/mooc_var_day_$RND.out"
TMPSESSFILE="/tmp/mooc_var_sess_$RND.out"
TMPQOSFILE="/tmp/mooc_var_qos_$RND.out"
rm -f $OUT_FILE
for users in "250" "500" "750" "1000"; do
    sed -e "s/XXXXXX/$users/g" $IN_FILE | sed -e "s%DAYTMPFILE%$TMPDAYFILE%g" | sed -e "s%COSTTMPFILE%$TMPCOSTFILE%g" | sed -e "s%QOSTMPFILE%$TMPQOSFILE%g" | sed -e "s%SESSTMPFILE%$TMPSESSFILE%g"> $TMPJSONFILE
    src/streamsim.py $TMPJSONFILE
    echo -n $users "" >> $OUT_FILE
    cat $TMPCOSTFILE | $SCRIPT | tr -d '\n' >> $OUT_FILE
    echo -n " " >> $OUT_FILE
    cat $TMPQOSFILE | $SCRIPT | tr -d '\n'>> $OUT_FILE
    echo -n " " >> $OUT_FILE
    cat $TMPSESSFILE | $SCRIPT | tr -d '\n'>> $OUT_FILE
    echo >> $OUT_FILE
rm -f $TMPJSONFILE $TMPCOSTFILE $TMPDAYFILE $TMPQOSFILE    
done
