set title "Susceptibility vs Temperature"
set xrange [*:*]
set yrange [*:*]
set xlabel "Temperature"
set ylabel "Susceptibility"
plot 'susceptibility.txt' with linespoints
