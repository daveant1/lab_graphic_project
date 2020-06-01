from graphics import *

#Function to update properties of mouse shape
#Input: mouse object, respective shape
#Output: updated shape
def update_prop(mouse, shape):
    origin = shape.getCenter()
    shape.setFill('LimeGreen')
    if mouse.pregnant:
        shape.setFill('Pink')
    if not mouse.ET:
        shape.setOutline('Red')
        shape.setWidth(2)
    if mouse.age >= 300:
        shape.setFill('Orange')
    return shape

#Function to update mouse text elements
def gen_mouse_text(mouse, shape):
    tl=[]   #list of text objects to be drawn in main loop
    origin = shape.getCenter()    #Retrieve current coordinates
    x = origin.getX()
    y = origin.getY()

    #Draw Age
    t = Text(origin, mouse.age)
    t.setSize(12)
    tl.append(t)
    #Draw Mouse ID
    pos = Point(x, y+23)
    t = Text(pos, mouse.ID)
    t.setSize(9)

    if(mouse.genotyped):
        t.setTextColor('Yellow')

    tl.append(t)
    return tl


#Draw all mice shapes and apply relevant properties (called by main())
#initalize coordinates (x and y always represent center of shape)
#inital coordinate: (o_x, o_y) is the top left corner of current cage cell
def print_mice(win, mice_dict, mouse_list, o_x, o_y):
    x = o_x + 24
    y = o_y + 50
    m_count = 0    #Count of printed mice to check for next row
    for ID in mouse_list:
        curr = mice_dict[ID]     #fetch curr mouse from dict
        if curr.sex:        #init square
            sh = Rectangle(Point(x-16, y-16), Point(x+16, y+16))
        else:               #init circle
            sh = Circle(Point(x, y), 16)
        sh = update_prop(curr, sh)
        sh.draw(win)

        textlist = gen_mouse_text(curr, sh)   #generate text elements for mouse as list
        for t in textlist:
            t.draw(win)

        m_count+=1
        if(m_count==3):
            x -= 72
            y += 44
        else:
            x += 48
