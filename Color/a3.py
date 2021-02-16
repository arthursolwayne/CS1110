""" 
Functions for Assignment A3

This file contains the functions for the assignment. You should replace the stubs
with your own implementations.

Arthur Wayne asw263
16 October 2020
"""
import introcs
import math


def complement_rgb(rgb):
    """
    Returns the complement of color rgb.
    
    Parameter rgb: the color to complement
    Precondition: rgb is an RGB object
    """

    return introcs.RGB(255 - rgb.red, 255 - rgb.green, 255 - rgb.blue)


def str5(value):
    """
    Returns value as a string, but expanded or rounded to be exactly 5 characters.
    
    The decimal point counts as one of the five characters.
   
    Examples:
        str5(1.3546)  is  '1.355'.
        str5(21.9954) is  '22.00'.
        str5(21.994)  is  '21.99'.
        str5(130.59)  is  '130.6'.
        str5(130.54)  is  '130.5'.
        str5(1)       is  '1.000'.
    
    Parameter value: the number to conver to a 5 character string.
    Precondition: value is a number (int or float), 0 <= value <= 360.
    """
    # Remember that the rounding takes place at a different place depending 
    # on how big value is. Look at the examples in the specification.
    if value < 10:
        return str(format(value, '.3f'))
    elif value >= 10 and value < 100:
        if value == 99.995:
            return str(format(value, '.1f'))
        return str(format(value, '.2f'))
    else:
        return str(format(value, '.1f'))


def str5_cmyk(cmyk):
    """
    Returns the string representation of cmyk in the form "(C, M, Y, K)".
    
    In the output, each of C, M, Y, and K should be exactly 5 characters long.
    Hence the output of this function is not the same as str(cmyk)
    
    Example: if str(cmyk) is 
    
          '(0.0,31.3725490196,31.3725490196,0.0)'
    
    then str5_cmyk(cmyk) is '(0.000, 31.37, 31.37, 0.000)'. Note the spaces after the
    commas. These must be there.
    
    Parameter cmyk: the color to convert to a string
    Precondition: cmyk is an CMYK object.
    """
    return "("+str5(cmyk.cyan)+", "+str5(cmyk.magenta)+", "+str5(cmyk.yellow)+", "+str5(cmyk.black)+")"


def str5_hsv(hsv):
    """
    Returns the string representation of hsv in the form "(H, S, V)".
    
    In the output, each of H, S, and V should be exactly 5 characters long.
    Hence the output of this function is not the same as str(hsv)
    
    Example: if str(hsv) is 
    
          '(0.0,0.313725490196,1.0)'
    
    then str5_hsv(hsv) is '(0.000, 0.314, 1.000)'. Note the spaces after the
    commas. These must be there.
    
    Parameter hsv: the color to convert to a string
    Precondition: hsv is an HSV object.
    """
    s = "("+str5(hsv.hue)+", "+str5(hsv.saturation)+", "+str5(hsv.value)+")"
    return s


def rgb_to_cmyk(rgb):
    
    """
    Returns a CMYK object equivalent to rgb, with the most black possible.
    
    Formulae from https://www.rapidtables.com/convert/color/rgb-to-cmyk.html
    
    Parameter rgb: the color to convert to a CMYK object
    Precondition: rgb is an RGB object
    """
    # The RGB numbers are in the range 0..255.
    # Change them to the range 0..1 by dividing them by 255.0.
    r = rgb.red / 255.0
    g = rgb.green / 255.0
    b = rgb.blue / 255.0

    k = 1 - max(r,g,b)

    if k == 1:
        c = 0
        m = 0
        y = 0
    else:
        c = (1-r-k)/(1-k)
        m = (1-g-k)/(1-k)
        y = (1-b-k)/(1-k)

    c *= 100.0
    m *= 100.0
    y *= 100.0
    k *= 100.
0
    return introcs.CMYK(c,m,y,k)


def cmyk_to_rgb(cmyk):
    """
    Returns an RGB object equivalent to cmyk
    
    Formulae from https://www.rapidtables.com/convert/color/cmyk-to-rgb.html
   
    Parameter cmyk: the color to convert to a RGB object
    Precondition: cmyk is an CMYK object.
    """
    # The CMYK numbers are in the range 0.0..100.0. 
    # Deal with them the same way as the RGB numbers in rgb_to_cmyk()
    c = cmyk.cyan / 100.0
    m = cmyk.magenta / 100.0
    y = cmyk.yellow / 100.0
    k = cmyk.black / 100.0

    r = (1-c)*(1-k)
    g = (1-m)*(1-k)
    b = (1-y)*(1-k)

    r = round(r*255.0)
    g = round(g*255.0)
    b = round(b*255.0)

    return introcs.RGB(r,g,b)


def rgb_to_hsv(rgb):
    """
    Return an HSV object equivalent to rgb
    
    Formulae from https://en.wikipedia.org/wiki/HSL_and_HSV
   
    Parameter hsv: the color to convert to a HSV object
    Precondition: rgb is an RGB object
    """
    # The RGB numbers are in the range 0..255.
    # Change them to range 0..1 by dividing them by 255.0.
    r = rgb.red / 255.0
    g = rgb.green / 255.0
    b = rgb.blue / 255.0

    maxy = max(r,g,b)
    miny = min(r,g,b)

    if maxy == miny:
        h = 0
    elif maxy == r and g >= b:
        h = 60.0*(g-b)/(maxy-miny)
    elif maxy == r and g < b:
        h = 60.0*(g-b)/(maxy-miny) + 360.0
    elif maxy == g:
        h = 60.0*(b-r)/(maxy-miny) + 120.0
    elif maxy == b:
        h = 60.0*(r-g)/(maxy-miny) + 240.0

    if maxy == 0:
        s = 0
    else: 
        s = 1 - (miny/maxy)

    v = maxy

    return introcs.HSV(h,s,v)


def hsv_to_rgb(hsv):
    """
    Returns an RGB object equivalent to hsv
    
    Formulae from https://en.wikipedia.org/wiki/HSL_and_HSV
    
    Parameter hsv: the color to convert to a RGB object
    Precondition: hsv is an HSV object.
    """
    
    hi = math.floor(hsv.hue/60)
    f = hsv.hue/60 - hi
    p = hsv.value*(1-hsv.saturation)
    q = hsv.value*(1-(f*hsv.saturation))
    t = hsv.value*(1-(1-f)*hsv.saturation)

    if hi == 0 or hi == 5:
        r = hsv.value
    elif hi == 1:
        r = q
    elif hi == 2 or hi == 3:
        r = p
    elif hi == 4:
        r = t

    if hi == 0:
        g = t
    elif hi == 1 or hi == 2:
        g = hsv.value
    elif hi == 3:
        g = q
    elif hi == 4 or hi == 5:
        g = p

    if hi == 0 or hi == 1:
        b = p
    elif hi == 2:
        b = t
    elif hi == 3 or hi == 4:
        b = hsv.value
    elif hi == 5:
        b = q

    return introcs.RGB(round(r*255),round(g*255),round(b*255))


def contrast_value(value,contrast):
    """
    Returns value adjusted to the "sawtooth curve" for the given contrast
    
    At contrast = 0, the curve is the normal line y = x, so value is unaffected.
    If contrast < 0, values are pulled closer together, with all values collapsing
    to 0.5 when contrast = -1.  If contrast > 0, values are pulled farther apart, 
    with all values becoming 0 or 1 when contrast = 1.
    
    Parameter value: the value to adjust
    Precondition: value is a float in 0..1
    
    Parameter contrast: the contrast amount (0 is no contrast)
    Precondition: contrast is a float in -1..1
    """
    x = value
    c = contrast
    if c >= -1 and c < 1:
        if x < (0.25 + (0.25*c)):
            y = ((1-c)/(1+c))*x
        elif x > (0.75 - (0.25*c)):
            y = ((1-c)/(1+c))*(x-((3-c)/4))+((3+c)/4)
        else:
            y = ((1+c)/(1-c))*(x-((1+c)/4))+((1+c)/4)
    elif c == 1:
        if x >= 0.5:
            y = 1
        else:
            y = 0

    return y



def contrast_rgb(rgb,contrast):
    """
    Applies the given contrast to the RGB object rgb
    
    This function is a PROCEDURE.  It modifies rgb and has no return value.  It should
    apply contrast_value to the red, blue, and green values.
    
    Parameter rgb: the color to adjust
    Precondition: rgb is an RGB object
    
    Parameter contrast: the contrast amount (0 is no contrast)
    Precondition: contrast is a float in -1..1
    """
    rgb.red = round(255.0*contrast_value(rgb.red/255.0, contrast))
    rgb.blue = round(255.0*contrast_value(rgb.blue/255.0, contrast))
    rgb.green = round(255.0*contrast_value(rgb.green/255.0, contrast))