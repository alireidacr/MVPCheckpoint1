set palette color
set palette rgbformula 30,13,10
set cblabel "Spin"
unset cbtics
set xrange [0:20]
set yrange [0:20]
set cbrange[-1:1]
set title "Visualisation of the Ising Model"
plot 'output.txt' w image
while (1) {
    pause 0.5
    replot
}
