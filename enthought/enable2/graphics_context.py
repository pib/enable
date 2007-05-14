
# Enthought library imports
from enthought.kiva import GraphicsContext
from enthought.traits.api import Instance

# Relative imports
from abstract_window import AbstractWindow
from base import bounding_coordinates, coordinates_to_bounds, default_font


class GraphicsContextEnable(GraphicsContext):
    """
    Subclass of Kiva GraphicsContext that provides a few more utility methods.
    Most importantly, it provides a pointer back to the window that this
    GC is being drawn to.
    
    This will eventually be deprecated as the follow methods are folded into
    Kiva or their use is discontinuted in Enable.
    """

    # The window that this GraphicsContext is being drawn to.  It is OK to leave
    # this as None if the graphics context is used as a backbuffer; however, in
    # such cases, it is more appropriate to use a GC from Kiva directly as opposed
    # to using the Enable one, as some draw methods may need to parent controls
    # or dialogs from the Window.
    window = Instance(AbstractWindow)

    def __init__(self, *args, **kwargs):
        if kwargs.has_key("window"):
            self.window = kwargs.pop("window")
        GraphicsContext.__init__(self, *args, **kwargs)
        return

    def clip_to_rect(self, x, y, width, height):
        GraphicsContext.clip_to_rect(self, x-0.5, y-0.5, width+1, height+1)

    def clear_clip(self, color, coordinates):
        "Clip and clear a Kiva graphics context to a specified area and color"
        bounds = coordinates_to_bounds(coordinates) 
        self.clip_to_rect(*bounds)
        self.set_fill_color(color)
        self.begin_path()
        self.rect(*bounds)
        self.fill_path()
        return
        
    def clear_clip_region(self, color, update_region):
        "Clip and clear a Kiva graphics context to a specified region and color"
        bounds = coordinates_to_bounds(bounding_coordinates(update_region))
        self.clip_to_rect(*bounds)
        self.set_fill_color(color)
        for coordinates in update_region:
            bounds = coordinates_to_bounds(coordinates) 
            self.begin_path()
            self.rect(*bounds)
        self.fill_path()
        return

    def alpha(self, alpha):
        raise NotImplementedError, \
            "The alpha() method is not compatible with DisplayPDF; use clear() instead."

    def stretch_draw(self, image, x, y, dx, dy):
        "Draws an image 'stretched' to fit a specified area"
        idx  = image.width()
        idy  = image.height()
        self.save_state()
        self.clip_to_rect(x, y, dx, dy)
        cx, cy, cdx, cdy = x, y, dx, dy
        yt = cy + cdy
        xr = cx + cdx
        x += (int(cx - x) / idx) * idx
        y += (int(cy - y) / idy) * idy
        while y < yt:
            x0 = x
            while x0 < xr:
                self.draw_image(image,(x0, y, idx, idy))
                x0 += idx
            y += idy
        self.restore_state()
        return
    
    #~ def text(self, text, bounds, font = default_font, color = black_color, 
             #~ shadow_color = white_color, style = 0, alignment = LEFT,
             #~ y_offset = 0.0, info = None):
        #~ "Draw a text string within a specified area with various attributes"
        #~ # Set up the font and get the text bounding box information:
        #~ self.set_font(font)
        #~ if info is None:
            #~ info = self.get_full_text_extent(text)
        #~ tdx, tdy, descent, leading = info
        
        #~ # Calculate the text position, based on its alignment:
        #~ xl, yb, dx, dy = bounds
        #~ y = yb + y_offset + (dy - tdy) / 2.0
        #~ if alignment & LEFT:
            #~ x = xl
        #~ elif alignment & RIGHT:
            #~ x = xl + dx - tdx - 4.0  # 4.0 is a hack!!!
        #~ else:
            #~ x = xl + (dx - tdx) / 2.0
        
        #~ self.save_state()
        #~ self.clip_to_rect(*bounds)
            
        #~ # Draw the normal text:
        #~ self.set_fill_color(color)
        #~ self.show_text(text, (x,y))
        
        #~ self.restore_state()
        #~ self.set_fill_color(color)
        #~ return

# EOF
