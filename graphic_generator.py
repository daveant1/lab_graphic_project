from graphics import *
from data_parser import *

win = GraphWin('Date Lab Graphic', 720, 1280)
c = Circle(Point(50,50), 10)
c.draw(win)
win.getMouse() # pause for click in window
#win.close()

mice, cages = parse_data()
for c in cages:

    #for m in c.mice:
