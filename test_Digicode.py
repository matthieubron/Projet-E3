import RPi.GPIO as GPIO
import time
from threading import Timer

ROW_PINS = [27, 22, 5, 6]
COL_PINS = [26, 23, 24, 25]

TARGET_CODE = "1234"
MAX_DIGITS = 4
TIMEOUT_SECONDS = 10

KEYPAD  = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"],
]


input_code = ""
timeout_timer = None



def reset_input():
    global input_code, timeout_timer
    input_code = ""
    print("Code réinitialisé.")
    if timeout_timer:
        timeout_timer.cancel()
        timeout_timer = None


def restart_timeout():
    global timeout_timer
    if timeout_timer:
        timeout_timer.cancel()
    timeout_timer = Timer(TIMEOUT_SECONDS, reset_input)
    timeout_timer.start()


def process_key(key):
    global input_code

    if key == "*":
        print("Annulation manuelle.")
        reset_input()
        return

    if key == "#":
        if len(input_code) == MAX_DIGITS:
            print(f"Code saisi : {input_code}")
            if input_code == TARGET_CODE:
                print("Code correct !")
                # Action ici (ouvrir porte ?)
            else:
                print("Code incorrect.")
        else:
            print("Code incomplet.")
        reset_input()
        return

    # Si c’est un chiffre (pas A, B, etc.)
    if key in "0123456789":
        if len(input_code) < MAX_DIGITS:
            input_code += key
            print(f"Code actuel : {input_code}")
            restart_timeout()
        else:
            print("Trop de chiffres, réinitialisation.")
            reset_input()



# Utilisation des numéros GPIO et pas physique car j'ai initialisé les variables
# comme ça
GPIO.setmode(GPIO.BCM)

#Ligne sont mises en sortie et initialisé à haut
for row in ROW_PINS:
    GPIO.setup(row, GPIO.OUT)
    GPIO.output(row, GPIO.HIGH)

for col in COL_PINS:
    GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Init à high


def scan_keypad():
    for row_num, row_pin in enumerate(ROW_PINS):
        GPIO.output(row_pin, GPIO.LOW)  # Active cette ligne

        for col_num, col_pin in enumerate(COL_PINS):
            if GPIO.input(col_pin) == GPIO.LOW:
                key = keypad[row_num][col_num]
                while GPIO.input(col_pin) == GPIO.LOW:
                    time.sleep(0.01)  # Attente relâchement
                return key

        GPIO.output(row_pin, GPIO.HIGH)  # Désactive la ligne

    return None

#Interuptions appelés quand une touche est appuyé
def key_pressed_callback(channel):
    key = scan_keypad()
    if key:
        print(f"Touche pressée : {key}")
        process_key(key)


# Attacher des interruptions aux colonnes
for col_pin in col_pins:
    GPIO.add_event_detect(col_pin, GPIO.FALLING, callback=key_pressed_callback, bouncetime=300)

try:
    print("Press a key (Ctrl+C to quit)")
    while True:
        time.sleep(0.1) #Pour laisser le programme en vie


except KeyboardInterrupt:
    print("Bye.")
    GPIO.cleanup()

