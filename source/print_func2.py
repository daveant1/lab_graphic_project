import re
import math
import pygame

pygame.font.init()
FONT18 = pygame.font.SysFont("Times New Roman", 18)
FONT12 = pygame.font.SysFont("Times New Roman", 12)
FONT11 = pygame.font.SysFont("Times New Roman", 11)
FONT8 = pygame.font.SysFont("Times New Roman", 8)

#Function to update properties of cage shape based on conds dict
def get_cage_color(cage, conds):
    if isinstance(cage.status, str) and not cage.status.isspace() and cage.status in conds.keys():   #If status is string and not empty space, check for condition color
        return conds[cage.status][0]       #Fill rectangle to corresponding condition color
    else:
        return 'white'

#Function to construct cage text elements
def gen_cage_text2(cage, shape):
    tl=[]   #list of tuples of text objects with rect object dimension
    origin = shape.center    #Retrieve current coordinates
    x = origin[0]
    y = origin[1]

    #Draw Cage ID
    if len(cage.CID) > 5:
        pos = (x, y-65)
    elif len(cage.CID) > 3:
        pos = (x-43, y-65)
    else:
        pos = (x-50, y-65)
    #Initialize Text object, set area center, add tuple to list
    t = FONT18.render(cage.CID, True, 'black')
    t_area = t.get_rect()
    t_area.center = pos
    tl.append((t, t_area))

    #Draw Pup DOB and Wean Date
    if cage.pups > 0:
        dates = []
        date = str(cage.DOB)
        for i in range(2):
            #Reformat pup DOB or WD and construct pup text
            match = re.search(r'(\d*)\-(\d\d)\-(\d\d)', date)
            dates.append(match.group(2) + '/' + match.group(3) + '/' + match.group(1))
            date = str(cage.WD)

        dob_msg = str(int(cage.pups)) + ' pups DOB: ' + str(dates[0])
        t = FONT12.render(dob_msg, True, 'black')
        t_area = t.get_rect()
        t_area.center = (x, y+55)
        tl.append((t, t_area))

        wd_msg = 'Wean Date: ' + str(dates[1])
        t = FONT12.render(wd_msg, True, 'black')
        t_area = t.get_rect()
        t_area.center = (x, y+70)
        tl.append((t, t_area))
    return tl

#Function to update properties of mouse shape
def get_mouse_color(mouse):
    color = 'White'
    if isinstance(mouse.age, int) and (mouse.age > 275):
        color = 'Orange'
    if mouse.pregnant:
        color = 'Pink'
    return color

#Function to construct mouse text elements
def gen_mouse_text2(mouse, shape):
    tl=[]   #list of text objects to be drawn in main loop
    origin = shape.center    #Retrieve current coordinates
    x = origin[0]
    y = origin[1]

    #Draw Age
    if not str(mouse.age).isspace():
        if mouse.runt:
            t = FONT8.render(str(mouse.age), True, 'black')
        else:
            t = FONT12.render(str(mouse.age), True, 'black')
        t_area = t.get_rect()
        t_area.center = shape.center
        tl.append((t, t_area))

    #Draw Mouse ID
    if mouse.genotyped:
        t = FONT11.render(mouse.ID, True, 'yellow')
    else:
        t = FONT11.render(mouse.ID, True, 'black')
    t_area = t.get_rect()
    t_area.center = (x, y+23)
    tl.append((t, t_area))
    return tl

#Draw all mice shapes and apply relevant properties
#initalize coordinates (x and y always represent center of shape)
#inital coordinate: (o_x, o_y) is the top left corner of current cage cell
def print_mice2(pygwin, mice_dict, mouse_list, o_x, o_y):
    x = o_x + 24
    y = o_y + 50
    m_count = 0    #Count of printed mice (for coordinate calculation)
    for idx in mouse_list:
        curr = mice_dict[idx]
        color = get_mouse_color(curr)
        if curr.runt:
            rad = 10
        else:
            rad = 16
        if curr.sex:
            sh = pygame.draw.rect(pygwin, color, (x-rad, y-rad, 2*rad, 2*rad))
            sh = pygame.draw.rect(pygwin, 'black', (x-rad, y-rad, 2*rad, 2*rad), width = 1)
            # Check Ear Tag status and print border if no ear tag
            if not curr.ET:
                sh = pygame.draw.rect(pygwin, 'red', (x-rad, y-rad, 2*rad, 2*rad), width = 3)
        else:
            sh = pygame.draw.circle(pygwin, color, (x,y), rad)
            sh = pygame.draw.circle(pygwin, 'black', (x,y), rad, width = 1)
            if not curr.ET:
                sh = pygame.draw.circle(pygwin, 'red', (x,y), rad, width = 3)

        mouse_text = gen_mouse_text2(curr, sh)   #generate text elements for mouse as list
        for t in mouse_text:
            pygwin.blit(t[0], t[1])

        #print sacked symbol (cross)
        if curr.sacked in ('p', 's'):
            pygame.draw.line(pygwin, 'black', (x-rad, y+rad), (x+rad, y-rad), 1)
            if curr.sacked == 's':
                pygame.draw.line(pygwin, 'black', (x-rad, y-rad), (x+rad, y+rad), 1)

        m_count+=1
        if(m_count==3):
            x -= 96
            y += 48
        else:
            x += 48
