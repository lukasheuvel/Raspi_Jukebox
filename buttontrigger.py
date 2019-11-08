import RPi.GPIO as GPIO
from datetime import datetime
import interface

print("kies een plaat\nde plaat die je kiest triggert bij iedere knopdruk")
selected_nr = input("locatie (e.g. V8):").strip()
print("locatie nummer {} geselecteerd.\n\nStarting Script\n".format(selected_nr))

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(4, GPIO.OUT, initial = GPIO.HIGH)

while True:
    if GPIO.input(24) == GPIO.HIGH:
        print("Sending signal for {} | {}".format(selected_nr, str(datetime.now)))
        signal = interface.encode(selected_nr)
        interface.send_gpio_signal(signal)
