set term postscript color enhanced eps 20 dashlength 2 rounded
set size 1,0.8

FILE="poker_var_user.out"

set xlabel "No users"
set ylabel "Data cost/user"
set style line 1 lw 6 lt 1
set style line 2 lw 4 lt 2 

plot FILE using ($1):($5)/($1) title "Data download cost" w l, \
    FILE using ($1):($4)/($1) title "Data transfer cost" w l
