set title "Susceptibility vs Temperature"
set xrange [*:*]
set yrange [*:*]
set xlabel "Temperature"
set ylabel "Susceptibility"
plot 'Data/susceptibility.txt' with linespoints
