import framebuf
from framebuf import FrameBuffer

import config
from game import Bitmap, UILoopContext, DisplayObjectWithPosition, Geom


class Bird(DisplayObjectWithPosition):
    def __init__(self) -> None:
        super().__init__()

        self._width = 24
        self._height = 18
        self._frame_index = 0
        self._times = 0
        self._frames = [
            Bitmap(
                bytearray(
                    [0x0, 0x0, 0x0, 0x0, 0xc0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xff, 0x0, 0x0, 0x0, 0x0, 0xf0, 0xff, 0x0, 0xff,
                     0xcf, 0xff, 0xf, 0xc0, 0x3, 0xff, 0xff, 0x0, 0x3, 0xff, 0xf, 0xfc, 0x3, 0x0, 0x0, 0xf3, 0xfc, 0x3c,
                     0x0, 0x0, 0x0, 0xf3, 0x3c, 0xf0, 0x0, 0x0, 0x0, 0xfc, 0x3c, 0xc0, 0x0, 0x0, 0x0, 0x0, 0xfc, 0x30,
                     0x0, 0x0, 0x0, 0x0, 0x3, 0xf0, 0xc0, 0x0, 0x30, 0xc0, 0x0, 0xf0, 0xc0, 0x0, 0xfc, 0x3f, 0x0, 0xf0,
                     0xc0, 0xc0, 0xc3, 0x3, 0x0, 0xc0, 0xc3, 0xff, 0x0, 0x3, 0x0, 0xc0, 0xcf, 0xc, 0x0, 0xf, 0x0, 0x0,
                     0xcf, 0xfc, 0x33, 0xc, 0x0, 0x0, 0x3c, 0xf0, 0xcf, 0x30, 0x0, 0x0, 0x0, 0xf0, 0xff, 0xf3, 0x0, 0x0,
                     0x0, 0x0, 0xc0, 0x3c, 0x0]
                ), 24, 19
            ),
            Bitmap(
                bytearray(
                    [0x0, 0x0, 0x0, 0x0, 0xc0, 0x0, 0x0, 0x0, 0x0, 0xc0, 0xff, 0x0, 0xc0, 0x0, 0x0, 0xfc, 0xf3, 0x0,
                     0xff, 0xcf, 0xff, 0xf, 0xf0, 0x3, 0xff, 0x3f, 0x0, 0x0, 0xff, 0xf, 0xfc, 0x3, 0x0, 0x0, 0xf3, 0xfc,
                     0x3c, 0x0, 0x0, 0x0, 0xff, 0x3c, 0xf0, 0x0, 0x0, 0x0, 0x3c, 0x3c, 0xf0, 0x0, 0x0, 0x0, 0x0, 0xff,
                     0xf0, 0x0, 0x0, 0x0, 0x0, 0x3, 0xf0, 0xc0, 0x0, 0x3c, 0xf0, 0x0, 0xf0, 0xc0, 0x0, 0xcc, 0x3f, 0x0,
                     0xc0, 0xc3, 0xff, 0x3, 0xf, 0x0, 0x0, 0xff, 0xfc, 0xff, 0xff, 0x0]
                ), 24, 14
            )
        ]

        self._gravity_enabled = False
        self.move_to_start_point()
        self._speed_y: float = 0.0
        self._gravity: float = 0.05

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    async def enter_frame(self, context: UILoopContext):
        if self.gravity_enabled:
            self._speed_y += self._gravity
            self.y = int(self.y + self._speed_y)
            if self.y < 0:
                self.y = 0

    def power_up(self):
        self._speed_y = -0.5

    @property
    def gravity_enabled(self):
        return self._gravity_enabled

    @gravity_enabled.setter
    def gravity_enabled(self, v):
        self._gravity_enabled = v

    def move_to_start_point(self):
        self.x = config.SCREEN_WIDTH // 2 - self.width - 6
        self.y = (config.SCREEN_HEIGHT - self.height) // 2
        self._speed_y = 0.0

    async def draw(self, context: UILoopContext):
        frame = self._frames[self._frame_index]
        frame.x = self.x
        frame.y = self.y
        await frame._internal_draw(context)
        if self._times % 10 == 0:
            self._frame_index += 1
            if self._frame_index >= len(self._frames):
                self._frame_index = 0
        self._times += 1
        if self._times >= 7200:
            self._times = 0
        pass


class HandClick(Bitmap):
    def __init__(self) -> None:
        super().__init__(bytearray(
            [0x0, 0x0, 0x0, 0x0, 0x3c, 0x3c, 0x3c, 0x0, 0x30, 0xfc, 0x3c, 0x0, 0x0, 0xcf, 0x0, 0x0, 0xc, 0xcf, 0xf0,
             0x0, 0x3f, 0xcf, 0xf, 0x0, 0x0, 0xcf, 0xff, 0x3, 0x0, 0xcf, 0xfc, 0x3f, 0xfc, 0xcf, 0x3c, 0xff, 0xc, 0xcf,
             0x3c, 0xf3, 0x3c, 0x0, 0x0, 0xf0, 0x30, 0x0, 0x0, 0xf0, 0xf0, 0x0, 0x0, 0xf0, 0xc0, 0x3, 0x0, 0x30, 0xc0,
             0x3, 0x0, 0x3c, 0x0, 0xf, 0x0, 0xf, 0x0, 0xfc, 0xff, 0x3, 0x0, 0xc0, 0xff, 0x0]),
            16, 18
        )
        self.x = config.SCREEN_WIDTH // 2 + 6
        self.y = (config.SCREEN_HEIGHT - self._height) // 2
        self._frames = 0

    async def enter_frame(self, context: UILoopContext):
        if self._frames % 20 == 0:
            self.visible = not self.visible
        self._frames += 1
        if self._frames >= 2000:
            self._frames = 0


class Block(DisplayObjectWithPosition):

    def __init__(self, width: int, height: int, remove_myself_callback) -> None:
        super().__init__()
        self._remove_myself_callback = remove_myself_callback
        self.x = config.SCREEN_WIDTH
        self._width = width
        self._height = height
        self._move_enabled = True

    async def draw(self, context: UILoopContext):
        context.oled.fill_rect(self.x, self.y, self.width, self.height, 1)

    async def enter_frame(self, context: UILoopContext):
        if self.move_enabled:
            self.x -= 1
            if self.x < -self.width:
                if self._remove_myself_callback:
                    self._remove_myself_callback(self)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def move_enabled(self):
        return self._move_enabled

    @move_enabled.setter
    def move_enabled(self, v):
        self._move_enabled = v

    def hit_test_bird(self, bird: Bird):
        return Geom.rect_hit_test_rect(
            (self.x, self.y, self.width, self.height),
            (bird.x, bird.y, bird.width, bird.height)
        )
