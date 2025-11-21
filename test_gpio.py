import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LED_PIN = 17
BUTTON_PIN = 27

try:
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    print("Testing LED...")
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(LED_PIN, GPIO.LOW)
    print("LED test done")
    
    print("Press button within 10 seconds...")
    for i in range(20):
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Button pressed!")
            break
        time.sleep(0.5)
    
finally:
    GPIO.cleanup()
    print("Cleanup done")