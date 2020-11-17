from graphics import *
from data_parser import *
from print_func import *
import re
import os
import time
import math
import pyglet
import pygame
from pyglet import shapes
from PIL import Image, ImageGrab
from win32api import GetSystemMetrics

#Find monitor height dimension (subtract 19px to account for taskbar) and # of ouptut frames
win_h = GetSystemMetrics(1) - 19

#Initialize pygame's submodules for future use
pygame.init()
pygame.font.init()

#Inital data parsing and setup....
#Search base directory
basedir = os.path.dirname(os.getcwd())
dir = os.listdir(basedir)

#Check for valid excel file
for file in dir:
    match = re.search(r'(\d+\-\d+\-\d+)(\.xlsx)', file)
    if match != None:
        break
if match == None:
    print('Error: No file with name format 00-00-00.xlsx found!')
    sys.exit(0)
filename = str(match.group(1)) + str(match.group(2))

start = time.perf_counter()
#Parse data
mice, cages, conds = parse_data(filename)
sort_cages = sorted(cages.items(), key = lambda x: x[1].pri)  #sorted list of cage objects from which to print

#Calculate metrics for .txt output
total_mice = len(mice.keys())
total_cages = len(cages.keys())
total_litters = 0
total_pups = 0
total_pregnant = 0
for c in sort_cages:
    if c[1].pups > 0:
        total_litters += 1
        total_pups += c[1].pups
for m in mice.keys():
    if mice[m].pregnant:
        total_pregnant += 1

end = time.perf_counter()
print('Excel file parsed successfully: ', str('%.4f'%(end-start)) + 's')

start = time.perf_counter()
#Set up base layer dimensions based on number of cages for default (720,base_y) window
num_frames = math.ceil(len(cages)/40)

scale_f = float(win_h/1280)

for i in range(num_frames):
    #Code for Drawing Pillow Image side-by-side with original graphics.py code!
    win = GraphWin(filename, int(720*scale_f), win_h)
    #Create blank 720x1280 pyglet window and enable drawing obj
    # pygwin = pyglet.window.Window(720, 1280)
    pygwin = pygame.display.set_mode((720,1280))
    pygwin.fill('white')
    # @pygwin.event
    # def on_draw():
    #     pygwin.clear()
    #     print('draw!')


    c_idx = 40*i
    if i == (num_frames-1):
        cage_list = sort_cages[c_idx:]
    else:
        cage_list = sort_cages[c_idx:c_idx+40]

    #initalize first cage coordinates
    x1, y1 = 0, 0
    x2, y2 = 143, 159
    row_counter = 0 

    #loop to draw cages (base layer of rectangles), 144x160px
    for cage in cage_list:
        c = cage[1]
        r = Rectangle(Point(x1, y1), Point(x2,y2))
        r = update_cage(c,r,conds)
        # r.draw(win)

        # cage_batch = pyglet.graphics.Batch()
        # r2 = shapes.Rectangle(x=0, y=50, width=14, height=16, batch=cage_batch)
        # r2 = update_cage2(c, r2, conds)
        # r2.draw()
        # pygwin.flip()
        
        r2=0
        color = update_cage2(c, r2, conds, pygwin)
        r2 = pygame.draw.rect(pygwin, color, (x1, y1, 144, 160))
        r2 = pygame.draw.rect(pygwin, 'black', (x1, y1, 144, 160), 3)
        cage_text = gen_cage_text(c, r, scale_f)
        # for t in cage_text:
        #     t.draw(win)
        # print_mice(win, mice, c.mice, x1, y1, scale_f)
        x1 = x2
        x2 += 144
        row_counter+=1
        if row_counter > 4:     #reset coordinates for next row of cages
            x1, x2 = 0, 143
            y1 = y2
            y2 += 160
            row_counter = 0

    # cage_batch.draw()
    #Rescale tk objects to fit window size
    win.addtag_all('all')
    win.scale('all', 0, 0, scale_f, scale_f)
    win.postscript(file = 'graphic.eps', colormode = 'color')

    #Open postscript graphic file
    pic = Image.open('graphic.eps')
    pic.load(scale=10)

    #Set desired dimensions for rescaling eps conversion
    factor = max(720/pic.size[0], 1280/pic.size[1])
    final_size = (int(pic.size[0] * factor), int(pic.size[1] * factor))

    #Resize to fit target size
    pic = pic.resize(final_size, Image.ANTIALIAS)

    # pyglet.image.get_buffer_manager().get_color_buffer().save('../pygwin'+'-'+str(i)+'.png')
    # pyglet.app.run()
    # pygwin.close()
    # x = win.winfo_rootx()
    # y = win.winfo_rooty()
    # x1 = x + win.winfo_width()
    # y1 = y + win.winfo_height()
    # ImageGrab.grab().crop((x, y, x1, y1)).save('../grab'+ str(i) + '.png')

    # Save to PNG
    pic.save('../'+ match.group(1) + '-'+ str(i) + '.png')
    pygame.display.update()
    pygame.image.save(pygwin, '../pygwin'+'-'+str(i)+'.png')
    win.close()
    

end = time.perf_counter()
print('Colony graphic saved successfully: ', str('%.4f'%(end-start)) + 's')

start= time.perf_counter()
#Save colony stats to .txt file
col_txt = open('../'+'Colony_Data_'+ match.group(1) + '.txt', 'w')
print('Total Number of Cages:', total_cages,'\n', file = col_txt)
print('Total Number of Mice:', total_mice,'\n', file = col_txt)
print('Total Number of Litters:', total_litters,'\n', file = col_txt)
print('Total Number of Pups:', int(total_pups),'\n', file = col_txt)
print('Total Number of Pregancies:', total_pregnant, file = col_txt)
col_txt.close()

end = time.perf_counter()
print('Colony stat file saved successfully: ', str('%.4f'%(end-start)) + 's')
print('Graphic generation process complete!')