import random
import time

import config
from character import Bird, HandClick, Block
from game import UILoopContext, Label, Container
from simple_event import Events


class Scene(Container):
    GAME_AT_START_SCREEN = 1
    GAME_RUNNING = 2
    GAME_OVER = 3

    def __init__(self) -> None:
        super().__init__()
        # init properties
        self._game_mode = Scene.GAME_AT_START_SCREEN
        self._game_start_time = 0
        self._game_over_time = 0
        self._frames = 0
        self._score = 0

        self._blocks = []

        self._tips_label = Label()
        self._vendor_info_label = Label()
        self._bird = Bird()
        self._hand_click = HandClick()
        self._score_label = Label()
        self._final_score_label = Label()

        self.build_ui()
        self.show_start_screen()

    def build_ui(self):
        self.children.append(self._tips_label)
        self.children.append(self._vendor_info_label)
        self.children.append(self._bird)
        self.children.append(self._score_label)
        self.children.append(self._final_score_label)

    async def handle_events(self, context: UILoopContext):
        code = context.event_queue.poll_event_code(Events.TYPE_BUTTON)
        if code is not None:
            if code == Events.CODE_BUTTON_DOWN:
                await context.buzzer.beep()
                if self._game_mode == Scene.GAME_RUNNING:
                    self._bird.power_up()
                    pass
                elif self._game_mode == Scene.GAME_AT_START_SCREEN:
                    self.start_game()
                    pass
                elif self._game_mode == Scene.GAME_OVER:
                    if time.ticks_ms() - self._game_over_time > 1000:
                        self.show_start_screen()
                    pass

    def game_over(self):
        self._game_over_time = time.ticks_ms()
        self._bird.gravity_enabled = False
        for b in self._blocks:
            b.move_enabled = False
        self.set_tips_label_text("Game over")
        self._tips_label.visible = True
        self._game_mode = Scene.GAME_OVER
        self._score_label.visible = False

        self._final_score_label.visible = True
        self._final_score_label.text = f"Score: {self._score}"
        self._final_score_label.x = (config.SCREEN_WIDTH - self._final_score_label.width) // 2
        self._final_score_label.y = (config.SCREEN_HEIGHT - 8) // 2
        pass

    def clear_blocks(self):
        while len(self._blocks) > 0:
            b = self._blocks.pop()
            if b in self.children:
                self.children.remove(b)

    def check_bird_position(self):
        if self._game_mode == Scene.GAME_RUNNING:
            if self._bird.y > config.SCREEN_HEIGHT - self._bird.height:
                self.game_over()

    def count_score(self):
        if self._frames % 20 == 0:
            if self._game_mode == Scene.GAME_RUNNING:
                current_time = time.ticks_ms()
                self._score = (current_time - self._game_start_time) // 1000
                self._score_label.text = f"{self._score}s"

    def block_remove_myself_callback(self, block):
        self.children.remove(block)
        self._blocks.remove(block)
        pass

    def add_block(self, height: int, on_top=True):
        block = Block(8, height, self.block_remove_myself_callback)
        if not on_top:
            block.y = config.SCREEN_HEIGHT - height
        self.children.append(block)
        self._blocks.append(block)

    def add_blocks(self):
        if self._game_mode == Scene.GAME_RUNNING:
            if self._frames % 60 == 0:
                top_block_height = random.randrange(18)
                bottom_block_height = config.SCREEN_HEIGHT - 40 - top_block_height
                self.add_block(top_block_height, True)
                self.add_block(bottom_block_height, False)
            pass

    def count_frame(self):
        self.count_score()
        self.add_blocks()

        self._frames += 1
        if self._frames >= 7200:
            self._frames = 0

    def hit_test(self):
        if self._game_mode == Scene.GAME_RUNNING:
            for b in self._blocks:
                if b.hit_test_bird(self._bird):
                    self.game_over()
                    break

    async def enter_frame(self, context: UILoopContext):
        await self.handle_events(context)
        self.check_bird_position()
        self.count_frame()
        self.hit_test()

    def start_game(self):
        self.clear_blocks()
        self._game_start_time = time.ticks_ms()
        self._score_label.visible = True
        self._tips_label.visible = False
        if self._hand_click in self.children:
            self.children.remove(self._hand_click)
        self._vendor_info_label.visible = False
        self._bird.move_to_start_point()
        self._bird.gravity_enabled = True
        self._final_score_label.visible = False
        self._score = 0
        self._game_mode = Scene.GAME_RUNNING
        pass

    def set_tips_label_text(self, text: str):
        self._tips_label.text = text
        self._tips_label.y = 6
        self._tips_label.x = (config.SCREEN_WIDTH - self._tips_label.width) // 2

    def show_start_screen(self):
        self._game_mode = Scene.GAME_AT_START_SCREEN

        self.clear_blocks()

        self._score_label.visible = False
        self._final_score_label.visible = False

        self.set_tips_label_text("Flying bird")
        self._tips_label.visible = True

        if self._hand_click not in self.children:
            self.children.append(self._hand_click)

        self._vendor_info_label.visible = True
        self._vendor_info_label.text = "yunp.top"
        self._vendor_info_label.x = (config.SCREEN_WIDTH - self._vendor_info_label.width) // 2
        self._vendor_info_label.y = config.SCREEN_HEIGHT - 8 - 6

        self._bird.move_to_start_point()
        pass
