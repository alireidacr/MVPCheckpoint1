set title "Mean Energy vs Temperature"
set xrange [*:*]
set yrange [*:*]
set xlabel "Temperature"
set ylabel "Mean System Energy"
plot 'Data/magnetisation.txt' with linespoints
