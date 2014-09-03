set term postscript color enhanced eps 20 dashlength 2 rounded
set size 1,0.8

FILE="poker_var_user.out"

set xlabel "No users"
set ylabel "RTT quintile"
set style line 1 lw 6 lt 1
set style line 2 lw 4 lt 2 

plot FILE using ($1):($18)/1000000 title "Unmanaged first quintile" w l, \
    FILE using ($1):($19)/1000000 title "Unmanaged second quintile" w l, \
FILE using ($1):($20)/1000000 title "Unmanaged third quintile" w l, \
FILE using ($1):($21)/1000000 title "Unmanaged fourth quintile" w l, \
FILE using ($1):($22)/1000000 title "Unmanaged fifth quintile" w l, \
