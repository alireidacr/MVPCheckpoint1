set title "Mean Magnetisation vs Temperature"
set xrange [*:*]
set yrange [*:*]
set xlabel "Temperature"
set ylabel "Absolute Value of the Mean Magnetisation"
plot 'Data/magnetisation.txt' with linespoints
