from graphics import *
from data_parser import *
from print_func import *
import re
import os
import math
from win32api import GetSystemMetrics

#Find monitor height dimension (subtract 19px to account for taskbar)
win_h = GetSystemMetrics(1) - 19

#Inital data parsing and setup
dir = os.listdir()
#Check for valid excel file
for file in dir:
    match = re.search(r'(\d\d\-\d\d\-\d\d)(\.xlsx)', file)
    if match != None:
        break
filename = str(match.group(1)) + str(match.group(2))
mice, cages = parse_data(filename)

#Set up base layer dimensions based on number of cages for default (720,base_y) window
base_y = math.ceil(len(cages)/5) * 160    #calculate base_y dimension (force int type)
scale_f = float(win_h/base_y)
win = GraphWin(filename, int(720*scale_f), win_h)

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
    cage_text = gen_cage_text(c, r, scale_f)
    for t in cage_text:
        t.draw(win)
    print_mice(win, mice, c.mice, x1, y1, scale_f)
    x1 = x2
    x2 += 144
    row_counter+=1
    if row_counter > 4:     #reset x coordinates for next row of cages
        x1, x2 = 0, 143
        y1 = y2
        y2 += 160
        row_counter = 0

#Rescale objects in window to fit window size
win.addtag_all('all')
win.scale('all', 0, 0, scale_f, scale_f)
# print(scale_f)
# print(win.cget('width'), win.cget('height'))
win.postscript(file = 'image.eps', colormode = 'color')

from PIL import Image

#Set desired dimensions for rescaling eps conversion
pic_size = (720, base_y)

pic = Image.open('image.eps')
pic.load(scale=10)

factor = max(pic_size[0] / pic.size[0],
            pic_size[1] / pic.size[1])
final_size = (int(pic.size[0] * factor), int(pic.size[1] * factor))

#Resize to fit the target size
pic = pic.resize(final_size, Image.ANTIALIAS)

# Save to PNG
pic.save('../'+ match.group(1) + '.png')
win.getMouse()
