import json
from time import sleep
import RPi.GPIO as GPIO

def encode(pos, type):

    letter = pos[0]
    number = pos[1:]
    
    if type == 'wallomatic100':
        lettercode = {'A':(1,'L'),
                     'B':(1,'R'),
                     'C':(2,'L'),
                     'D':(2,'R'),
                     'E':(3,'L'),
                     'F':(3,'R'),
                     'G':(4,'L'),
                     'H':(4,'R'),
                     'J':(5,'L'),
                     'K':(5,'R'),}

        # Wall-o-matic 100 models start with pulses for the number, with one
        # pulse per number. Here we refer to it as the headsignal.
        headsignal = int(number)
        
        # If the plate is on the left (A) side, there's a long (815ms) high.
        # If the plate is on the right (B) side, the head signal is extended
        # by 11 pulses.
        side = lettercode[letter][1]
        if  side == 'R':
            headsignal += 11
            gap = ('shortlow')
        else:
            gap = ('longhigh', 'shortlow')
        

        # Wall-o-matic 100 models end with the letter code. A and B (same plate
        # ) share the same number here, but with a different gap signal.
        tailsignal = lettercode[letter][0]
    
    if type == 'wallomatic160':
        letterorder = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K",
                       "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V"]
        
        # Wall-o-matic 160 models fire n pulses for the nth letter in the order
        # +1 to compensate for index 1 being 0 in python.
        headsignal = letterorder.index(letter) + 1
        
        # Letter and number codes are seperated by a low signal of ~120ms
        gap = ('longhigh','shortlow')
        
        # Wall-o-matic 160 models fire pulses equal to the second number
        tailsignal = int(number)
        
    return (headsignal, tailsignal, gap)
    
def print_signal(signalset):
    print("\n\n")
    print(" THIS FEATURE WAS USED FOR TESTING AND HAS BEEN REMOVED")
    print("the goal is to eventually output the waveform as graph with pyplot")
    print("\n\n")

    
def send_gpio_signal(signalset):

    relay_high = GPIO.LOW
    relay_low = GPIO.HIGH
    
    with open("pulsesettings.json",'r') as f:
        pulse = json.load(f)
    
    
    
    # Set up GPIO pins
    if GPIO.getmode() == None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.OUT, initial=relay_low)
    
    
    # Head waveform (ends on high for easy gap handling)
    for headpeak in range(signalset[0]):
        GPIO.output(4, relay_low)
        sleep(pulse['low'] - pulse['correction'])
        GPIO.output(4, relay_high)
        sleep(pulse['high'] - pulse['correction'])
    
    
    # Gap waveform
    for gaptype in signalset[2]:
    
        if gaptype == 'longhigh':
            # Quick low before the gap
            GPIO.output(4, relay_low)
            sleep(pulse['low'] - pulse['correction'])
            # Long high gap
            GPIO.output(4, relay_high)
            sleep(pulse['long_wait'] - pulse['correction'])

            # IMPORTANT: This does not go back to low, as it is generally
            # followed by a shortlow. 
            
        if gaptype == 'shortlow':
            # Short wait on a low signal
            GPIO.output(4, relay_low)
            sleep(pulse['short_wait'] - pulse['correction'])
    
    
    # Tail waveform (starts on high for easy gap handling)
    for tailpeak in range(signalset[1]):
        GPIO.output(4, relay_high)
        sleep(pulse['high'] - pulse['correction'])
        GPIO.output(4, relay_low)
        sleep(pulse['low'] - pulse['correction'])
    
    # Return back to low
    GPIO.output(4, relay_low)


if __name__ == "__main__":
    pass
    # while True:
        # selection = input()
        # signal = encode(selection)
        # print_signal(signal)


