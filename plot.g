set datafile separator ","
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
#set format x "%y-%m-%d %H:%M:%S"

set xlabel "date-time"
set ylabel "Atmospheric pressure [hPa]"

set terminal png
set output 'mpl115_timedomain.png'

plot 'mpl115.csv' using 1:2 w l
#pause -1 "hit Enter key"
