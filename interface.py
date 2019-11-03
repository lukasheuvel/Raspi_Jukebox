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
    
    if GPIO.getmode() == None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT, initial=GPIO.LOW)
    
    correction = 0.005
    
    now = time()
    for headpeak in range(signalset[0]):
        GPIO.output(4, GPIO.HIGH)
        sleep(0.050 - correction)
        GPIO.output(4, GPIO.LOW)
        sleep(0.015 - correction)
    
    if signalset[2] == 815:
        GPIO.output(4, GPIO.HIGH)
        sleep(0.815 - correction)
        GPIO.output(4, GPIO.LOW)
        sleep(0.010 - correction)
    
    sleep(0.175-0.015 - correction)
        
    for tailpeak in range(signalset[1]):
        GPIO.output(4, GPIO.HIGH)
        sleep(0.050 - correction)
        GPIO.output(4, GPIO.LOW)
        sleep(0.015 - correction)
    
    GPIO.output(4, GPIO.LOW)


if __name__ == "__main__":
    pass
    # while True:
        # selection = input()
        # signal = encode(selection)
        # print_signal(signal)


