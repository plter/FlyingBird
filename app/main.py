import machine
import time
import uasyncio

import config
from buzzer import Buzzer
from game import UILoopContext
from scene import Scene
from simple_event import Events
from ssd1306 import SSD1306_I2C


async def ui_loop():
    # config i2c and oled
    i2c = machine.I2C(0, freq=1200000)
    oled = SSD1306_I2C(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, i2c)

    # config button
    button = machine.Pin(config.BUTTON_PIN, machine.Pin.IN)

    # config buzzer
    buzzer = Buzzer(config.BUZZER_PIN)

    # init properties
    recorded_last_time = 0
    context = UILoopContext(oled, buzzer)
    game_scene = Scene()
    fps = 0
    while True:
        context.event_queue.push_event_code(config.BUTTON_PIN, button.value(), Events.TYPE_BUTTON)
        # clear background
        oled.fill(0)
        context.current_fps = fps
        await game_scene._internal_draw(context)

        # Compute fps
        current_time = time.ticks_ms()
        if recorded_last_time != 0:
            frame_time = current_time - recorded_last_time
            fps = 1000 / frame_time
            if config.SHOW_FPS:
                oled.text(f"fps: {int(fps)}", 0, 56)
        recorded_last_time = current_time
        oled.show()
        await uasyncio.sleep_ms(1)


async def main():
    # config cpu freq
    machine.freq(240000000)

    await ui_loop()


if __name__ == '__main__':
    uasyncio.run(main())
