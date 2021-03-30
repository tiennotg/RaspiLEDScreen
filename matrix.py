'''
  matrix.py
  
  Copyright 2020 Guilhem Tiennot
  
  A led screen for Raspberry Pi, using GPIO. Data management:
    - text conversion to a displayable matrix
    - image importation
  
  Dependencies: os, skimage, threading
  
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

from screen import CustomScreen
import os
from skimage import io
import threading

# Path to the directory with char images.
CHAR_IMG_DIR = "./chars"

class ImageSizeError(Exception):
	def __init__(self, message):
		super(ImageSizeError, self).__init__(message)

class MatrixScreen(CustomScreen):
	def __init__(self, size):
		super(MatrixScreen, self).__init__(size)
		self._chars = {}
		self.load_from_dir(CHAR_IMG_DIR)
		# Main loop is in a thread
		thread = threading.Thread(target=self._loop)
		thread.start()

	def _loop(self):
		while True:
			self.refresh()
	
	# Load a char from a file, and put its matrix in _chars array
	# with its filename as key.
	def load_from_file(self, filename):
		key = os.path.splitext(os.path.basename(filename))[0]
		self._chars[key] = self.matrix_from_file(filename)
	
	# Load all char images from a directory to the _chars array.
	def load_from_dir(self, dirname):
		for f in os.listdir(dirname):
			self.load_from_file(os.path.join(dirname,f))
	
	# Build a matrix to display on the screen from a text,
	# with the _chars array, containing representation of each char
	# Warning: input must be filtered, otherwise an exception will raise
	# when encountering an unexpected char.
	def matrix_from_string(self, string):
		m = []
		# init a sub array for each row
		for i in range(self._height):
			m.append([]);
		for c in string:
			for i in range(len(self._chars[c])):
				for pix in self._chars[c][i]:
					m[i].append(pix)
		return m
	
	# Convert an image into a displayable matrix. Black pixels are for
	# lighting LEDs, the other colors switch them off.
	def matrix_from_file(self, filename):
		img = io.imread(filename)
		if not img.shape[0] == self._height:
			raise ImageSizeError("Image height must be equal to screen height.")
		m = []
		for j in range(len(img)):
			m.append([])
			for i in range(len(img[j])):
				if img[j][i].all(0):
					m[j].append(False)
				else:
					m[j].append(True)
		return m
	
	# If matrix width is smaller than screen width, fill it with zeros
	# until it reaches screen widt.
	def matrix_fill_screen_width(self, m):
		d = self._width-len(m[0])
		if d > 0:
			for j in range(len(m)):
				for i in range(d):
					m[j].append(False)
		return m
	
	# Debug function, to print the generated matrix on stdout.
	def _debug_print_matrix(m):
		for row in m:
			row_p=""
			for pix in row:
				if pix:
					row_p = row_p+"*"
				else:
					row_p = row_p+"_"
			print(row_p)
	
	# Print "text" on the screen.
	# Bug: doesn't work yet with UTF-8 chars like ❤️ or ☺️...
	def print(self, text):
		m = self.matrix_fill_screen_width(self.matrix_from_string(text))
		self.update(m)
		MatrixScreen._debug_print_matrix(m)
	
	# Print a picture on the screen. Black pixels are for lighting LEDs,
	# other colors switch them off.
	def draw(self, filename):
		m = self.matrix_fill_screen_width(self.matrix_from_file(filename))
		self.update(m)
		MatrixScreen._debug_print_matrix(m)

if __name__ == '__main__':
	mb = MatrixScreen((28,7))
	mb.print("GUI'M LA SCIENCE")
