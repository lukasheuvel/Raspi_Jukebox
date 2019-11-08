import json
import RPi.GPIO as GPIO
from datetime import datetime
import interface

def yes_or_no(question):
    answer = input(question + "(y/n): ").lower().strip()
    print("")
    while not(answer == "y" or answer == "yes" or \
    answer == "n" or answer == "no"):
        print("Input yes/y or no/n")
        answer = input(question + "(y/n):").lower().strip()
        print("")
    if answer[0] == "y":
        return True
    else:
        return False

print("kies een plaat\nde plaat die je kiest triggert bij iedere knopdruk")
selected_nr = input("locatie (e.g. V8):").strip().upper()
print("locatie nummer {} geselecteerd.\n".format(selected_nr))

if yes_or_no("Wil je verder nog settings aanpassen"):

    with open("pulsesettings.json",'r') as f:
        pulsedict = json.load(f)
    
    descriptions = {
                   "high":"Hoe lang de HIGH pulse duurt (ms)",
                   "low":"Hoe lang de LOW pulse duurt (ms)",
                   "long_wait":"Hoe lang de HIGH pulse als je een nummer pakt op de linker kant van een plaat (ms)",
                   "short_wait":"Hoe lang de LOW pulse is tussen signalen naar de letter en nummer stepper (ms)",
                   "correction":"Correctie. bijv. 5 invullen verkort ALLE pulses met 5ms (ms)"
                   }
    
    newdict = pulsedict.copy()
    
    for key in pulsedict.keys():
        if key != 'default':
            print("\n{} aanpassen:".format(key))
            print(descriptions[key])
            print("\t{} is nu {}".format(key, pulsedict[key]*1000))
            print("\t{} is default {}".format(key, pulsedict['default'][key]*1000))
        
            newvalue = input("Nieuwe waarde (puur het getal)(ms):")
            if newvalue == "":
                newvalue = pulsedict['default'][key]
            else:
                newvalue = float(newvalue.strip())/1000.0
        
            newdict[key]=newvalue
            print("\n\t{} is nu {}ms".format(key, newvalue*1000))
    
    with open("pulsesettings.json",'w') as f:
        json.dump(newdict, f)

print("\nStarting Script\n")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(4, GPIO.OUT, initial = GPIO.HIGH)

while True:
    if GPIO.input(24) == GPIO.HIGH:
        print("Sending signal for {} | {}".format(selected_nr, str(datetime.now)))
        signal = interface.encode(selected_nr)
        interface.send_gpio_signal(signal)
