# RaspiLEDScreen
Source code of the program showed here: https://peertube.tiennot.net/videos/watch/4a3d1c6c-4e90-4751-811d-f6d08cab509d

# Installation
  - Install dependancies skimage and RPi: `apt-get install python3-skimage python3-rpi.gpio`
  - Start the program: `python3 raspi_led_screen.py`
  - Each line of the standard input is printed on the screen. If the text is a valid image file name, it tries to print it (note: height of the image must be the same as screen height, black pixel means LED on, and other color means LED off).

# About the LED screen conception
By default, this program is intended to drive a simple LED matrix of 7 rows by 28 columns. As the Raspberry Pi only have 28 available GPIO, I made two groups of 14 columns: the columns from 1 to 14 first, and then the columns from 15 to 28. The two groups share the same pins. It means that column 1 and 15 are wired together, also 2 and 16, etc.

But to control them separately, I choosed to split each line in two sublines. Line 1 is made of half-lines 1 and 2, line 2 made of half-lines 3 and 4, etc. And I turn half-lines on each in sequence. Here is the default GPIO numbers (BCM numbering; you can change them in `screen.py`):
  - columns: `2 3 4 17 27 22 10 9 11 0 5 6 13 19`
  - half-rows (grouped by lines): `(7 14) (1 25) (12 8) (16 15) (20 18) (21 23) (26 24)`
