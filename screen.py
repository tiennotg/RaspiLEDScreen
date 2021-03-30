'''
  screen.py
  
  Copyright 2020 Guilhem Tiennot
  
  A led screen for Raspberry Pi, using GPIO. Low-level GPIO manipulation.
  
  Dependencies: RPi.GPIO, math,
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

from GS_timing import delayMicroseconds, millis
from math import trunc
from RPi import GPIO

''' You'll probably have to change GPIO cols and rows, according
to your physical LED matrix ! '''

# outputs connected to half rows, starting from top left, to right bottom
ROW_GPIO = [7, 14, 1, 25, 12, 8, 16, 15, 20, 18, 21, 23, 26, 24]
# outputs connected to columns, starting from left to right
COL_GPIO = [2, 3, 4, 17, 27, 22, 10, 9, 11, 0, 5, 6, 13, 19]
# minimal delay while an half row is powered
SAFEGUARD_INTERVAL = 100 # in µs

# Constant for rolling text effect
ROLLING_INTERVAL = 200 # in ms

class CustomScreen():
	''' "size" is expected to be an array of two parameters : (width,height) of
	the screen, in pixels.'''
	def __init__(self, size):
		if not (isinstance(size, (tuple, list)) and len(size) == 2):
			raise TypeError('"Size" must be a tuple or a list with two elements.')
		if size[0] > 0 and size[1] > 0:
			self._width = size[0]
			self._height = size[1]
		else:
			raise ValueError("Dimensions must be positive integers.")
		self.clear()
		
		# We use BCM pinout for inputs/outputs.
		GPIO.setmode(GPIO.BCM)
		
		# Setup each pin in output mode, with low initial state.
		for n in ROW_GPIO:
			GPIO.setup(n, GPIO.OUT, initial=GPIO.LOW)
		for n in COL_GPIO:
			GPIO.setup(n, GPIO.OUT, initial=GPIO.LOW)

	def clear_pos(self):
		# define and set to zero the current half row pointer.
		self._y = 0
		
		# position of text roll
		self._offset = 0
		self._last_offset = None
	
	def clear(self):
		# Fills a matrix with False
		self._matrix = []
		self.clear_pos()
		for i in range(self._height): # rows
			self._matrix.append([])
			for j in range(self._width): # cols
				self._matrix[i].append(False)

	def clear_gpio(self):
		# Reset all of the GPIO to low state.
		for i in ROW_GPIO:
			GPIO.output(n, GPIO.LOW)
		for i in COL_GPIO:
			GPIO.output(n, GPIO.LOW)
	
	def update(self, matrix):
		self.clear_pos()
		# Row number must be the same as screen height. Col number can be equal or greather than screen width.
		if not (len(matrix) == self._height and len(matrix[0]) >= self._width):
			raise ValueError("Matrix size mismatchs with screen size.")
			
		# matrix in argument becomes the new current matrix.
		self._matrix = matrix
		
		# If matrix is too width, add a rolling effect
		if len(self._matrix[0]) > self._width:
			self._last_offset = millis()
    
	def refresh(self):
		# Offset, for rolling effect
		if self._last_offset and millis()-self._last_offset >= ROLLING_INTERVAL:
			self._offset = self._offset + 1
			self._last_offset = millis()
		
		for i in range(len(COL_GPIO)):
			''' Coordinates of one pixel in the matrix are :
				- row : self._y/2 (truncated) ; because _y is for half rows
				- column : (self._y modulo 2) * number of cols + i ; because if _y
					is odd, we are in a right half row, and we have to shift of
					the sizeh of an half row. '''
			p_y = trunc(self._y/2)
			p_x = ((self._y % 2) * len(COL_GPIO) + i + self._offset ) % len(self._matrix[0])
			if self._matrix[p_y][p_x]:
				GPIO.output(COL_GPIO[i], GPIO.HIGH)
			else:
				GPIO.output(COL_GPIO[i], GPIO.LOW)
		
		# power up the half row, wait, and power down
		GPIO.output(ROW_GPIO[self._y], GPIO.HIGH)
		delayMicroseconds(SAFEGUARD_INTERVAL)
		GPIO.output(ROW_GPIO[self._y], GPIO.LOW)
		
		# Next half row
		self._y = self._y+1
		if (self._y >= len(ROW_GPIO)):
			self._y = 0

	def __del__(self):
		self.clear_gpio()
		GPIO.cleanup()
