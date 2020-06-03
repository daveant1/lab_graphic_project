from graphics import *
from data_parser import *
from print_func import *
import math

#Inital data parsing and setup
filename = '05-28-2020.xlsx'
mice, cages = parse_data(filename)

#Set up base layer dimensions based on number of cages
base_y = math.ceil(len(cages)/5) * 160    #calculate base y dimension (force int type)
win = GraphWin(filename, 720, base_y)

#initalize first cage coordinates
#box_count = len(cages)
x1, y1 = 0, 0
x2, y2 = 143, 159
row_counter = 0   #a counter to realize when we have finished drawing a row of cages

#loop to draw cages (base layer of rectangles)
#Each cage is 144x160 px by default
for c in cages:
    r = Rectangle(Point(x1, y1), Point(x2,y2))   #generate new cage
    r = update_cage(c,r)    #update cage color
    r.draw(win)
    cage_text = gen_cage_text(c, r)
    for t in cage_text:
        t.draw(win)
    print_mice(win, mice, c.mice, x1, y1)
    x1 = x2
    x2 += 144
    row_counter+=1
    if row_counter > 4:     #reset x coordinates for next row of cages
        x1, x2 = 0, 143
        y1 = y2
        y2 += 160
        row_counter = 0
win.getMouse()
