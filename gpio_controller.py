import RPi.GPIO as GPIO
import time

class GPIOController:
    def __init__(self, led_pin, button_pin, button_callback):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        self.led_pin = led_pin
        self.button_pin = button_pin
        self.last_button_time = 0
        self.debounce = 0.3
        
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.output(self.led_pin, GPIO.LOW)
        
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_pin, GPIO.FALLING, 
                            callback=self._button_handler, bouncetime=300)
        
        self.callback = button_callback
    
    def _button_handler(self, channel):
        now = time.time()
        if now - self.last_button_time > self.debounce:
            self.last_button_time = now
            self.callback()
    
    def led_on(self):
        GPIO.output(self.led_pin, GPIO.HIGH)
    
    def led_off(self):
        GPIO.output(self.led_pin, GPIO.LOW)
    
    def cleanup(self):
        GPIO.cleanup()