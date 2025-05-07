from gpiozero import LED
from time import sleep

def allumer_led():
    led = LED(23)  # GPIO23 (pin 16)
    led.on()
    sleep(10)
    led.off()