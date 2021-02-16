"""
Image processing methods for the imager application.

This module provides all of the image processing operations that are called 
whenever you press a button. Some of these are provided for you and others you
are expected to write on your own.

Note that this class is a subclass of Editor. This allows you to make use
of the undo functionality. You do not have to do anything special to take 
advantage of this.  Just make sure you use getCurrent() to access the most 
recent version of the image.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Arthur Wayne asw263
November 16 2020
"""
import a6editor
import a6image
import math # Just in case


class Filter(a6editor.Editor):
    """
    A class that contains a collection of image processing methods
    
    This class is a subclass of a6editor. That means it inherits all of the 
    methods and attributes of that class too. We do that (1) to put all of the 
    image processing methods in one easy to read place and (2) because we might 
    want to change how we implement the undo functionality later.
    
    This class is broken into three parts (1) implemented non-hidden methods, 
    (2) non-implemented non-hidden methods and (3) hidden methods. The 
    non-hidden methods each correspond to a button press in the main 
    application.  The hidden methods are all helper functions.
    
    Each one of the non-hidden functions should edit the most recent image 
    in the edit history (which is inherited from Editor).
    """
    
    # PROVIDED ACTIONS (STUDY THESE)
    def invert(self):
        """
        Inverts the current image, replacing each element with its color complement
        """
        current = self.getCurrent()
        for pos in range(len(current)): # We can do this because of __len__
            rgb = current[pos]          # We can do this because of __getitem__
            red   = 255 - rgb[0]
            green = 255 - rgb[1]
            blue  = 255 - rgb[2]
            rgb = (red,green,blue)      # New pixel value
            current[pos] = rgb          # We can do this because of __setitem__
    
    def transpose(self):
        """
        Transposes the current image
        
        Transposing is tricky, as it is hard to remember which values have been 
        changed and which have not.  To simplify the process, we copy the 
        current image and use that as a reference.  So we change the current 
        image with setPixel, but read (with getPixel) from the copy.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):      # Loop over the rows
            for col in range(current.getWidth()):   # Loop over the columnns
                current.setPixel(row,col,original.getPixel(col,row))
    
    def reflectHori(self):
        """
        Reflects the current image around the horizontal middle.
        """
        current = self.getCurrent()
        for h in range(current.getWidth()//2):      # Loop over the columnns
            for row in range(current.getHeight()):  # Loop over the rows
                k = current.getWidth()-1-h
                current.swapPixels(row,h,row,k)
    
    def rotateRight(self):
        """
        Rotates the current image right by 90 degrees.
        
        Technically, we can implement this via a transpose followed by a 
        horizontal reflection. However, this is slow, so we use the faster 
        strategy below.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):      # Loop over the rows
            for col in range(current.getWidth()):   # Loop over the columnns
                current.setPixel(row,col,original.getPixel(original.getHeight()-col-1,row))
    
    def rotateLeft(self):
        """
        Rotates the current image left by 90 degrees.
        
        Technically, we can implement this via a transpose followed by a 
        vertical reflection. However, this is slow, so we use the faster 
        strategy below.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):      # Loop over the rows
            for col in range(current.getWidth()):   # Loop over the columnns
                current.setPixel(row,col,original.getPixel(col,original.getWidth()-row-1))
    
    # ASSIGNMENT METHODS (IMPLEMENT THESE)
    def reflectVert(self):
        """ 
        Reflects the current image around the vertical middle.
        """
        current = self.getCurrent()
        for h in range(current.getHeight()//2):     # Loop over the rows
            for col in range(current.getHeight()):  # Loop over the columns
                k = current.getHeight()-1-h
                current.swapPixels(h,col,k,col)
    
    def monochromify(self, sepia):
        """
        Converts the current image to monochrome (greyscale or sepia tone).
        
        If `sepia` is False, then this function uses greyscale. It removes all
        color from the image by setting the three color components of each 
        pixel to that pixel's overall brightness, defined as 
            
            brightness = 0.3 * red + 0.6 * green + 0.1 * blue.
        
        If sepia is True, it makes the same computations as before but sets 
        green to 0.6 * brightness and blue to 0.4 * brightness (red is same as
        for greyscale).
        
        Parameter sepia: Whether to use sepia tone instead of greyscale.
        Precondition: sepia is a bool
        """
        assert type(sepia) == bool, repr(sepia) + " is not a bool"
        current = self.getCurrent()

        if sepia == False: #greyscale
            for row in range(current.getHeight()):      # Loop over the rows
                for col in range(current.getWidth()):   # Loop over the columnns
                    pixel = current.getPixel(row,col)
                    red = pixel[0]
                    green = pixel[1]
                    blue = pixel[2]
                    bness = int(0.3 * red + 0.6 * green + 0.1 * blue)
                    current.setPixel(row,col,(bness,bness,bness))
        else: #sepia
            for row in range(current.getHeight()):      # Loop over the rows
                for col in range(current.getWidth()):   # Loop over the columnns
                    pixel = current.getPixel(row,col)
                    red = pixel[0]
                    green = pixel[1]
                    blue = pixel[2]
                    bness = 0.3 * red + 0.6 * green + 0.1 * blue
                    current.setPixel(row,col,(int(bness), int(0.6 * bness), int(0.4 *bness)))        
    
    def jail(self):
        """
        Puts jail bars on the current image
        
        The jail should be built as follows:
        * Put 3-pixel-wide horizontal bars across top and bottom,
        * Put 4-pixel vertical bars down left and right, and
        * Put n 4-pixel vertical bars inside, where n is 
          (number of columns - 8) // 50.
        
        Note that the formula for the number of interior bars is explicitly
        not counting the two bars on the outside.
        
        The n+2 vertical bars should be as evenly spaced as possible.
        """
        current = self.getCurrent()

        red = (255,0,0)

        self._drawHBar(0,red)
        self._drawHBar(current.getHeight()-3,red)
        self._drawVBar(0,red)
        self._drawVBar(current.getWidth()-4,red)
        n = (current.getWidth() - 8) // 50
        spacing = (current.getWidth()-(4*(n+2)))/(n+1)
        for i in range(n): 
            self._drawVBar(int((4*(i+1))+(spacing*(i+1))),red)
    
    def vignette(self):
        """
        Modifies the current image to simulates vignetting (corner darkening).
        
        Vignetting is a characteristic of antique lenses. This plus sepia tone 
        helps give a photo an antique feel.
        
        To vignette, darken each pixel in the image by the factor
        
            1 - (d / hfD)^2
        
        where d is the distance from the pixel to the center of the image and 
        hfD (for half diagonal) is the distance from the center of the image 
        to any of the corners.  
        
        The values d and hfD should be left as floats and not converted to ints.
        Furthermore, when the final color value is calculated for each pixel,
        the result should be converted to int, but not rounded.
        """
        current = self.getCurrent()
        for row in range(current.getHeight()):      # Loop over the rows
            for cl in range(current.getWidth()):   # Loop over the columnns
                pixel = current.getPixel(row,cl)
                d=math.sqrt(((row-(current.getHeight()/2))**2)
                            +((cl-(current.getWidth()/2))**2))
                hfD=math.sqrt(((0-(current.getHeight()/2))**2)
                            +((0-(current.getWidth()/2))**2))
                darken = 1.0 - ((d/hfD)**2)
                red = int(pixel[0]*darken)
                green = int(pixel[1]*darken)
                blue = int(pixel[2]*darken)
                current.setPixel(row,cl,(red,green,blue))
    
    def pixellate(self,step):
        """
        Pixellates the current image to give it a blocky feel.
        
        To pixellate an image, start with the top left corner (e.g. the first 
        row and column).  Average the colors of the step x step block to the 
        right and down from this corner (if there are less than step rows or 
        step columns, go to the edge of the image). Then assign that average 
        to ALL of the pixels in that block.
        
        When you are done, skip over step rows and step columns to go to the 
        next corner pixel.  Repeat this process again.  The result will be a 
        pixellated image.
        
        When the final color value is calculated for each pixel, the result 
        should be converted to int, but not rounded.
        
        Parameter step: The number of pixels in a pixellated block
        Precondition: step is an int > 0
        """
        assert type(step) == int and step > 0, repr(step) + " is not a valid step"
        current = self.getCurrent()
        widthSteps = current.getWidth()//step
        heightSteps = current.getHeight()//step
        widthRem = current.getWidth()%step
        heightRem = current.getHeight()%step
        for i in range(heightSteps):
            for j in range(widthSteps):
                block = self._avging(i*step,j*step,step)
                # fill in a block with dimensions step x step, starting at row + (i*step) and col + (j*step)
                for row in range(step):
                    for col in range(step):
                        current.setPixel(row+(i*step), col+(j*step), block)
            # fill the rest in through width remainder width and step height
            if widthRem != 0:
                r = 0
                g = 0
                b = 0
                for ro in range(step):
                    for co in range(widthRem):
                        pixel = current.getPixel(ro+(i*step),co+(widthRem*step))
                        r += pixel[0]
                        g += pixel[1]
                        b += pixel[2]
                avgFactor = step*step        
                blok = (int(r/avgFactor),int(g/avgFactor),int(b/avgFactor))
                for k in range(step):
                    for l in range(widthRem):
                        current.setPixel(k+(i*step),l+(widthRem*step), blok)
        
        if heightRem != 0:
            r = 0
            g = 0
            b = 0
            for z in range(widthSteps):
                for ro in range(heightRem):
                    for co in range(step):
                        pixel = current.getPixel(ro+(heightRem*step),co+(z*step))
                        r += pixel[0]
                        g += pixel[1]
                        b += pixel[2]
                avgFactor = step*step        
                blok = (int(r/avgFactor),int(g/avgFactor),int(b/avgFactor))
                for k in range(heightRem):
                    for l in range(step):
                        current.setPixel(ro+(heightRem*step),co+(z*step), blok)

    # HELPER METHODS
    def _drawHBar(self, row, pixel):
        """
        Draws a horizontal bar on the current image at the given row.
        
        This method draws a horizontal 3-pixel-wide bar at the given row 
        of the current image. This means that the bar includes the pixels 
        row, row+1, and row+2. The bar uses the color given by the pixel 
        value.
        
        Parameter row: The start of the row to draw the bar
        Precondition: row is an int, 0 <= row  &&  row+2 < image height
        
        Parameter pixel: The pixel color to use
        Precondition: pixel is a 3-element tuple (r,g,b) of ints in 0..255
        """
        current = self.getCurrent()
        assert type(row) == int, repr(row) + " is not an int"
        assert (0<=row and row+2<current.getHeight()), repr(row)+"is not a valid row"
        assert a6image._is_pixel(pixel) == True, repr(pixel) + " is not a pixel"

        for col in range(current.getWidth()):
            current.setPixel(row,   col, pixel)
            current.setPixel(row+1, col, pixel)
            current.setPixel(row+2, col, pixel)

    def _drawVBar(self, col, pixel):
        """
        Draws a vertical bar on the current image at the given col.
        
        This method draws a vertical 4-pixel-wide bar at the given col 
        of the current image. This means that the bar includes the pixels 
        col, col+1, col+2, and col+3. The bar uses the color given by the pixel 
        value.
        
        Parameter col: The start of the col to draw the bar
        Precondition: col is an int, 0 <= col  &&  col + 3 < image width
        
        Parameter pixel: The pixel color to use
        Precondition: pixel is a 3-element tuple (r,g,b) of ints in 0..255
        """
        current = self.getCurrent()
        assert type(col) == int, repr(col) + " is not an int"
        assert (0<=col and col+3<current.getWidth()), repr(col)+" is not a valid col"
        assert a6image._is_pixel(pixel) == True, repr(pixel) + " is not a pixel"

        for row in range(current.getHeight()):
            current.setPixel(row, col, pixel)
            current.setPixel(row, col+1, pixel)
            current.setPixel(row, col+2, pixel)
            current.setPixel(row, col+3, pixel)

    def _avging(self, row, col, step):
        """
        Returns the a tuple of the average rgb values for a given step, starting at coordinate row, col
        
        Parameter step: The number of pixels in a pixellated block
        Precondition: step is an int > 0

        Parameter col: The starting column
        Precondition: col is an int, 0 <= col  &&  col < image width

        Parameter row: The starting row
        Precondition: row is an int, 0 <= row  &&  row < image height
        
        """
        current = self.getCurrent()
        assert type(step) == int and step > 0, repr(step) + " is not a valid step"
        assert type(col) == int and (0<=col and col<current.getWidth())
        assert type(row) == int and (0<=row and row<current.getHeight())
        r = 0
        g = 0
        b = 0
        for i in range(step):
            for j in range(step):
                pixel = current.getPixel(row+i,col+j)
                r += pixel[0]
                g += pixel[1]
                b += pixel[2]
        avgFactor = step*step        
        return (int(r/avgFactor),int(g/avgFactor),int(b/avgFactor))