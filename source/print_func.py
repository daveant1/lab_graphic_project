#Module that utilizes pygame to draw graphics
import re
import pygame

pygame.font.init()
FONT18 = pygame.font.SysFont("Times New Roman", 18)
FONT12 = pygame.font.SysFont("Times New Roman", 12)
FONT11 = pygame.font.SysFont("Times New Roman", 11)
FONT8 = pygame.font.SysFont("Times New Roman", 8)

#Function to reformat date to visible text format 00/00/00
def reformat_date (date):
    match = re.search(r'(\d\d\d\d)\-(\d\d)\-(\d\d)', date)
    if match:
        return (match.group(2) + '/' + match.group(3) + '/' + match.group(1))
    else:
        return None

#Function to construct cage text elements
def gen_cage_text(cage, shape):
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
        dob = reformat_date(str(cage.DOB))
        dob_msg = str(int(cage.pups)) + ' pups DOB: ' + dob
        t = FONT12.render(dob_msg, True, 'black')
        t_area = t.get_rect()
        t_area.center = (x, y+58)
        tl.append((t, t_area))

        wd = reformat_date(str(cage.WD))
        if wd:
            wd_msg = 'Wean Date: ' + wd
            t = FONT12.render(wd_msg, True, 'black')
            t_area = t.get_rect()
            t_area.center = (x, y+71)
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
def gen_mouse_text(mouse, shape, o_x, o_y):
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
        t = FONT11.render(mouse.ID, True, 'black', 'yellow')
    else:
        t = FONT11.render(mouse.ID, True, 'black')
    t_area = t.get_rect()
    t_area.center = (x, y+23)
    tl.append((t, t_area))

    #Draw mouse date of death (DOD)
    death_date = reformat_date(str(mouse.DOD)) 
    if (death_date):
        if mouse.sacked == 's':
            cod = 'Sacked'
        else:
            cod = 'Died'
        death_msg = cod + ': ' + death_date
        t = FONT12.render(death_msg, True, 'black')
        t_area = t.get_rect()
        t_area.center = (o_x + 71, o_y + 124)           #Use o_x, o_y (coords of top left of cage) as reference point
        tl.append((t, t_area))                        #y=79 for center + 45 for offset = 124; x = 71 for center
    
    return tl

#Draw all mice shapes and apply relevant properties
#initalize coordinates (x and y always represent center of shape)
#inital coordinate: (o_x, o_y) is the top left corner of current cage cell
def print_mice(pygwin, mice_dict, mouse_list, o_x, o_y):
    x = o_x + 24
    y = o_y + 42
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

        mouse_text = gen_mouse_text(curr, sh, o_x, o_y)   #generate text elements for mouse as list
        for t in mouse_text:
            pygwin.blit(t[0], t[1])

        #print sacked symbol (cross)
        if curr.sacked in ('p', 's', 'd'):
            pygame.draw.line(pygwin, 'black', (x-rad, y+rad), (x+rad, y-rad), 1)
            if curr.sacked != 'p':
                pygame.draw.line(pygwin, 'black', (x-rad, y-rad), (x+rad, y+rad), 1)

        m_count+=1
        if(m_count==3):
            x -= 96
            y += 45
        else:
            x += 48
