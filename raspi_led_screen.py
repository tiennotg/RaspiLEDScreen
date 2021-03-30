'''
  raspi_led_screen.py
  
  Copyright 2020 Guilhem Tiennot
  
  A led screen for Raspberry Pi, using GPIO. Main program.
  (Introduced in this video:
	https://peertube.tiennot.net/videos/watch/4a3d1c6c-4e90-4751-811d-f6d08cab509d)
  
  Usage:
    - launch the program, without any arguments
    - all new text line is displayed on the screen
    - if it's an image file name, displays it (black = light on,
    otherwise light off)
  
  Dependencies: os, string, sys, skimage, threading, RPi.GPIO, math,
		GS_timing (https://github.com/ElectricRCAircraftGuy/eRCaGuy_PyTime)
  
  This file is part of RaspiLEDScreen.
  
  RaspiLEDScreen is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  RaspiLEDScreen is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  
  You should have received a copy of the GNU General Public License
  along with RaspiLEDScreen.  If not, see <https://www.gnu.org/licenses/>.
'''

#!/usr/bin/python3

from matrix import MatrixScreen
from os.path import isfile
import string
from sys import stdin

ALLOWED_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,'°\"?()[]+-!:"

def led_print(screen, text):
	# if there is a file named like text, then print it
	# else just print the text
	if isfile(text):
		screen.draw(text)
	else:
		allowed_set = set(ALLOWED_CHARS)
		text_set = set(text)
		if text_set.issubset(allowed_set):
			screen.print(text.upper())

s = MatrixScreen((28,7))
for line in stdin:
	led_print(s,line.rstrip())
