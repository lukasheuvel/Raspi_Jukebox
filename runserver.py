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
import json

from flask import Flask, request, render_template

import interface

# create web application
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def main():
    select_row = ['0', '1', '2', '3', '4', '5', '6', '7']
    select_col = ['0', '1', '2', '3', '4']
    colnames = {'0': "All Time Favorites",
                '1': "50s",
                '2': "60s",
                '3': "70s",
                '4': "80s"}
    colours = {'0': ('orange','peachpuff'),
              '1': ('royalblue','skyblue'),
              '2': ('mediumseagreen','lightgreen'),
              '3': ('firebrick','white'),
              '4': ('mediumorchid','plum')}
    
    with open('seeburg.json', 'r') as f:
        selection_datastore = json.load(f)

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
            
    return render_template('main.html', Datastore = selection_datastore,
                           RowCount = select_row, ColCount = select_col,
                           ColName = colnames, Colour = colours)

    
if __name__ == "__main__":
    # Run file manager on the excel file?
    app.run(host = '0.0.0.0', port = 5000)
