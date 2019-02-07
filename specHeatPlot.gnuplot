set title "Specific Heat Capacity per Spin vs Temperature"
set xrange [*:*]
set yrange [*:*]
set xlabel "Temperature"
set ylabel "Specific Heat Capacity per Spin"
plot 'Data/specHeat.txt' using 1:2:3 with errorlines
