import json
from time import sleep, time
import RPi.GPIO as GPIO

def encode(pos):
    lettercode = {'A':(1,'-'),
                 'B':(1,'+'),
                 'C':(2,'-'),
                 'D':(2,'+'),
                 'E':(3,'-'),
                 'F':(3,'+'),
                 'G':(4,'-'),
                 'H':(4,'+'),
                 'J':(5,'-'),
                 'K':(5,'+'),
                 'L':(6,'-'),
                 'M':(6,'+'),
                 'N':(7,'-'),
                 'P':(7,'+'),
                 'Q':(8,'-'),
                 'R':(8,'+'),
                 'S':(1,'-'),
                 'T':(1,'+'),
                 'U':(1,'-'),
                 'V':(1,'+')}

    letter = pos[0]
    number = pos[1:]
    
    headsignal = int(number)
    tailsignal = lettercode[letter][0]
    
    side = lettercode[letter][1]
    if  side == '+':
        headsignal += 11
        gap = 175
    else:
        gap = 815
    
    return (headsignal, tailsignal, gap)
    
def print_signal(signalset):
    outline = "__________" #starting null
    
    for headpeak in range(signalset[0]):
        outline += '¯_' #1 wave
    
    if signalset[2] == 815:
        outline += '¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯' #815ms high
    
    outline += '____' #175ms low
        
    for tailpeak in range(signalset[1]):
        outline += '¯_' #1 wave
    
    outline += '_________' #closing null
    
    print(outline)
    
def send_gpio_signal(signalset):

    relay_high = GPIO.LOW
    relay_low = GPIO.HIGH
    
    with open("pulsesettings.json",'r') as f:
        pulse = json.load(f)
    
    if GPIO.getmode() == None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.OUT, initial=relay_low)
    
    now = time()
    
    # Cycle letter stepper
    for headpeak in range(signalset[0]):
        GPIO.output(4, relay_high)
        sleep(pulse['high'] - pulse['correction'])
        GPIO.output(4, relay_low)
        sleep(pulse['low'] - pulse['correction'])
    
    if signalset[2] == 815:
        # Keep the long high wait
        GPIO.output(4, relay_high)
        sleep(pulse['long_wait'] - pulse['correction'])
        
        # The short wait (below) is shortened by 1 low pulse to compensate for
        # any extension caused by the last low of the loop above. We therefore
        # also imitate that here.
        GPIO.output(4, relay_low)
        sleep(pulse['low'] - pulse['correction'])
    
    # Short wait on a low signal, for switch between letter and number steppers
    # With compensation for any extension cause by the last low of the loops.
    sleep(pulse['short_wait'] - pulse['low'] - pulse['correction'])
    
    # Cycle number stepper
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


