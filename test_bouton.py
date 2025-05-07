from gpiozero import Button
from led import allumer_led

# Ajout d'un temps de rebond de 100ms (bounce_time=0.1)
bouton = Button(18, pull_up=True, bounce_time=0.1)

while True:
    bouton.wait_for_press()
    allumer_led()