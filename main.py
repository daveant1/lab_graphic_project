from graphics import *
from data_parser import *
from print_func import *
import re
import os
import math

#Inital data parsing and setup
dir = os.listdir()
#Check for valid excel file
for file in dir:
    match = re.search(r'\w\w\-\w\w\-\w\w\.xlsx', file)
    if match != None:
        break
filename = str(match.group())
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
win.postscript(file = 'image.eps', colormode = 'color')
# from PIL import Image
# output = Image.open("05-28-20.eps")
# #convert = output.convert('RGBA')
# output.save("image.png")
from PIL import Image

pic_size = (720, base_y)

# Load the EPS at 10 times whatever size Pillow thinks it should be
# (Experimentaton suggests that scale=1 means 72 DPI but that would
#  make 600 DPI scale=8⅓ and Pillow requires an integer)
pic = Image.open('image.eps')
pic.load(scale=10)

# Ensure scaling can anti-alias by converting 1-bit or paletted images
# if pic.mode in ('P', '1'):
#     pic = pic.convert("RGB")

# Calculate the new size, preserving the aspect ratio
factor = min(pic_size[0] / pic.size[0],
            pic_size[1] / pic.size[1])
final_size = (int(pic.size[0] * factor), int(pic.size[1] * factor))

# Resize to fit the target size
pic = pic.resize(final_size, Image.ANTIALIAS)

# Save to PNG
pic.save(filename + '.png')
win.getMouse()
