from math import floor
from settings import DrawSettings

class WayElement:
    _width: float
    _height: float
    _distance: float
    colour: str
    background_colour: str

    def __init__(self: 'WayElement', width, height, colour = "grey"):
        self._width = width
        self._height = height
        self._distance = None
        self.colour = colour
        self.background_colour = None

    def set_distance(self : 'WayElement', distance, background_colour: str) -> None:
        self._distance = distance
        self.background_colour = background_colour

    def __str__(self: 'WayElement') -> str:
        return "Way_Element: " + str(self.__dict__)

    def convert_meter_to_pixel(self: 'WayElement', val):
        # floor to avoid floating point inaccuracies and weird subpixel gaps in the rendered svg
        return floor(val * DrawSettings()["pixel_pro_meter"])

    def width(self: 'WayElement') -> float:
        return self.convert_meter_to_pixel(self._width)

    def height(self: 'WayElement') -> float:
        return self.convert_meter_to_pixel(self._height)

    def get_distance(self: 'WayElement') -> float:
        if self._distance is None:
            return None
        return self.convert_meter_to_pixel(self._distance)
