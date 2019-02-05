set palette color
set cbrange[-1:1]
plot 'output.txt' w image
while (1) {
    pause 0.5
    replot
}
