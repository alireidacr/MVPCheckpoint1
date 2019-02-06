set title "Mean Magnetisation vs Temperature"
set xrange [*:*]
set yrange [*:*]
set xlabel "Temperature"
set ylabel "Square of the Mean Magnetisation ( <M>^2)"
plot 'magnetisation.txt' with linespoints
