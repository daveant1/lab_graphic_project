from graphics import *
import re
import math

#Function to update properties of mouse shape
#Input: mouse object, respective shape
#Output: updated shape
def update_mouse(mouse, shape):
    origin = shape.getCenter()
    shape.setFill('White')
    # if mouse.pregnant:
    #     shape.setFill('Pink')
    if isinstance(mouse.age, int) and (mouse.age > 275):
        shape.setFill('Orange')
    # if mouse.sacked:
    #     shape.setFill('Black')
    if not mouse.ET:
        shape.setOutline('Red')
        shape.setWidth(3)
    return shape

#Function to update properties of cage shape
#Input: cage object, respective shape
#Output: updated shape
def update_cage(cage, shape):
    if cage.status == 'BREEDING':
        shape.setFill('DarkGray')
    elif cage.status == 'PREGNANT':
        shape.setFill('Pink')
    elif type(cage.status) == float:   #cell is blank, default color is white
        shape.setFill('White')
    else:
        shape.setFill(cage.status)
    return shape




def gen_cage_text(cage, shape, factor):
    tl=[]   #list of text objects to be drawn in main loop
    origin = shape.getCenter()    #Retrieve current coordinates
    x = origin.getX()
    y = origin.getY()

    #Draw Cage ID
    if len(cage.CID) > 5:
        pos=Point(x, y-65)
    elif len(cage.CID) > 3:
        pos = Point(x-43, y-65)
    else:
        pos = Point(x-50, y-65)
    t = Text(pos, cage.CID)
    t.setSize(math.ceil(18*factor))
    t.setStyle('bold')
    tl.append(t)

    #Draw Pup DOB
    if cage.pups > 0:
        pos = Point(x, y+65)
        #Reformat pup DOB and create pup text
        match = re.search(r'(\d*)\-(\d\d)\-(\d\d)', str(cage.DOB))
        new_DOB = match.group(2) + '/' + match.group(3) + '/' + match.group(1)
        pup_msg = str(int(cage.pups)) + ' pups DOB: ' + str(new_DOB)
        t = Text(pos, pup_msg)
        t.setSize(math.ceil(10*factor))
        tl.append(t)
    return tl

#Function to update mouse text elements
def gen_mouse_text(mouse, shape, factor):
    tl=[]   #list of text objects to be drawn in main loop
    origin = shape.getCenter()    #Retrieve current coordinates
    x = origin.getX()
    y = origin.getY()

    #Draw Age
    if mouse.age != '':
        t = Text(origin, mouse.age)
        t.setSize(math.ceil(12*factor))
        if mouse.runt:
            t.setSize(math.ceil(8*factor))
            # if mouse.genotyped:
            #     t.setTextColor('Yellow')
        tl.append(t)

    #Draw Mouse ID
    pos = Point(x, y+23)
    t = Text(pos, mouse.ID)
    t.setSize(math.floor(11*factor))
    if mouse.genotyped:
        t.setTextColor('Yellow')
    tl.append(t)
    return tl



#Draw all mice shapes and apply relevant properties (called by main())
#initalize coordinates (x and y always represent center of shape)
#inital coordinate: (o_x, o_y) is the top left corner of current cage cell
def print_mice(win, mice_dict, mouse_list, o_x, o_y, factor):
    x = o_x + 24
    y = o_y + 50
    m_count = 0    #Count of printed mice to check for next row
    for idx in mouse_list:
        curr = mice_dict[idx]     #fetch curr mouse from dict
        if curr.runt:
            rad = 10
        else:
            rad = 16
        if curr.sex:        #init square
            sh = Rectangle(Point(x-rad, y-rad), Point(x+rad, y+rad))
        else:               #init circle
            sh = Circle(Point(x, y), rad)
        sh = update_mouse(curr, sh)
        sh.draw(win)

        mouse_text = gen_mouse_text(curr, sh, factor)   #generate text elements for mouse as list
        for t in mouse_text:
            t.draw(win)

        if curr.sacked in ('P', 'S'):
            ln = Line(Point(x-rad, y+rad), Point(x+rad, y-rad))
            ln.draw(win)
            if curr.sacked == 'S':
                ln2 = Line(Point(x-rad, y-rad), Point(x+rad, y+rad))
                ln2.draw(win)

        m_count+=1
        if(m_count==3):
            x -= 96
            y += 48
        else:
            x += 48
