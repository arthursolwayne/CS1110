"""
Application for displaying color models

You are welcome to read the code in this file. I guarantee that you will not understand
it. The TAs do not understand it. That does not matter. When you code with another
person, you do not need to understand the code they write. You just have to write your
code to specification.

This is an example of a fairly sophisticated Kivy application. Kivy applications are
broken into a code file (this) and a layout file (colormodel.kv). The layout file serves
much the same role as CSS in web pages. In order for it to work it must be in the same 
folder as colormodel.kv. Do not move or change the name of that file.

Author: Walker M. White (wmw2)
Date:   September 25, 2019
"""
import kivy
from kivy.app           import App
from kivy.lang          import Builder
from kivy.uix.widget    import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties    import *
from kivy.vector        import Vector
from kivy.uix.label     import Label
from kivy.factory       import Factory
from kivy.graphics      import Color
from kivy.graphics      import Ellipse
from kivy.config        import Config

from kivy.metrics import dp
from kivy.graphics import Mesh, InstructionGroup

import introcs
import math
import a3


#mark String Functions
def str_rgb(rgb):
    """
    Returns the string representation of an RGB object without alpha
    
    Parameter rgb: the color object to display
    Precondition: rgb is an RGB object
    """
    return '('+str(rgb.red)+', '+str(rgb.green)+', '+str(rgb.blue)+')'


def str_cmyk(cmyk):
    """
    Returns the string representation of a CMYK object.

    Proxy function for a3.str5_cmyk. It returns the empty string if it is not
    defined.
    
    Parameter cmyk: the color object to display
    Precondition: cmyk is an CMYK object
    """
    result = a3.str5_cmyk(cmyk)
    if result is None:
        return ''
    return result 


def str_hsv(hsv):
    """
    Returns the string representation of a HSV object.

    Proxy function for a3.str5_hsv. It returns the empty string if it is not
    defined.
    
    Parameter hsv: the color object to display
    Precondition: hsv is an HSV object
    """
    result = a3.str5_hsv(hsv)
    if result is None:
        return ''
    return result 


pass
#mark -
#mark Utility Widgets
class Separator(Widget):
    """
    A class to space out widgets from one another.
    
    This class is cosmetic and simply gives us some edge definition
    """
    # The background color of the left edge
    left  = ListProperty([1,1,1,1])
    # The background color of the right edge
    right = ListProperty([1,1,1,1])


class PanelHeader(Label):
    """
    A label header for each subpanel.
    
    This class is essentially a label with predefined features for convenience. 
    It is fully defined in colormodel.kv
    """
    pass


class ColorArc(InstructionGroup):
    """
    A color arc (color wheel segment) created using OpenGL
    
    This code is heavily adapted (with permission) from
        
        https://kivy.org/doc/stable/_modules/kivy/uix/colorpicker.html
    
    We have removed alpha, as it is not relevant.
    """
    
    def __init__(self, r_min, r_max, theta_min, theta_max, **kwargs):
        """
        Initializes a new color arc.
        
        Parameter r_min: The minimum segment radius
        Precondition: r_min a float <= r_max
        
        Parameter r_max: The maximum segment radius
        Precondition: r_max a float >= r_min
        
        Parameter theta_min: The minimum segment angle
        Precondition: theta_min is a float is 0..2pi, theta_min <= theta_max
        
        Parameter theta_max: The maximum segment angle
        Precondition: theta_max is a float is 0..2pi, theta_min <= theta_max
        
        Parameter kwargs: Additional kivy keyword arguments
        """
        super(ColorArc, self).__init__(**kwargs)
        self.r_min = r_min
        self.r_max = r_max
        self.theta_min = theta_min
        self.theta_max = theta_max
        self.origin = kwargs['origin'] if 'origin' in kwargs else (0, 0)
        self.color =  list(kwargs['color'] if 'color' in kwargs else (0, 0, 1, 1))
        
        if 'origin' in kwargs:
            del kwargs['origin']
        if 'color' in kwargs:
            del kwargs['color']
        super(ColorArc, self).__init__(**kwargs)
        
        self.color_instr = Color(*self.color, mode='hsv')
        self.add(self.color_instr)
        self.mesh = self.get_mesh()
        self.add(self.mesh)
    
    def __str__(self):
        """
        Returns a string representation of this arc segment (for debugging)
        """
        return "r_min: %s r_max: %s theta_min: %s theta_max: %s color: %s" % (
            self.r_min, self.r_max, self.theta_min, self.theta_max, self.color
        )
    
    def get_mesh(self):
        """
        Returns a newly created OpenGL mesh for this segment.
        """
        v = []
        # first calculate the distance between endpoints of the inner
        # arc, so we know how many steps to use when calculating
        # vertices
        end_point_inner = self.polar_to_rect(self.origin, self.r_min, self.theta_max)
        
        d_inner = d_outer = 3.
        theta_step_inner = (self.theta_max - self.theta_min) / d_inner
        
        end_point_outer = self.polar_to_rect(self.origin, self.r_max, self.theta_max)
        
        if self.r_min == 0:
            theta_step_outer = (self.theta_max - self.theta_min) / d_outer
            for x in range(int(d_outer)):
                v += (self.polar_to_rect(self.origin, 0, 0) * 2)
                v += (self.polar_to_rect(self.origin, self.r_max, 
                                         self.theta_min + x * theta_step_outer) * 2)
        else:
            for x in range(int(d_inner + 1)):
                v += (self.polar_to_rect(self.origin, self.r_min - 1,
                                         self.theta_min + x * theta_step_inner) * 2)
                v += (self.polar_to_rect(self.origin, self.r_max + 1,
                                         self.theta_min + x * theta_step_inner) * 2)
        
        v += (end_point_inner * 2)
        v += (end_point_outer * 2)
        
        return Mesh(vertices=v, indices=range(int(len(v) / 4)), mode='triangle_strip')
    
    def change_value(self, value):
        """
        Changes the HSV value for this segment.
        
        The value is external to the segment, and is 1 by default, but can be changed.
        
        Parameter value: The new hsv value
        Precondition: value is a float in 0..1
        """
        self.remove(self.color_instr)
        self.color[2] = value
        self.color_instr = Color(*self.color, mode='hsv')
        self.insert(0, self.color_instr)
    
    @classmethod
    def distance(cls, pt1, pt2):
        """
        Returns the distance between points pt1 and pt2
        
        This is a utility function used throughout this file.
        
        Parameter pt1: The first point
        Precondition: pt1 a list of two floats
        
        Parameter pt2: The second point
        Precondition: pt2 a list of two floats
        """
        return math.sqrt((pt1[0] - pt2[0]) ** 2. + (pt1[1] - pt2[1]) ** 2.)
    
    @classmethod
    def polar_to_rect(cls, origin, r, theta):
        """
        Returns a point in rectangular coordinates given polar coordinates.
        
        This is a utility function used throughout this file.
        
        Parameter origin: The polar origin in rectangular coordinates
        Precondition: origin a list of two floats
        
        Parameter r: The radius coordinate
        Precondition: r is a float >= 0
        
        Parameter theta: The angular coordinate
        Precondition: theta is a float in 0..math.pi*2
        """
        return origin[0] + r * math.cos(theta), origin[1] + r * math.sin(theta)
    
    @classmethod
    def rect_to_polar(cls, origin, x, y):
        """
        Returns a point in polar coordinates given rectangular coordinates.
        
        This is a utility function used throughout this file.
        
        Parameter origin: The polar origin in rectangular coordinates
        Precondition: origin a list of two floats
        
        Parameter x: The x coordinate
        Precondition: x is a float
        
        Parameter y: The y coordinate
        Precondition: y is a float
        """
        if x == origin[0]:
            if y == origin[1]:
                return (0, 0)
            elif y > origin[1]:
                return (y - origin[1], math.pi / 2.)
            else:
                return (origin[1] - y, 3 * math.pi / 2.)
        t = math.atan(float((y - origin[1])) / (x - origin[0]))
        if x - origin[0] < 0:
            t += math.pi
        
        if t < 0:
            t += 2 * math.pi
        
        return (cls.distance((x, y), origin), t)


class HSVWheel(Widget):
    """
    A chromatic wheel supporting HSV colors
    
    This code is heavily adapted (with permission) from
        
        https://kivy.org/doc/stable/_modules/kivy/uix/colorpicker.html
    
    We have removed alpha, as it is not relevant. We have also removed the gestures,
    in order to customize this for traditional mouse support. The value property is
    now external and provided by other input sources.
    """
    # The hue and saturation (other widgets should observe this)
    # Direct access is only safe for READ-ONLY access
    huesat = ListProperty([0.0, 0.0])
    # The value (lumens).  This value is read-write safe, as it only affects graphics
    value  = BoundedNumericProperty(1, min=0, max=1)
    
    # The number of concentric circles (lower in kv file for weaker graphics cards)
    radial_segments  = NumericProperty(10)
    # The angular segments (lower in kv file for weaker graphics cards)
    angular_segments = NumericProperty(16)
    
    # The position of the control knob in rectangular coordinates
    knob_pos  = ListProperty([0, 0])
    # The knob radius in pts (not pixels)
    knob_size = NumericProperty(20)
    # The factor of the knob outline
    KNOB_FACTOR = 1.5
    
    def __init__(self, **kwargs):
        """
        Initializes a new color wheel.
        
        Parameter kwargs: Additional kivy keyword arguments
        """
        super(HSVWheel, self).__init__(**kwargs)
        self.origin = (self.pos[0]+self.size[0]/2,self.pos[1]+self.size[1]/2)
        self.radius = min(self.size[0],self.size[1])/2 - dp(10)
        self.selected = None
        self.wheelmesh = InstructionGroup()
        self.canvas.add(self.wheelmesh)
        self.bind(value=self.recolor)
    
    def init_wheel(self, dt):
        """
        (Re)initializes the OpenGL meshes for the wheel
        
        Parameter dt: the time since last initialization
        Precondition: dt is a float
        """
        # initialize list to hold all meshes
        self.wheelmesh.clear()
        self.arcs = []
        self.sv_idx = 0
        pdv = self.radial_segments
        ppie = self.angular_segments
        
        self.origin = (self.pos[0]+self.size[0]/2,self.pos[1]+self.size[1]/2)
        self.radius = min(self.size[0],self.size[1])/2 - dp(10)
        for r in range(pdv):
            for t in range(ppie):
                self.arcs.append(
                    ColorArc(
                        self.radius * (float(r) / float(pdv)),
                        self.radius * (float(r + 1) / float(pdv)),
                        2 * math.pi * (float(t) / float(ppie)),
                        2 * math.pi * (float(t + 1) / float(ppie)),
                        origin=self.origin,
                        color=(float(t) / ppie,
                               float(r) / pdv,
                               self.value,
                               1)))
                
                self.wheelmesh.add(self.arcs[-1])
    
    def recolor(self,instance,value):
        """
        Recolors the color wheel for a new HSV brightness value
        
        Parameter instance: the Kivy widget setting the new value
        Precondition: instance is a Kivy widget
        
        Parameter value: the new brightness value
        Precondition: value is a float in 0..1
        """
        for segment in self.arcs:
            segment.change_value(value)
    
    def on_touch_down(self, touch):
        """
        Responds to a mouse down event
        
        If the mouse down is inside the knob, it will start to move the knob.
        
        Parameter touch: the mouse down information
        Precondition: touch is a Kivy touch event
        """
        vec = [touch.pos[0]-self.origin[0], touch.pos[1]-self.origin[1]]
        dis = ColorArc.distance(self.knob_pos,vec)
        if dis <= dp(self.knob_size)*self.KNOB_FACTOR:
            touch.grab(self)
            self.selected = touch.pos
    
    def on_touch_move(self, touch):
        """
        Responds to a mouse move event.
        
        This method is only relevant if the knob is actively moving.
        
        Parameter touch: the mouse move information
        Precondition: touch is a Kivy touch event
        """
        if touch.grab_current is not self or not self.selected:
            return
        
        origin = [0,0]
        new_knob = self.knob_pos[:]
        new_knob[0] += touch.pos[0]-self.selected[0]
        new_knob[1] += touch.pos[1]-self.selected[1]
        
        (r,t) = ColorArc.rect_to_polar(origin,new_knob[0],new_knob[1])
        if r > self.radius:
            r = self.radius
        new_knob = ColorArc.polar_to_rect(origin,r,t)
        
        adjust = [0,0]
        adjust[0] = (new_knob[0]-self.knob_pos[0])+self.selected[0]
        adjust[1] = (new_knob[1]-self.knob_pos[1])+self.selected[1]
        self.selected = adjust
        
        self.knob_pos[0] = new_knob[0]
        self.knob_pos[1] = new_knob[1]
        
        t *= 180.0/math.pi # Degrees
        t = t % 360
        r /= self.radius
        self.huesat = [t,r]
    
    def on_touch_up(self, touch):
        """
        Responds to a mouse up event.
        
        This method is only relevant if the knob is actively moving.
        
        Parameter touch: the mouse up information
        Precondition: touch is a Kivy touch event
        """
        if touch.grab_current is self:
            touch.ungrab(self)
            self.selected = None
    
    def setHue(self,hue):
        """
        Sets the hue, updating the knob position.
        
        This method is for "pushing down" a hue to synchronize it with other
        input sources.  Direct write access to the huesat attribute is unsafe.
        
        Parameter hue: The new hue value
        Precondition: hue is a float 0..360
        """
        hue = hue % 360
        t = hue*math.pi/180.0
        r = self.huesat[1]*self.radius
        knob = ColorArc.polar_to_rect([0,0],r,t)
        
        self.knob_pos[0] = knob[0]
        self.knob_pos[1] = knob[1]
        self.huesat[0] = hue
    
    def setSat(self,sat):
        """
        Sets the saturation, updating the knob position.
        
        This method is for "pushing down" a saturation to synchronize it with other
        input sources.  Direct write access to the huesat attribute is unsafe.
        
        Parameter sat: The new saturation value
        Precondition: sat is a float 0..1
        """
        t = self.huesat[0]*math.pi/180.0
        r = sat*self.radius
        knob = ColorArc.polar_to_rect([0,0],r,t)
        
        self.knob_pos[0] = knob[0]
        self.knob_pos[1] = knob[1]
        self.huesat[1] = sat


class SliderField(BoxLayout):
    """
    A class to implement a slider/field combination.
    
    This is a convenience class as many of the inputs work with text input/slider
    combinations. It keeps the text field and slider in sync and provides a unified
    observable value for higher-level widgets.
    """
    # The background color (for melding into the background)
    color = ListProperty([1,1,1,1])
    # The foreground color (for melding into the background)
    text_color = ListProperty([0,0,0,1])
    # A reference to the slider child widget
    slider = ObjectProperty(None)
    # A reference to the text input child widget
    field  = ObjectProperty(None)
    # A name label for display up tp[
    text = ObjectProperty("")
    
    # The unified value (other widgets should observe this)
    # Direct access is only safe for READ-ONLY access
    value = NumericProperty(1.0)
    # The initial value as start-up (override in the kv file)
    initial = NumericProperty(10000)
    # The maximum slider value (override in the kv file)
    max_val = NumericProperty(10000)
    # The minimum slider value (override in the kv file)
    min_val = NumericProperty(0)
    # Amount to divide the slider value to get the unified value (override in the kv file)
    factor  = NumericProperty(10000)
    
    # The number of decimals to display in the text box (0 means round to int)
    decimals = NumericProperty(3)
    
    # A semaphore-style lock to prevent infinite cascade in Kivy events 
    lock = BooleanProperty(False)
    
    def on_kv_post(self, widget):
        """
        Links and registers all children after the KV file has been processed
        
        Parameter widget: This object, after kv initialization
        Precondition: widget is this object
        """
        if self.slider:
            self.slider.bind(value=self.update_on_slide)
            self.update_on_slide(self,self.initial)
    
    def validate_text(self,text):
        """
        Returns the number for the given text, or None if it is invalid
        
        Parameter text: The text to convert to a number
        Precondition: text is a string
        """
        try:
            value = float(text)
            return self.validate_number(value)
        except:
            return None
    
    def validate_number(self,value):
        """
        Returns this number rounded to the appropriate decimals, or None if it is invalid
        
        This method uses self.decimals to determine the number of places to round to.
        If the number is outside of range (min_val to max_val), this method will 
        return None.
        
        Parameter value: The number to verify
        Precondition: value is an int or float
        """
        if self.decimals:
            value = round(value,self.decimals)
        else:
            value = round(value)
        
        if self.min_val/self.factor <= value  and value <= self.max_val/self.factor:
            return value
        
        return None
    
    def update_on_slide(self, instance, value):
        """
        Updates the value property to match the child slider.
        
        Parameter instance: the reporting slider
        Precondition: instance is the child Slider object
        
        Parameter value: the new slider value
        Precondition: value is an int
        """
        if self.lock:
            return
        
        self.lock = True # Prevent infinite event recursion
        
        value = self.validate_number(value/self.factor)
        if self.value == value:  # Hack because of poor Kivy design
            self.value = value+1 if value < self.max_val else value-1
        self.value = value
        if self.field:
            self.field.focus = False
            self.field.text = str(value)
        
        self.lock = False
        
    
    def update_on_text(self, instance, text):
        """
        Updates the value property to match the child text input
        
        Parameter instance: the reporting text input
        Precondition: instance is the child TextInput object
        
        Parameter text: the new text input
        Precondition: value is a string
        """
        if self.lock:
            return
        
        self.lock = True # Prevent infinite event recursion
        
        value = self.validate_text(text)
        if not value is None:
            if self.slider:
                self.slider.value = value*self.factor
            self.value = value
            self.field.text = str(value)
        elif self.field:
            self.field.text = str(self.value)
        
        self.lock = False
    
    def filter_text(self, text, from_undo):
        """
        Returns a truncated text value to prevent overflow in the text input.
        
        This method allows the user to type just enough into the text input field to
        be in range and have the given number of decimals. Any more than that, and it
        will stop accepting input.
        
        Parameter text: the new text to append to the input
        Precondition: text is a string
        
        Parameter from_undo: whether this result is from an undo operation
        Precondition: from_undo is a boolean
        """
        size = int(math.log10(self.max_val/self.factor))+1
        if self.min_val < 0:
            size = max(size,int(math.log10(-self.min_val/self.factor))+1)
        if self.decimals:
            size += self.decimals+1
        if '-' in self.field.text:
            size += 1
        return text[:size-len(self.field.text)]
    
    def setValue(self,value):
        """
        Sets the value, updating both the slider and the text field.
        
        This method is for "pushing down" a value to synchronize it with other
        input sources.  Direct write access to the value attribute is unsafe.
        
        Parameter value: The new numeric value
        Precondition: value is a number
        """
        self.lock = True # Prevent infinite event recursion
        
        value = self.validate_number(value)
        if not value is None:
            if self.slider:
                self.slider.value = value*self.factor
            if self.field:
                self.field.text = str(value)
            self.value = value
        
        self.lock = False


pass
#mark -
#mark Input Panels

class RGBInputPanel(BoxLayout):
    """
    An input panel for defining an RGB color.
    
    This panels stores its internal state as a color property. It consists of three
    separate slider fields.
    """
    # The current active color (other widgets should observe this)
    # Direct access is only safe for READ-ONLY access
    color = ListProperty([0, 0, 0])
    # Reference to the red slider
    rSlider = ObjectProperty(None)
    # Reference to the green slider
    gSlider = ObjectProperty(None)
    # Reference to the blue slider
    bSlider = ObjectProperty(None)
    
    def on_kv_post(self, widget):
        """
        Links and registers all children after the KV file has been processed
        
        Parameter widget: This object, after kv initialization
        Precondition: widget is this object
        """
        if self.rSlider:
            self.rSlider.bind(value=self.pollSlider)
            self.color[0] = self.rSlider.value
        if self.gSlider:
            self.gSlider.bind(value=self.pollSlider)
            self.color[1] = self.gSlider.value
        if self.bSlider:
            self.bSlider.bind(value=self.pollSlider)
            self.color[2] = self.bSlider.value
    
    def pollSlider(self, instance, value):
        """
        Polls the latest color value from a slider change
        
        Parameter instance: the reporting instance
        Precondition: instance is a SliderField
        
        Parameter value: the color value
        Precondition: value is an int 0..255
        """
        if instance == self.rSlider:
            self.color[0] = value
        elif instance == self.gSlider:
            self.color[1] = value
        elif instance == self.bSlider:
            self.color[2] = value
    
    def setColor(self, r, g, b):
        """
        Sets the color value for this input device, updating all sliders.
        
        This method is for "pushing down" a color to synchronize it with other
        input sources.  Direct write access to the color attribute is unsafe.
        
        Parameter r: the red value
        Precondition: r is an int 0..255
        
        Parameter g: the green value
        Precondition: g is an int 0..255
        
        Parameter b: the blue value
        Precondition: b is an int 0..255
        """
        if self.rSlider:
            self.rSlider.setValue(r)
        else:
            self.color[0] = r
        if self.gSlider:
            self.gSlider.setValue(g)
        else:
            self.color[1] = g
        if self.bSlider:
            self.bSlider.setValue(b)
        else:
            self.color[2] = g


class CMYKInputPanel(BoxLayout):
    """
    An input panel for defining a CMYK color.
    
    This panels stores its internal state as a color property. It consists of four
    separate slider fields.
    """
    # The current active color (other widgets should observe this)
    # Direct access is only safe for READ-ONLY access
    color = ListProperty([0, 0, 0, 0])
    # Reference to the cyan slider
    cSlider = ObjectProperty(None)
    # Reference to the magenta slider
    mSlider = ObjectProperty(None)
    # Reference to the yellow slider
    ySlider = ObjectProperty(None)
    # Reference to the black slider
    kSlider = ObjectProperty(None)
    
    def on_kv_post(self, widget):
        """
        Links and registers all children after the KV file has been processed
        
        Parameter widget: This object, after kv initialization
        Precondition: widget is this object
        """
        if self.cSlider:
            self.cSlider.bind(value=self.pollSlider)
            self.color[0] = self.cSlider.value
        if self.mSlider:
            self.mSlider.bind(value=self.pollSlider)
            self.color[1] = self.mSlider.value
        if self.ySlider:
            self.ySlider.bind(value=self.pollSlider)
            self.color[2] = self.ySlider.value
        if self.kSlider:
            self.kSlider.bind(value=self.pollSlider)
            self.color[3] = self.kSlider.value
    
    def pollSlider(self, instance, value):
        """
        Polls the latest color value from a slider change
        
        Parameter instance: the reporting instance
        Precondition: instance is a SliderField
        
        Parameter value: the color value
        Precondition: value is an float 0..100
        """
        if instance == self.cSlider:
            self.color[0] = value
        elif instance == self.mSlider:
            self.color[1] = value
        elif instance == self.ySlider:
            self.color[2] = value
        elif instance == self.kSlider:
            self.color[3] = value
    
    def setColor(self, c, m, y, k):
        """
        Sets the color value for this input device, updating all sliders.
        
        This method is for "pushing down" a color to synchronize it with other
        input sources.  Direct write access to the color attribute is unsafe.
        
        Parameter c: the cyan value
        Precondition: c is a float 0.0..100.0
        
        Parameter m: the magenta value
        Precondition: m is a float 0.0..100.0
        
        Parameter y: the yellow value
        Precondition: y is a float 0.0..100.0
        
        Parameter k: the yellow value
        Precondition: k is a float 0.0..100.0
        """
        if self.cSlider:
            self.cSlider.setValue(c)
        else:
            self.color[0] = c
        if self.mSlider:
            self.mSlider.setValue(m)
        else:
            self.color[1] = m
        if self.ySlider:
            self.ySlider.setValue(y)
        else:
            self.color[2] = y
        if self.kSlider:
            self.kSlider.setValue(k)
        else:
            self.color[3] = k


class HSVInputPanel(BoxLayout):
    """
    An input panel for defining a HSV color.
    
    This panels stores its internal state as a color property. It consists of a color
    wheel, a slider, and three text fields.
    """
    # The current active color (other widgets should observe this)
    # Direct access is only safe for READ-ONLY access
    color = ListProperty([0, 0, 1])
    # Reference to the color wheel
    hsWheel = ObjectProperty(None)
    # Reference to the value slider
    vSlider = ObjectProperty(None)
    # Reference to the hue text field
    hField = ObjectProperty(None)
    # Reference to the saturation text field
    sField = ObjectProperty(None)
    # Reference to the value text field
    vField = ObjectProperty(None)
    
    # A semaphore-style lock to prevent infinite cascade in Kivy events 
    lock = BooleanProperty(False)
    
    def on_kv_post(self, widget):
        """
        Links and registers all children after the KV file has been processed
        
        Parameter widget: This object, after kv initialization
        Precondition: widget is this object
        """
        if self.lock:
            return
        
        self.lock = True
        
        h = self.color[0]
        s = self.color[1]
        v = self.color[2]
        
        if self.hsWheel:
            self.hsWheel.bind(huesat=self.pollWheel)
            h = self.hsWheel.huesat[0]
            s = self.hsWheel.huesat[1]
        if self.vSlider:
            self.vSlider.bind(value=self.pollSlider)
            v = round(self.vSlider.value/self.vSlider.max,3)
        if self.hField:
            self.hField.index = 0
            self.hField.text = str(h)
        if self.sField:
            self.sField.index = 1
            self.sField.text = str(s)
        if self.vField:
            self.vField.index = 2
            self.vField.text = str(v)
        
        self.color[0] = h
        self.color[1] = s
        self.color[2] = v
        
        self.lock = False
    
    def validate_text(self,instance,text):
        """
        Returns the number for the given text, or None if it is invalid
        
        Parameter instance: the reporting text input
        Precondition: instance is one of the three Text Input children
        
        Parameter text: The text to convert to a number
        Precondition: text is a string
        """
        try:
            value = round(float(text),3)
            if instance == self.hField:
                while value < 0:
                    value += 360
                value = value % 360
            elif value < 0 or value > 1:
                return None
            
            return value
        except:
            return None

    def update_on_text(self, instance, text):
        """
        Updates a color attribute to match the child text input
        
        Parameter instance: the reporting text input
        Precondition: instance is one of the three Text Input children
        
        Parameter text: the new text input
        Precondition: value is a string
        """
        if self.lock or not hasattr(instance,'index'):
            return
        
        self.lock = True # Prevent infinite event recursion
        
        oldvalue = self.color[instance.index]
        newvalue = self.validate_text(instance,text)
        if not newvalue is None:
            if instance.index == 2:
                if self.vSlider:
                    self.vSlider.value = newvalue*self.vSlider.max
                if self.hsWheel:
                    self.hsWheel.value = newvalue
            elif self.hsWheel:
                if instance.index == 0:
                    self.hsWheel.setHue(newvalue)
                else:
                    self.hsWheel.setSat(newvalue)
            instance.text = str(newvalue)
            self.color[instance.index] = newvalue
        else:
            instance.text = str(oldvalue)
        
        self.lock = False
    
    def pollSlider(self, instance, value):
        """
        Polls the latest value from a slider change
        
        Parameter instance: the reporting instance
        Precondition: instance is the child value Slider
        
        Parameter value: the hsv brightness value
        Precondition: value is an float 0..1
        """
        if self.lock:
            return
        
        self.lock = True # Prevent infinite event recursion
        
        value = round(value/self.vSlider.max,3)
        if self.hsWheel:
            self.hsWheel.value = value
        if self.vField:
            self.vField.text = str(value)
        self.color[2] = value
        
        self.lock = False
    
    def pollWheel(self, instance, value):
        """
        Polls the latest hue and saturation from the color wheel
        
        Parameter instance: the reporting instance
        Precondition: instance is the child HSVWheel
        
        Parameter value: the hue and saturation
        Precondition: value is an list of float 0..360 and float 0..1
        """
        if self.lock:
            return
        
        self.lock = True # Prevent infinite event recursion
        
        hue = round(value[0],3) % 360
        sat = round(value[1],3)
        if self.hField:
            self.hField.text = str(hue)
        if self.sField:
            self.sField.text = str(sat)
        self.color[0] = hue
        self.color[1] = sat
        
        self.lock = False
    
    def setColor(self,h,s,v):
        """
        Sets the color value for this input device, updating input features.
        
        This method is for "pushing down" a color to synchronize it with other
        input sources.  Direct write access to the color attribute is unsafe.
        
        Parameter h: the hue value
        Precondition: h is a float 0.0..360.0
        
        Parameter s: the saturation value
        Precondition: s is a float 0.0..1.0
        
        Parameter v: the brightness value
        Precondition: v is a float 0.0..1.0
        """
        if self.lock:
            return
        
        self.lock = True # Prevent infinite event recursion
        
        if self.hsWheel:
            self.hsWheel.setHue(h)
            self.hsWheel.setSat(s)
            self.hsWheel.value = v
        if self.vSlider:
            self.vSlider.value = v*self.vSlider.max
        if self.hField:
            self.hField.text = str(round(h,3))
        if self.sField:
            self.sField.text = str(round(s,3))
        if self.vField:
            self.vField.text = str(round(v,3))
        self.color[0] = round(h,3)
        self.color[1] = round(s,3)
        self.color[2] = round(v,3)
        
        self.lock = False


pass
#mark -
#mark Color Panels

class ColorPanel(BoxLayout):
    """
    A class to display a color and its complement.
    
    This is really just an exalted label, with fine tune control over colors.
    """
    # The font color
    foreground = ListProperty([1,0,0,1])
    # The panel color
    background = ListProperty([0,1,1,1])
    # The text contents
    text  = ObjectProperty("")


class ContrastPanel(BoxLayout):
    """
    A ColorPanel variation with a slider.
    
    The contrast setting is a localized input. Therefore, we attach it to the color
    panel that uses it.
    """
    # The font color
    foreground = ListProperty([1,0,0,1])
    # The panel color
    background = ListProperty([0,1,1,1])
    # The text contents
    text  = ObjectProperty("")
    # A reference to the contrast SliderField
    slider = ObjectProperty(None)


pass
#mark -
#mark Primary Application
class ColorWidget(BoxLayout):
    """
    A class to implement the fully integrated application.
    
    This class synchronizes the input panels and uses them to set the color settings
    in the various color panels. It depends heavily on the completion of a3.py. Until
    that file is completed, it will not do much.
    """
    # Reference to the RGB input panel
    rgbPanel  = ObjectProperty(None)
    # Reference to the CMYK input panel
    cmykPanel = ObjectProperty(None)
    # Reference to the HSV input panel
    hsvPanel  = ObjectProperty(None)
    # Reference to the main (central) color panel
    mainPanel = ObjectProperty(None)
    # Reference to the complementary color panel
    compPanel = ObjectProperty(None)
    # Reference to the contrast panel
    contPanel = ObjectProperty(None)
    # Reference to the edge separator between the complement and main
    leftSep  = ObjectProperty(None)
    # Reference to the edge separator between the main and contrast
    rightSep = ObjectProperty(None)
    
    # A semaphore-style lock to prevent infinite cascade in Kivy events 
    lock = BooleanProperty(False)
    
    # Color attributes for display and synchronization
    rgb  = introcs.RGB(255,255,255)
    cmyk = None
    hsv  = None
    
    def on_kv_post(self, widget):
        """
        Links and registers all children after the KV file has been processed
        
        Parameter widget: This object, after kv initialization
        Precondition: widget is this object
        """
        if self.rgbPanel:
            self.rgbPanel.bind(color=self.syncInput)
            self.rgb = introcs.RGB(*self.rgbPanel.color)
        if self.cmykPanel:
            self.cmykPanel.bind(color=self.syncInput)
            self.cmyk = a3.rgb_to_cmyk(self.rgb)
        if self.hsvPanel:
            self.hsvPanel.bind(color=self.syncInput)
            self.hsv  = a3.rgb_to_hsv(self.rgb)
        if self.contPanel and self.contPanel.slider:
            self.contPanel.slider.bind(value=self.recalibrate)
        self.recolor()
    
    def syncInput(self, instance, value):
        """
        Synchronizes all input between input panels.
        
        This is called whenever the user updates and input panel. This code uses the
        conversion functions in a3.py to automatically update the other two panels.
        
        Parameter instance: the reporting input instance
        Precondition: instance is one of the three input panels
        
        Parameter value: the color value
        Precondition: value the color property of instance
        """
        if self.lock:
            return
        
        self.lock = True # Prevent infinite event recursion
        
        if instance == self.rgbPanel:
            self.rgb  = introcs.RGB(*value)
            self.cmyk = a3.rgb_to_cmyk(self.rgb)
            if not self.cmyk is None:
                assert (type(self.cmyk) == introcs.CMYK), 'rgb_to_cmyk does not return a CMYK object'
                self.cmykPanel.setColor(self.cmyk.cyan,self.cmyk.magenta,self.cmyk.yellow,self.cmyk.black)
            self.hsv  = a3.rgb_to_hsv(self.rgb)
            if not self.hsv is None:
                assert (type(self.hsv) == introcs.HSV), 'rgb_to_hsv does not return a HSV object'
                self.hsvPanel.setColor(self.hsv.hue,self.hsv.saturation,self.hsv.value)
        elif instance == self.cmykPanel:
            self.cmyk = introcs.CMYK(*value)
            rgb = a3.cmyk_to_rgb(self.cmyk)
            if not rgb is None:
                assert (type(rgb) == introcs.RGB), 'cmyk_to_rgb does not return a RGB object'
                self.rgbPanel.setColor(rgb.red,rgb.green,rgb.blue)
                self.rgb = rgb
            else:
                self.cmyk = None
            self.hsv  = a3.rgb_to_hsv(self.rgb)
            if not self.hsv is None:
                assert (type(self.hsv) == introcs.HSV), 'rgb_to_hsv does not return a HSV object'
                self.hsvPanel.setColor(self.hsv.hue,self.hsv.saturation,self.hsv.value)
        elif instance == self.hsvPanel:
            self.hsv = introcs.HSV(*value)
            rgb = a3.hsv_to_rgb(self.hsv)
            if not rgb is None:
                assert (type(rgb) == introcs.RGB), 'hsv_to_rgb does not return a RGB object'
                self.rgbPanel.setColor(rgb.red,rgb.green,rgb.blue)
                self.rgb = rgb
            else:
                self.hsv = None
            self.cmyk = a3.rgb_to_cmyk(self.rgb)
            if not self.cmyk is None:
                assert (type(self.cmyk) == introcs.CMYK), 'rgb_to_cmyk does not return a CMYK object'
                self.cmykPanel.setColor(self.cmyk.cyan,self.cmyk.magenta,self.cmyk.yellow,self.cmyk.black)
        
        self.recolor()
        self.lock = False
    
    def recalibrate(self,instance,value):
        """
        Recalibrates the contrast panel to use the new color and contrast.
        
        This can be called for two different events: a change in color or a change
        in contrast. On a change in color, instance and value will be None, but 
        self.rgb will have the current correct color.
        
        Parameter instance: the reporting input instance
        Precondition: instance is one of the three input panels or None
        
        Parameter value: the color value
        Precondition: value the color property of instance or None
        """
        if not self.contPanel.slider:
            return
        
        cRGB  = introcs.RGB(self.rgb.red,self.rgb.green,self.rgb.blue)
        cComp = a3.complement_rgb(self.rgb)
        cComp = introcs.RGB(cComp.red,cComp.green,cComp.blue)
        level = self.contPanel.slider.value
        a3.contrast_rgb(cRGB,level)
        a3.contrast_rgb(cComp,level)
        self.contPanel.foreground = cComp.glColor()
        self.contPanel.background = cRGB.glColor()
        
        if self.rightSep:
            if self.mainPanel:
                self.rightSep.left  = self.mainPanel.background
            if self.contPanel:
                self.rightSep.right = self.contPanel.background
    
    def recolor(self):
        """
        Recolors the three bottom color panels.
        """
        compRGB = a3.complement_rgb(self.rgb)
        if (compRGB is None):
            compRGB = self.rgb
        
        
        rgb_str  = str_rgb(self.rgb)
        cmyk_str = '' if self.cmyk is None else str_cmyk(self.cmyk) 
        hsv_str  = '' if self.hsv is None else str_hsv(self.hsv)
        text = ('Color\n' +
                'RGB:    ' + rgb_str +'\n'+
                'CMYK: ' + cmyk_str +'\n'+
                'HSV:    ' + hsv_str + '\n \n' +
                'R,G,B sliders in: 0..255\n' +
                'C,M,Y,K sliders: 0 to 100%\n' +
                'Color Wheel: 360 degrees, radius 1\n'+
                'V slider: 0 to 1')
        if self.mainPanel:
            self.mainPanel.text = text
            self.mainPanel.background = self.rgb.glColor()
            self.mainPanel.foreground = compRGB.glColor()
        
        if self.compPanel:
            self.compPanel.text = text
            self.compPanel.foreground = self.rgb.glColor()
            self.compPanel.background = compRGB.glColor()
        
        if self.contPanel:
            self.contPanel.text = text
            self.recalibrate(None,None)
        
        if self.leftSep:
            if self.compPanel:
                self.leftSep.left  = self.compPanel.background
            if self.mainPanel:
                self.leftSep.right = self.mainPanel.background
        
        if self.rightSep:
            if self.mainPanel:
                self.rightSep.left  = self.mainPanel.background
            if self.contPanel:
                self.rightSep.right = self.contPanel.background


class ColorModelApp(App):
    """
    The Kivy entry-point for the color model application
    """
    def build(self):
        """
        Reads the kivy file and performs the layout
        """
        Config.set('graphics', 'multisamples', '0')
        Config.set('graphics', 'width', '900')
        Config.set('graphics', 'height', '600')
        Config.set('graphics', 'resizable', False)
        return ColorWidget()


pass
#mark -
#mark Application Code
if __name__ in ('__android__', '__main__'):
    # .kv initialization
    Factory.register("Separator", Separator)
    Factory.register("ColorPanel", ColorPanel)
    Factory.register("SliderField", SliderField)
    Factory.register("RGBInputPanel", RGBInputPanel)
    Factory.register("CMYKInputPanel", CMYKInputPanel)
    Factory.register("HSVInputPanel", HSVInputPanel)
    Factory.register("HSVWheel", HSVWheel)
    Factory.register("ColorWidget", ColorWidget)
    ColorModelApp().run()