import biggles

x = [1, 2, 3, 4, 5]
y = [5, 4, 3, 2, 1]
p = biggles.FramedPlot()
p += biggles.Curve(x, y)
p.show()
