import RPi.GPIO as GPIO 
from time import sleep 
GPIO.setwarnings(False) 

GPIO.setmode(GPIO.BCM) 
GPIO.setup(17, GPIO.OUT) 
GPIO.output(17, True) 
sleep(2) 
GPIO.output(17, False)

#git clone https://github.com/matthieubron/Projet-E3

print("Je ne sais pas")