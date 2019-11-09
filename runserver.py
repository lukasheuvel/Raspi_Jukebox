#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Seeburg wallbox imitation

Developed in Python 3.7 for use on Raspberry Pi
"""


# Meta

__author__ = "Lukas van den Heuvel"
__copyright__ = "van den Heuvel"
__license__ = "GPL"
__version__ = "0.1"
__project__ = "Seeburg Wallbox Imitation"
__maintainer__ = "Lukas van den Heuvel"
__contact__ = "lukas.vandenheuvel@wur.nl"
__status__ = "Prototype"


# Imports
from datetime import datetime

from flask import Flask, request, render_template

import interface

# create web application
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def main():
    
    inputs = []
    with open('seeburg.txt') as f:
        for line in f:
            line = line.strip().replace('\t',' - ')
            inputs.append(line)
            
    if request.method == 'POST':
        with open('queuelog.txt', 'r+') as f:
            now = datetime.now()
            selected = request.form.get('Selection')
            
            logline = "{}\t{}".format(selected.replace(' - ','\t'),now)
            
            content = f.read()
            f.seek(0, 0)
            f.write(logline + '\n' + content)
            f.close()
    
            selected_nr = selected.split(' - ')[0]
    
            signal = interface.encode(selected_nr, 'wallomatic160')
    
            interface.send_gpio_signal(signal)
    
    with open('queuelog.txt','r') as f:
        queuelog = []
        for entry in f:
            entry = entry.strip().split('\t')
            entry[-1] = str(entry[-1])[0:-4]
            queuelog.append(entry)
    
    return render_template('main.html', InputList = inputs, QueueLog = queuelog)

    
if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000)
