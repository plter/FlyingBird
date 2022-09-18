import framebuf
from framebuf import FrameBuffer

from buzzer import Buzzer
from simple_event import EventQueue
from ssd1306 import SSD1306_I2C


class UILoopContext:

    def __init__(self, oled: SSD1306_I2C, buzzer: Buzzer) -> None:
        super().__init__()
        self._oled = oled
        self._current_fps = 0
        self._buzzer = buzzer
        self._event_queue = EventQueue()

    @property
    def oled(self) -> SSD1306_I2C:
        return self._oled

    @property
    def current_fps(self):
        return self._current_fps

    @current_fps.setter
    def current_fps(self, v):
        self._current_fps = v

    @property
    def event_queue(self):
        return self._event_queue

    @property
    def buzzer(self):
        return self._buzzer


class Geom:
    @staticmethod
    def point_hit_test_rect(point, rect):
        """
        :param point: (x,y)
        :param rect: (x,y,w,h)
        :return:
        """
        return rect[0] < point[0] < rect[0] + rect[2] and rect[1] < point[1] < rect[1] + rect[3]

    @staticmethod
    def rect_hit_test_rect(rect1, rect2):
        """
        :param rect1: (x,y,w,h)
        :param rect2: (x,y,w,h)
        :return:
        """
        return Geom.point_hit_test_rect((rect1[0], rect1[1]), rect2) or \
               Geom.point_hit_test_rect((rect1[0] + rect1[2], rect1[1]), rect2) or \
               Geom.point_hit_test_rect((rect1[0], rect1[1] + rect1[3]), rect2) or \
               Geom.point_hit_test_rect((rect1[0] + rect1[2], rect1[1] + rect1[3]), rect2) or \
               Geom.point_hit_test_rect((rect2[0], rect2[1]), rect1) or \
               Geom.point_hit_test_rect((rect2[0] + rect2[2], rect2[1]), rect1) or \
               Geom.point_hit_test_rect((rect2[0], rect2[1] + rect2[3]), rect1) or \
               Geom.point_hit_test_rect((rect2[0] + rect2[2], rect2[1] + rect2[3]), rect1)


class Display:

    def __init__(self) -> None:
        super().__init__()
        self._visible = True

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, v):
        self._visible = v

    async def draw(self, context: UILoopContext):
        raise NotImplementedError()

    async def enter_frame(self, context: UILoopContext):
        pass

    async def _internal_draw(self, context: UILoopContext):
        await self.enter_frame(context)
        if self.visible:
            await self.draw(context)


class DisplayObjectWithPosition(Display):

    def __init__(self) -> None:
        super().__init__()
        self._x: int = 0
        self._y: int = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, v):
        self._x = v

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, v):
        self._y = v

    async def draw(self, context: UILoopContext):
        pass


class Label(DisplayObjectWithPosition):

    def __init__(self, text: str = "") -> None:
        super().__init__()
        self._text = text
        self._width = 0

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, v):
        self._text = v
        self._width = len(self.text) * 8

    @property
    def width(self):
        return self._width

    async def draw(self, context: UILoopContext):
        if not self.visible:
            return
        context.oled.text(self.text, self.x, self.y)


class Container(Display):

    def __init__(self) -> None:
        super().__init__()
        self._children = []

    @property
    def children(self):
        return self._children

    async def draw(self, context: UILoopContext):
        for c in self.children:
            await c._internal_draw(context)


class Bitmap(DisplayObjectWithPosition):

    def __init__(self, pixels, width, height) -> None:
        """
        Create with GS2_HMSB format
        :param pixels:
        :param width:
        :param height:
        """
        super().__init__()
        self._buffer = FrameBuffer(pixels, width, height, framebuf.GS2_HMSB)
        self._width = width
        self._height = height

    async def draw(self, context: UILoopContext):
        context.oled.blit(self._buffer, self.x, self.y)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height
