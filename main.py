from graphics import *
from data_parser import *
from print_func import *
from time import perf_counter
import re
import os
import math
from PIL import Image
from win32api import GetSystemMetrics

#Find monitor height dimension (subtract 19px to account for taskbar) and # of ouptut frames
win_h = GetSystemMetrics(1) - 19

#Inital data parsing and setup
basename = os.path.dirname(os.getcwd())
dir = os.listdir(basename)

#Check for valid excel file
for file in dir:
    match = re.search(r'(\d+\-\d+\-\d+)(\.xlsx)', file)
    if match != None:
        break
if match == None:
    print('Error: No file with name format 00-00-00.xlsx found!')
    sys.exit(0)
filename = str(match.group(1)) + str(match.group(2))

mice, cages = parse_data(filename)
total_mice = len(mice.keys())
total_cages = len(cages)
total_litters = 0
total_pups = 0
total_pregnant = 0
for c in cages:
    if c.pups > 0:
        total_litters += 1
        total_pups += c.pups
    if c.status == 'PREGNANT':
        total_pregnant += 1

# start = perf_counter()
#Set up base layer dimensions based on number of cages for default (720,base_y) window
num_frames = math.ceil(len(cages)/40)

scale_f = float(win_h/1280)

for i in range(num_frames):
    win = GraphWin(filename, int(720*scale_f), win_h)

    c_idx = 40*i
    if i == (num_frames-1):
        cage_list = cages[c_idx:]
    else:
        cage_list = cages[c_idx:c_idx+40]

    #initalize first cage coordinates
    x1, y1 = 0, 0
    x2, y2 = 143, 159
    row_counter = 0   #a counter to realize when we have finished drawing a row of cages

    #loop to draw cages (base layer of rectangles)
    #Each cage is 144x160 px by default
    for c in cage_list:
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

    #Set desired dimensions for rescaling eps conversion
    pic = Image.open('image.eps')
    pic.load(scale=10)

    factor = max(720/pic.size[0], 1280/pic.size[1])
    final_size = (int(pic.size[0] * factor), int(pic.size[1] * factor))

    #Resize to fit the target size
    pic = pic.resize(final_size, Image.ANTIALIAS)

    # Save to PNG
    pic.save('../'+ match.group(1) + '-'+ str(i) + '.png')
    win.close()

col_txt = open('../'+'Colony_Data_'+ match.group(1) + '.txt', 'w')
print('Total Number of Cages:', total_cages,'\n', file = col_txt)
print('Total Number of Mice:', total_mice,'\n', file = col_txt)
print('Total Number of Litters:', total_litters,'\n', file = col_txt)
print('Total Number of Pups:', int(total_pups),'\n', file = col_txt)
print('Total Number of Pregancies:', total_pregnant, file = col_txt)
col_txt.close()
# end = perf_counter()
# print('printing time:', end-start)
