import uasyncio
from machine import Pin, PWM


class Buzzer:
    def __init__(self, pin: int) -> None:
        super().__init__()
        self._pin = Pin(pin, Pin.OUT)
        self._pwm = PWM(self._pin, duty=0, freq=523)

    async def _beep_task(self):
        self._pwm.duty(512)
        await uasyncio.sleep_ms(80)
        self._pwm.duty(0)
        self._pwm.init()
        pass

    async def beep(self):
        uasyncio.create_task(self._beep_task())
