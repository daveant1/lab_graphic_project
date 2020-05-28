from graphics import *
from data_parser import *
import math

#Inital data parsing and setup
filename = 'dummy_data.xlsx'
mice, cages = parse_data(filename)

cages = range(0,31)

#Set up base layer dimensions based on number of cages
base_y = math.ceil(len(cages)/5) * 160    #calculate base y dimension (force int type)
win = GraphWin(filename, 720, base_y)

#initalize first cage coordinates
box_count = len(cages)
x1, y1 = 0, 0
x2, y2 = 143, 159
row_counter = 0   #a counter to realize when we have finished drawing a row of cages

#loop to draw cages (base layer of rectangles)
#Each cage is 144x160 px by default
for i in range(0, box_count):
# # for y in range(-1, base_y-160, 160):     #base_y-160 to account for last box
# #     for x in range(-1, 576, 144):        #720-144=576
#         #dim = [Point(x,y), Point(x + 144, y + 160)]  #dimension list for rectangle
#         print(Point(x,y), Point(x + 144, y + 160))
#         r = Rectangle(Point(x,y), Point(x + 144, y + 160))
    r = Rectangle(Point(x1, y1), Point(x2,y2))
    r.setFill('DarkGray')
    r.draw(win)
    x1 = x2
    x2 += 144
    row_counter+=1
    if row_counter > 4:     #reset x coordinates for next row of cages
        x1, x2 = 0, 143
        y1 = y2
        y2 += 160
        row_counter = 0
win.getMouse() # pause for click in window

filename = 'dummy_data.xlsx'
mice, cages = parse_data(filename)
