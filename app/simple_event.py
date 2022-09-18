class Events:
    TYPE_BUTTON = "button"
    CODE_BUTTON_DOWN = 1
    CODE_BUTTON_UP = 0


class Device:
    __devices = {}

    @staticmethod
    def get_device(device_id: int):
        if device_id in Device.__devices:
            return Device.__devices[device_id]
        else:
            d = Device(device_id)
            Device.__devices[device_id] = d
            return d

    def __init__(self, device_id) -> None:
        super().__init__()
        self._device_id = device_id
        self._last_event_type = ""
        self._last_event_code = -1

        # Dict[str, list]
        self._events = {}

    @property
    def device_id(self):
        return self._device_id

    @property
    def last_event_code(self) -> int:
        return self._last_event_code

    @last_event_code.setter
    def last_event_code(self, v):
        self._last_event_code = v

    @property
    def last_event_type(self) -> str:
        return self._last_event_type

    @last_event_type.setter
    def last_event_type(self, v):
        self._last_event_type = v

    def push_event_state(self, code, event_type):
        if event_type in self._events:
            codes = self._events[event_type]
        else:
            codes = []
            self._events[event_type] = codes
        if self.last_event_code != code:
            codes.append(code)
            self.last_event_code = code

    def poll_event_code(self, event_type: str) -> int:
        if event_type in self._events:
            codes: list = self._events[event_type]
            if len(codes) > 0:
                return codes.pop(0)
        return None


class EventQueue:

    def __init__(self) -> None:
        super().__init__()
        # Dict[str, Dict[int, Device]]
        self._event_type_to_devices_map = {}

    def push_event_code(self, device_id: int, code: int, event_type: str):
        device = Device.get_device(device_id)
        if event_type in self._event_type_to_devices_map:
            devices = self._event_type_to_devices_map[event_type]
        else:
            devices = {}
            self._event_type_to_devices_map[event_type] = devices
        if device_id not in devices:
            devices[device_id] = device
        device.push_event_state(code, event_type)

    def poll_event_code(self, event_type: str) -> int:
        if event_type in self._event_type_to_devices_map:
            for device_id, device in self._event_type_to_devices_map[event_type].items():
                e = device.poll_event_code(event_type)
                if e is not None:
                    return e
        return None
