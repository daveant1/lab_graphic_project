from graphics import *
import re
import math

#Function to update properties of mouse shape
def update_mouse(mouse, shape):
    shape.setFill('White')
    if isinstance(mouse.age, int) and (mouse.age > 275):
        shape.setFill('Orange')
    if mouse.pregnant:
        shape.setFill('Pink')
    if not mouse.ET:
        shape.setOutline('Red')
        shape.setWidth(3)
    return shape

#Function to update properties of cage shape based on conds dict
def update_cage(cage, shape, conds):
    # if str(cage.status).lower() == 'breeding':
    #     shape.setFill('DarkGray')
    # elif str(cage.status).lower() == 'pregnant':
    #     shape.setFill('Pink')
    if isinstance(cage.status, str) and not cage.status.isspace():   #cell is blank, default color (X11) is white
        stat = str(cage.status).lower()
        if stat in conds.keys():
            shape.setFill(conds[stat][0])
    else:
        shape.setFill('White')
    return shape



#Function to construct cage text elements
def gen_cage_text(cage, shape, factor):
    tl=[]   #list of text objects
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
        t = Text(Point(x, y+55), dob_msg)
        t.setSize(math.ceil(10*factor))
        tl.append(t)
        wd_msg = 'Wean Date: ' + str(dates[1])
        t = Text(Point(x, y+70), wd_msg)
        t.setSize(math.ceil(10*factor))
        tl.append(t)
    return tl

#Function to construct mouse text elements
def gen_mouse_text(mouse, shape, factor):
    tl=[]   #list of text objects to be drawn in main loop
    origin = shape.getCenter()    #Retrieve current coordinates
    x = origin.getX()
    y = origin.getY()

    #Draw Age
    if not str(mouse.age).isspace():
        t = Text(origin, mouse.age)
        t.setSize(math.ceil(12*factor))
        if mouse.runt:
            t.setSize(math.ceil(8*factor))
        tl.append(t)

    #Draw Mouse ID
    pos = Point(x, y+23)
    t = Text(pos, mouse.ID)
    t.setSize(math.floor(11*factor))
    if mouse.genotyped:
        t.setTextColor('Yellow')
    tl.append(t)
    return tl

#Draw all mice shapes and apply relevant properties
#initalize coordinates (x and y always represent center of shape)
#inital coordinate: (o_x, o_y) is the top left corner of current cage cell
def print_mice(win, mice_dict, mouse_list, o_x, o_y, factor):
    x = o_x + 24
    y = o_y + 50
    m_count = 0    #Count of printed mice
    for idx in mouse_list:
        curr = mice_dict[idx]
        if curr.runt:
            rad = 10
        else:
            rad = 16
        if curr.sex:
            sh = Rectangle(Point(x-rad, y-rad), Point(x+rad, y+rad))
        else:
            sh = Circle(Point(x, y), rad)
        sh = update_mouse(curr, sh)
        sh.draw(win)

        mouse_text = gen_mouse_text(curr, sh, factor)   #generate text elements for mouse as list
        for t in mouse_text:
            t.draw(win)

        #print sacked symbol (cross)
        if curr.sacked in ('p', 's'):
            ln = Line(Point(x-rad, y+rad), Point(x+rad, y-rad))
            ln.draw(win)
            if curr.sacked == 's':
                ln2 = Line(Point(x-rad, y-rad), Point(x+rad, y+rad))
                ln2.draw(win)

        m_count+=1
        if(m_count==3):
            x -= 96
            y += 48
        else:
            x += 48
