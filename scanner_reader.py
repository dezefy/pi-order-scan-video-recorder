from evdev import InputDevice, categorize, ecodes

SCANCODES = {
    2: '1', 3: '2', 4: '3', 5: '4', 6: '5', 7: '6', 8: '7', 9: '8', 10: '9', 11: '0',
    12: '-', 16: 'A', 17: 'W', 18: 'E', 19: 'R', 20: 'T', 21: 'Y', 22: 'U', 23: 'I',
    24: 'O', 25: 'P', 30: 'A', 31: 'S', 32: 'D', 33: 'F', 34: 'G', 35: 'H', 36: 'J',
    37: 'K', 38: 'L', 44: 'Z', 45: 'X', 46: 'C', 47: 'V', 48: 'B', 49: 'N', 50: 'M'
}

class ScannerReader:
    def __init__(self, device_path):
        self.device = InputDevice(device_path)
        self.device.grab()
        self.buffer = []
    
    def read_codes(self, callback):
        for event in self.device.read_loop():
            if event.type == ecodes.EV_KEY:
                data = categorize(event)
                if data.keystate == 1:
                    if data.scancode == 28:
                        code = ''.join(self.buffer)
                        self.buffer = []
                        if code:
                            callback(code)
                    elif data.scancode in SCANCODES:
                        self.buffer.append(SCANCODES[data.scancode])