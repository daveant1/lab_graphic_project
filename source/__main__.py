from data_parser import *
from print_func import *
from log import *
from error import *
import re
import os
import sys
import time
import math
import pygame

def main():
    #Initialize pygame's submodules for future use
    pygame.init()

    #Parse filename
    match_fn = parse_filename()

    #Detect, autocorrect and log errors
    detect(match_fn.group(0))

    #Inital data parsing and setup....
    start = time.perf_counter()
    #Parse data
    mice, cages, conds = parse_data('new.xlsx')
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

    st_parse(str('%.4f'%(end-start)))

    #Print graphics
    start = time.perf_counter()
    #Set up base layer dimensions based on number of cages for default (720,base_y) window
    num_frames = math.ceil(len(cages)/40)
    for i in range(num_frames):
        #Create blank 720x1280 pygame Surface
        pygwin = pygame.display.set_mode((720,1280))
        pygwin.fill('white')
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
            color = get_cage_color(c, conds)
            r2 = pygame.draw.rect(pygwin, color, (x1, y1, 144, 160), border_radius = 10)
            r2 = pygame.draw.rect(pygwin, 'black', (x1, y1, 144, 160), width = 2, border_radius = 10)

            cage_text = gen_cage_text(c, r2)
            for t in cage_text:
                pygwin.blit(t[0], t[1])
            print_mice(pygwin, mice, c.mice, x1, y1)
            x1 = x2
            x2 += 144
            row_counter+=1
            if row_counter > 4:     #reset coordinates for next row of cages
                x1, x2 = 0, 143
                y1 = y2
                y2 += 160
                row_counter = 0

        # Update display and save to PNG
        pygame.display.update()
        pygame.image.save(pygwin, './'+ match_fn.group(1) + match_fn.group(2) + '-'+ str(i) + '.png')
    end = time.perf_counter()

    st_graph(str('%.4f'%(end-start)))

    #Generate colony stat file
    start= time.perf_counter()
    col_txt = open('./'+'Colony_Data_'+ match_fn.group(1) + match_fn.group(2) + '.txt', 'w')
    print('Total Number of Cages:', total_cages,'\n', file = col_txt)
    print('Total Number of Mice:', total_mice,'\n', file = col_txt)
    print('Total Number of Litters:', total_litters,'\n', file = col_txt)
    print('Total Number of Pups:', int(total_pups),'\n', file = col_txt)
    print('Total Number of Pregancies:', total_pregnant, file = col_txt)
    col_txt.close()
    end = time.perf_counter()

    st_colony_data(str('%.4f'%(end-start)))
    st_done()

#Entry point for pyinstaller
if __name__ == "__main__":
    main()
