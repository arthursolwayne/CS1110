"""
A module to draw cool shapes with the introcs Turtle.

You call all of these functions in the interactive shell, but you will have 
to create a Window first.  Alternatively, you can use the a4test.py test script
to try out the functions.

Arthur Wayne asw263
November 2, 2020
"""
from introcs.turtle import Window, Turtle, Pen
import introcs  # For the RGB and HSV objects
import math     # For the math computations


################# Helpers for Precondition Verification #################

def is_number(x):
    """
    Returns: True if value x is a number; False otherwise.
    
    Parameter x: the value to check
    Precondition: NONE (x can be any value)
    """
    return type(x) in [float, int]


def is_window(w):
    """
    Returns: True if w is a introcs Window; False otherwise.
    
    Parameter w: the value to check
    Precondition: NONE (w can be any value)
    """
    return type(w) == Window


def is_valid_color(c):
    """
    Returns: True c is a valid turtle color; False otherwise
    
    Parameter c: the value to check
    Precondition: NONE (c can be any value)
    """
    return (type(c) == introcs.RGB or type(c) == introcs.HSV or
            (type(c) == str and (introcs.is_tkcolor(c) or introcs.is_webcolor(c))))


def is_valid_speed(sp):
    """
    Returns: True if sp is an int in range 0..10; False otherwise.
    
    Parameter sp: the value to check
    Precondition: NONE (sp can be any value)
    """
    return (type(sp) == int and 0 <= sp and sp <= 10)


def is_valid_length(side):
    """
    Returns: True if side is a number >= 0; False otherwise.
    
    Parameter side: the value to check
    Precondition: NONE (side can be any value)
    """
    return (is_number(side) and 0 <= side)


def is_valid_iteration(n):
    """
    Returns: True if n is an int >= 1; False otherwise.
    
    Parameter n: the value to check
    Precondition: NONE (n can be any value)
    """
    return (type(n) == int and 1 <= n)


def is_valid_polygon(n):
    """
    Returns: True if n is an int >= 3; False otherwise.
    
    Parameter n: the value to check
    Precondition: NONE (n can be any value)
    """
    return (type(n) == int and 3 <= n)


def is_valid_depth(d):
    """
    Returns: True if d is an int >= 0; False otherwise.
    
    Parameter d: the value to check
    Precondition: NONE (d can be any value)
    """
    return (type(d) == int and d >= 0)


def is_valid_turtlemode(t):
    """
    Returns: True t is a Turtle with drawmode True; False otherwise.
    
    Parameter t: the value to check
    Precondition: NONE (t can be any value)
    """
    return (type(t) == Turtle and t.drawmode)


def is_valid_penmode(p):
    """
    Returns: True t is a Pen with solid False; False otherwise.
    
    Parameter p: the value to check
    Precondition: NONE (p can be any value)
    """
    return (type(p) == Pen and not p.solid)


def report_error(message, value):
    """
    Returns: An error message about the given value.
    
    This is a function for constructing error messages to be used in assert 
    statements. We find that students often introduce bugs into their assert 
    statement messages, and do not find them because they are in the habit of 
    not writing tests that violate preconditions.
    
    The purpose of this function is to give you an easy way of making error 
    messages without having to worry about introducing such bugs. Look at 
    the function draw_two_lines for the proper way to use it.
    
    Parameter message: The error message to display
    Precondition: message is a string
    
    Parameter value: The value that caused the error
    Precondition: NONE (value can be anything)
    """
    return message+': '+repr(value)


#################### DEMO: Two lines ####################

def draw_two_lines(w,sp):
    """
    Draws two lines on to window w.
    
    This function clears w of any previous drawings. Then, in the middle of 
    the window w, this function draws a green line 100 pixels to the east, 
    and then a blue line 200 pixels to the north. It uses a new turtle that 
    moves at speed sp, 0 <= sp <= 10, with 1 being slowest and 10 fastest 
    (and 0 being "instant").
    
    REMEMBER: You need to flush the turtle if the speed is 0.
    
    This procedure asserts all preconditions.
    
    Parameter w: The window to draw upon.
    Precondition: w is a introcs Window object.
    
    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # Assert the preconditions
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)
    
    # Clear the window first!
    w.clear()
    
    # Create a turtle and draw
    t = Turtle(w)
    t.speed = sp
    t.color = 'green'
    t.forward(100) # draw a line 100 pixels in the current direction
    t.left(90)     # add 90 degrees to the angle
    t.color = 'blue'
    t.forward(200)
    
    # This is necessary if speed is 0!
    t.flush()


#################### TASK 1: Triangle ####################

def draw_triangle(t, s, c):
    """
    Draws an equilateral triangle of side s and color c at current position.
    
    The direction of the triangle depends on the current facing of the turtle.
    If the turtle is facing west, the triangle points up and the turtle starts
    and ends at the east end of the base line.
    
    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    position (x and y, within round-off errors), heading, color, and drawmode.
    If you changed any of these in the function, you must change them back.
    
    REMEMBER: You need to flush the turtle if the speed is 0.
    
    This procedure asserts all preconditions.
    
    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.
    
    Parameter s: The length of each triangle side
    Precondition: s is a valid side length (number >= 0)
    
    Parameter c: The triangle color
    Precondition: c is a valid turtle color (see the helper function above)
    """
    # Assert the preconditions
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(s), report_error('Invalid side length', s)
    assert is_valid_color(c), report_error('Invalid color', c)
    
    # Hint: each angle in an equilateral triangle is 60 degrees.
    # Note: In this function, DO NOT save the turtle position and heading
    # in the beginning and then restore them at the end. The turtle moves
    # should be such that the turtle ends up where it started and facing
    # in the same direction, automatically.
    
    # Also, 3 lines have to be drawn. Does this suggest a for loop that
    # processes the range 0..2?
    orig_color = t.color
    t.color = c
    for i in range(3):
        t.forward(s)
        t.right(120)
    t.color = orig_color
    t.flush()


#################### TASK 2: Hexagon ####################

def draw_hex(t, s):
    """
    Draws six triangles using the color 'cyan' to make a hexagon.
    
    The triangles are equilateral triangles, using draw_triangle as a helper.
    The drawing starts at the turtle's current position and heading. The
    middle of the hexagon is the turtle's starting position.
    
    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    position (x and y, within round-off errors), heading, color, and drawmode.
    If you changed any of these in the function, you must change them back.
    
    REMEMBER: You need to flush the turtle if the speed is 0.
    
    This procedure asserts all preconditions.
    
    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.
    
    Parameter s: The length of each triangle side
    Precondition: s is a valid side length (number >= 0)
    """
    # Assert the preconditions
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(s), report_error('Invalid side length', s)

    # Note: Do not save any of the turtle's properties and then restore them
    # at the end. Just use 6 calls on procedures drawTriangle and t.left. Test
    # the procedure to make sure that t's final location and heading are the
    # same as t's initial location and heading (except for roundoff error).
    for i in range(6):
        draw_triangle(t, s, 'cyan')
        t.left(60)
    t.flush()


#################### Task 3A: Spirals ####################

def draw_spiral(w, side, ang, n, sp):
    """
    Draws a spiral using draw_spiral_helper(t, side, ang, n, sp)
    
    This function clears the window and makes a new turtle t.  This turtle
    starts in the middle of the canvas facing south (NOT the default east).
    It then calls draw_spiral_helper(t, side, ang, n, sp). When it is done,
    the turtle is left hidden (visible is False).
    
    REMEMBER: You need to flush the turtle if the speed is 0.
    
    This procedure asserts all preconditions.
    
    Parameter w: The window to draw upon.
    Precondition: w is a introcs Window object.
    
    Parameter side: The length of each spiral side
    Precondition: side is a valid side length (number >= 0)
    
    Parameter ang: The angle of each corner of the spiral
    Precondition: ang is a number
    
    Parameter n: The number of edges of the spiral
    Precondition: n is a valid number of iterations (int >= 1)
    
    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert is_number(ang), report_error('angle is not valid number', ang)
    assert is_valid_iteration(n), report_error('n is not a valid number of iterations',side)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)
    
    # HINT: Set the visible attribute to False at the end, and remember to flush
    w.clear()
    t = Turtle(w)
    t.heading = 270
    draw_spiral_helper(t, side, ang, n, sp)
    t.visible = False
    t.flush()


def draw_spiral_helper(t, side, ang, n, sp):
    """
    Draws a spiral of n lines at the current position and heading.
    
    The spiral begins at the current turtle position and heading, turning ang
    degrees to the left after each line. Line 0 is side pixels long. Line 1
    is 2*side pixels long, and so on.  Hence each Line i is (i+1)*side pixels
    long. The lines alternate between blue, magenta, and red, in that order, 
    with the first one blue.
    
    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    color, speed, visible, and drawmode. However, the final position and
    heading may be different. If you changed any of these four in the 
    function, you must change them back.
    
    This procedure asserts all preconditions.
    
    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.
    
    Parameter side: The length of each spiral side
    Precondition: side is a valid side length (number >= 0)
    
    Parameter ang: The angle of each corner of the spiral
    Precondition: ang is a number
    
    Parameter n: The number of edges of the spiral
    Precondition: n is a valid number of iterations (int >= 1)
    
    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert is_number(ang), report_error('angle is not valid number', ang)
    assert is_valid_iteration(n), report_error('n is not a valid number of iterations',side)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)

    orig_color = t.color
    orig_speed = t.speed
    colorList = ['blue', 'magenta', 'red']
    for i in range(n):
        if i > 2:
            j = i%3
            t.color = colorList[j]
        else:
            t.color = colorList[i]
        t.forward((i+1)*side)
        t.left(ang)
    t.color = orig_color
    t.speed = orig_speed    


#################### TASK 3B: Polygons ####################

def multi_polygons(w, side, k, n, sp):
    """
    Draws polygons using multi_polygons_helper(t, side, k, n, sp)
    
    This function clears the window and makes a new turtle t. This turtle 
    starts in the middle of the canvas facing north (NOT the default east). 
    It then calls multi_polygons_helper(t, side, k, n, sp). When it is done, 
    the turtle is left hidden (visible is False).
    
    REMEMBER: You need to flush the turtle if the speed is 0.
    
    This procedure asserts all preconditions.
    
    Parameter w: The window to draw upon.
    Precondition: w is a introcs Window object.
    
    Parameter side: The length of each polygon side
    Precondition: side is a valid side length (number >= 0)
    
    Parameter k: The number of polygons to draw
    Precondition: k is an int >= 1
    
    Parameter n: The number of sides of each polygon
    Precondition: n is an int >= 3
    
    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert is_valid_iteration(k), report_error('k is not valid number of polygons',k)
    assert is_valid_polygon(n), report_error('n is not valid number of sides', n)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)
    
    w.clear()
    t = Turtle(w)
    t.heading = 90
    multi_polygons_helper(t, side, k, n, sp)
    t.visible = False
    t.flush()


def multi_polygons_helper(t, side, k, n, sp):
    """
    Draws k n-sided polygons of side length s.
    
    The polygons are drawn by turtle t, starting at the current position. The
    turtles alternate colors between blue and orange (starting with blue). 
    Each polygon is drawn starting at the same place (within roundoff errors),
    but t turns left 360.0/k degrees after each polygon.
    
    At the end, ALL ATTRIBUTES of the turtle are the same as they were in the 
    beginning (within roundoff errors). If you change any attributes of the 
    turtle. then you must restore them. Look at the helper draw_polygon for 
    more information.
    
    This procedure asserts all preconditions.
    
    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.
    
    Parameter side: The length of each polygon side
    Precondition: side is a valid side length (number >= 0)
    
    Parameter k: The number of polygons to draw
    Precondition: k is an int >= 1
    
    Parameter n: The number of sides of each polygon
    Precondition: n is an int >= 3
    
    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
 
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert is_valid_iteration(k), report_error('k is not valid number of polygons',k)
    assert is_valid_polygon(n), report_error('n is not valid number of sides', n)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)
    
    # HINT: Make sure you restore t's color and speed when done
    # HINT: Since k polygons should be drawn, use a for-loop on a range of numbers.
    colorList = ['blue','orange']
    orig_color = t.color
    orig_speed = t.speed
    for i in range(k):
        if i > 1:
            j = i%2
            t.color = colorList[j]
        else:
            t.color = colorList[i]
        draw_polygon(t, side, n)
        t.left(360.0/k)
    t.color = orig_color
    t.speed = orig_speed


# DO NOT MODIFY
def draw_polygon(t, side, n):
    """
    Draws an n-sided polygon using of side length side.
    
    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    position (x and y, within round-off errors), heading, color, speed, 
    visible, and drawmode. There is no need to restore these.
    
    This procedure asserts all preconditions.
    
    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.
    
    Parameter side: The length of each polygon side
    Precondition: side is a valid side length (number >= 0)
    
    Parameter n: The number of sides of each polygon
    Precondition: n is an int >= 1
    """
    # Assert the preconditions
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert type(n) == int and n >= 1, report_error('n is an invalid # of poly sides',n)
    
    # Remember old speed
    ang = 360.0/n # exterior angle between adjacent sides
    
    # t is in position and facing the direction to draw the next line.
    for _ in range(n):
        t.forward(side)
        t.left(ang)


#################### TASK 3C: Radiating Petals ####################

def radiate_petals(w, radius, width, n, sp):
    """
    Draws a color flower with n petals using radiate_petals_helper(t, side, width, n, sp)
    
    This function clears the window and makes a new turtle t.  This turtle
    starts in the middle of the canvas facing west (NOT the default east).
    It then calls radiate_petals_helper(t, side, width, n, sp). When it is 
    done, the turtle is left hidden (visible is False).
    
    REMEMBER: You need to flush the turtle if the speed is 0.
    
    This procedure asserts all preconditions.
    
    Parameter w: The window to draw upon.
    Precondition: w is a introcs Window object.
    
    Parameter radius: The radius of the produced "flower"
    Precondition: radius is a valid side length (number >= 0)
    
    Parameter width: The width of an open petal
    Precondition: width is a valid side length (number >= 0)
    
    Parameter n: The number of lines to draw
    Precondition: n is an int >= 2
    
    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_length(radius), report_error('radius is not a valid length',radius)
    assert is_valid_length(width),  report_error('width is not a valid length',width)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)
    
    # HINT: w.clear() clears window.
    # HINT: Set the visible attribute to False at the end, and remember to flush
    pass


def radiate_petals_helper(t, radius, width, n, sp):
    """
    Draws a color flower with n petals of length radius at equal angles.
    
    The petals alternate between open (a diamond of the given width) and
    closed (a straight line), starting with an open petal.. Open petals are 
    drawn with function draw_diamond, while closed petals are drawn by 
    moving the turtle in a straight line. After drawing each petal, the 
    turtle should return to its original position.
    
    The petals are drawn at equal angles starting from the initial turtle
    heading. A petal drawn at angle ang, 0 <= ang < 360 has the HSV color 
    (ang % 360.0, 1, 1).
    
    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    color, speed, visible, and drawmode. However, the final position and
    heading may be different. If you changed any of these four in the 
    function, you must change them back.
    
    This procedure asserts all preconditions.
    
    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.
    
    Parameter radius: The radius of the produced "flower"
    Precondition: radius is a valid side length (number >= 0)
    
    Parameter width: The width of an open petal
    Precondition: width is a valid side length (number >= 0)
    
    Parameter n: The number of lines to draw
    Precondition: n is an int >= 2
    
    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # Assert the preconditions
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(radius), report_error('radius is not a valid length',radius)
    assert is_valid_length(width),  report_error('width is not a valid length',width)
    assert (type(n) == int and n >= 2), report_error('n is an invalid # of petals',n)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)
    
    # Hints:
    # 1. Drawing the petals should be drawn with a range loop.
    # 2. The first petal should be open, alternating with closed petals afterwards
    # 3. Open petals should be drawn with the function draw_diamond
    # 4. The heading of the turtle should stay in the range 0 <= heading < 360.
    # 5. (t.heading % 360.0, 1, 1) is the HSV color of the turtle for each petal
    # 6. You can use an HSV object for the turtle's color attribute,
    #    even though all the examples use strings with color names
    pass


# DO NOT MODIFY
def draw_diamond(t, length, width):
    """
    Draws an diamond whose major axis (length) is along the current heading.
    
    The width is the size of the minor axis, which is perpendicular to the 
    current turtle heading.
    
    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED: 
    position (x and y, within round-off errors), heading, color, speed, visible, 
    and drawmode. There is no need to restore these.
    
    This procedure asserts all preconditions.
    
    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.
    
    Parameter length: The size of the major axis
    Precondition: length is a valid side length (number >= 0)
    
    Parameter width: The size of the minor (perpendicular) axis
    Precondition: width is a valid side length (number >= 0)
    """
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(length), report_error('length is not a valid length',length)
    assert is_valid_length(width),  report_error('width is not a valid length',width)
    
    # Compute the next position to go to
    angle1 = t.heading*math.pi/180.0
    x2 = t.x+math.cos(angle1)*length/2
    y2 = t.y+math.sin(angle1)*length/2
    x2 -= math.sin(angle1)*width/2
    y2 += math.cos(angle1)*width/2
    
    # Compute the offset heading and edge length
    angle2 = math.atan2(y2-t.y,x2-t.x)*180.0/math.pi
    angle3 = angle2-t.heading
    edgesz = math.sqrt((x2-t.x)*(x2-t.x)+(y2-t.y)*(y2-t.y))
    
    # Draw the diamond, restoring position and heading
    t.right(angle3)
    t.forward(edgesz)
    t.left(2*angle3)
    t.forward(edgesz)
    t.right(2*angle3)
    t.backward(edgesz)
    t.left(2*angle3)
    t.backward(edgesz)
    t.right(angle3)


#################### TASK 4A: Sierpinski Triangle ####################

def triangle(w, side, d, sp):
    """
    Draws a Sierpinski triangle with the given side length and depth d.
    
    This function clears the window and makes a new graphics pen p.  This
    pen starts in the middle of the canvas at (0,0). It draws by calling
    the function triangle_helper(p, 0, 0, side, d). The pen is visible
    during drawing and should be set to hidden at the end.
   
    The pen should have  a 'magenta' fill color and a 'black' edge color.
    
    REMEMBER: You need to flush the pen if the speed is 0.
    
    Parameter w: The window to draw upon.
    Precondition: w is a Window object.
    
    Parameter side: The side length of the triangle
    Precondition: side is a valid side length (number >= 0)
    
    Parameter d: The recursive depth of the triangle
    Precondition: d is a valid depth (int >= 0)
    
    Parameter sp: The drawing speed.
    Precondition: sp is a valid turtle/pen speed.
    """
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert is_valid_depth(d), report_error('d is not a valid depth',d)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)
    # HINT: Set the visible attribute to False at the end, and remember to flush
    w.clear()
    p = Pen(w)
    p.fillcolor = 'magenta'
    p.edgecolor = 'black'
    triangle_helper(p, 0, 0, side, d)
    p.visible = False


def triangle_helper(p, x, y, side, d):
    """
    Draws a Sierpinski triangle with the given side length and depth d, centered at (x, y).
    
    The triangle is draw with the current pen color and visibility attribute. Follow 
    the instructions on the course website to recursively draw the Sierpinski triangle. 
    The center of the triangle is positioned at (x,y).
    
    Parameter p: The graphics pen
    Precondition: p is a Pen with fill attribute False.
    
    Parameter x: The x-coordinate of the triangle center
    Precondition: x is a number
    
    Parameter y: The y-coordinate of the triangle center
    Precondition: y is a number
    
    Parameter side: The side-length of the triangle
    Precondition: side is a valid side length (number >= 0)
    
    Parameter d: The recursive depth of the triangle
    Precondition: d is a valid depth (int >= 0)
    """
    assert is_valid_penmode(p), report_error('Invalid pen mode', p)
    assert is_number(x), report_error('x is not valid number', x)
    assert is_number(y), report_error('y is not valid number', y)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert is_valid_depth(d), report_error('d is not a valid depth',d)
    # Hint: Use fill_triangle to draw an individual triangle
    height = side*(math.sqrt(3)/2)
    if d == 0:
        fill_triangle(p, x, y, side)
    else:
        # three calls to triangle helper with variable x and y's
        triangle_helper(p,x-(side/4),y-(height/4),side/2,d-1)
        triangle_helper(p,x+(side/4),y-(height/4),side/2,d-1)
        triangle_helper(p,x,y+(height/4),side/2,d-1)


# DO NOT MODIFY
def fill_triangle(p, x, y, side):
    """
    Fills an equilateral triangle of side length 
    
    The triangle is pointing up.
    
    Parameter p: The graphics pen
    Precondition: p is a Pen with fill attribute False.
    
    Parameter x: The x-coordinate of the triangle center
    Precondition: x is a number
    
    Parameter y: The y-coordinate of the triangle center
    Precondition: y is a number
    
    Parameter side: The side length of the triangle
    Precondition: side is a valid side length (number >= 0)
    """
    # Precondition Assertions
    assert is_valid_penmode(p), report_error('Invalid pen mode', p)
    assert is_number(x), report_error('x is not a valid position',x)
    assert is_number(y), report_error('x is not a valid position',y)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    
    h = side * math.sqrt(.75)
    p.move(x-side/2, y-h/2)
    p.solid = True
    p.drawLine(side, 0)
    p.drawLine(-side/2.0, h)
    p.drawLine(-side/2.0, -h)
    p.solid = False


#################### TASK 4B: Cantor Stool ####################

def cantor(w, side, hght, d, sp):
    """
    Draws a Cantor Stool of dimensions side x hght, and depth d.
    
    This function clears the window and makes a new graphics pen p.  This
    pen starts in the middle of the canvas at (0,0). It draws by calling
    the function cantor_helper(p, 0, 0, side, hght, d). The pen is visible
    during drawing and should be set to hidden at the end.
    
    The pen should have both fill color and edge color 'red'.
    
    REMEMBER: You need to flush the pen if the speed is 0.
    
    Parameter w: The window to draw upon.
    Precondition: w is a Window object.
    
    Parameter side: The width of the Cantor stool
    Precondition: side is a valid side length (number >= 0)
    
    Parameter hght: The height of the Cantor stool
    Precondition: hght is a valid side length (number >= 0)
    
    Parameter d: The recursive depth of the stool
    Precondition: d is a valid depth (int >= 0)
    
    Parameter sp: The drawing speed.
    Precondition: sp is a valid turtle/pen speed.
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_window(w), report_error('w is not a valid window',w)
    
    # HINT: w.clear() clears window.
    # HINT: Set the visible attribute to False at the end, and remember to flush
    pass


def cantor_helper(p, x, y, side, hght, d):
    """
    Draws a stool of dimensions side x hght, and depth d centered at (x,y)
    
    The stool is draw with the current pen color and visibility attribute.
    Follow the instructions on the course website to recursively draw the
    Cantor stool.
    
    Parameter p: The graphics pen
    Precondition: p is a Pen with fill attribute False.
    
    Parameter x: The x-coordinate of the stool center
    Precondition: x is a number
    
    Parameter y: The y-coordinate of the stool center
    Precondition: y is a number
    
    Parameter side: The width of the Cantor stool
    Precondition: side is a valid side length (number >= 0)
    
    Parameter hght: The height of the Cantor stool
    Precondition: hght is a valid side length (number >= 0)
    
    Parameter d: The recursive depth of the stool
    Precondition: d is a valid depth (int >= 0)
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_valid_penmode(p), report_error('Invalid pen mode', p)
    
    # Hint: Use fill_rect to draw an individual rectangle
    pass


# DO NOT MODIFY
def fill_rect(p, x, y, side, hght):
    """
    Fills a rectangle of lengths side, hght with center (x, y) using pen p.
    
    This procedure asserts all preconditions.
    
    Parameter p: The graphics pen
    Precondition: p is a Pen with solid attribute False.
    
    Parameter x: The x-coordinate of the rectangle center
    Precondition: x is a number
    
    Parameter y: The y-coordinate of the rectangle center
    Precondition: y is a number
    
    Parameter side: The width of the rectangle
    Precondition: side is a valid side length (number >= 0)
    
    Parameter hght: The height of the rectangle
    Precondition: hght is a valid side length (number >= 0)
    """
    # Precondition assertions omitted
    assert is_valid_penmode(p), report_error('Invalid pen mode', p)
    assert is_number(x), report_error('x is not a valid position',x)
    assert is_number(y), report_error('x is not a valid position',y)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert is_valid_length(hght), report_error('hght is not a valid length',hght)
    
    # Move to the center and draw
    p.move(x - side/2.0, y - hght/2.0)
    p.solid = True
    p.drawLine(    0,  hght)
    p.drawLine( side,     0)
    p.drawLine(    0, -hght)
    p.drawLine(-side,     0)
    p.solid = False
    p.move(x - side/2.0, y - hght/2.0)


#################### TASK 5: Minkowski Island ####################

def island(w, side, d, sp):
    """
    Draws a Minkowski island with the given side length and depth d.
    
    This function clears the window and makes a new Turtle t.  This turtle starts in 
    lower right corner of the square centered at (0,0) with side length side. It is 
    facing straight up. It draws by calling the function island_edge(t, side, d) four 
    times, rotating the turtle left after each call to form a square.
    
    The turtle should be visible while drawing, but hidden at the end. The turtle color 
    is 'sea green'.
    
    REMEMBER: You need to flush the turtle if the speed is 0.
    
    Parameter w: The window to draw upon.
    Precondition: w is a Window object.
    
    Parameter side: The side-length of the island
    Precondition: side is a valid side length (number >= 0)
    
    Parameter d: The recursive depth of the island
    Precondition: d is a valid depth (int >= 0)
    
    Parameter sp: The drawing speed.
    Precondition: sp is a valid turtle/pen speed.
    """
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert is_valid_depth(d), report_error('d is not a valid depth',d)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)   

    w.clear()
    t = Turtle(w)
    t.heading = 90
    t.move(side/2,-(side/2))
    t.color = 'sea green'
    for i in range(4):
        island_edge(t,side,d)
        t.left(90)
    t.visible = False
    t.flush()


def island_edge(t, side, d):
    """
    Draws a single Minkowski edge with and depth d at the current position and angle.
    
    The edge is draw with the current turtle color.  You should make no assumptions of
    the current angle of the turtle (e.g. use left and right to turn; do not set the
    heading).
    
    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    color, speed, visible, and drawmode. However, the final position and
    heading may be different. If you changed any of these four in the function,
    you must change them back.
    
    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.
    
    Parameter side: The length of each Minkowski side
    Precondition: side is a valid side length (number >= 0)
    
    Parameter d: The recursive depth of the edge
    Precondition: d is a valid depth (int >= 0)
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert is_valid_depth(d), report_error('d is not a valid depth',d)
    
    # HINT: Look closely at the picture from the instructions.  
    # For depth other than 0, divide the side four equal parts (but eight edges)
    if d == 0:
        t.forward(side)
    else:
        island_edge(t,side/4,d-1)
        t.right(90)
        island_edge(t,side/4,d-1)
        t.left(90)
        island_edge(t,side/4,d-1)
        t.left(90)
        island_edge(t,side/4,d-1)
        island_edge(t,side/4,d-1)
        t.right(90)
        island_edge(t,side/4,d-1)
        t.right(90)
        island_edge(t,side/4,d-1)
        t.left(90)
        island_edge(t,side/4,d-1)

