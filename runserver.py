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
import json

from flask import Flask, request, render_template

import interface

# create web application
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def main():
    select_row = ['1', '2', '3', '4', '5', '6', '7', '8']
    select_col = ['1', '2', '3', '4', '5']
    colnames = {'1': "All Time Favorites",
                '2': "50s",
                '3': "60s",
                '4': "70s",
                '5': "80s"}
    colours = {'1': ('orange','peachpuff'),
              '2': ('royalblue','skyblue'),
              '3': ('mediumseagreen','lightgreen'),
              '4': ('firebrick','white'),
              '5': ('mediumorchid','plum')}
    
    with open('seeburg.json', 'r') as f:
        selection_datastore = json.load(f)

    if request.method == 'POST':
        selected = request.form.get('Selection')
        
        signal = interface.encode(selected, 'wallomatic160')

        # interface.send_gpio_signal(signal)
        print(selected)
            
    return render_template('main.html', Datastore = selection_datastore,
                           RowCount = select_row, ColCount = select_col,
                           ColName = colnames, Colour = colours)

    
if __name__ == "__main__":
    # Run file manager on the excel file?
    app.run(host = '0.0.0.0', port = 5000)
