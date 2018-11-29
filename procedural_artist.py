import sys
from PIL import Image
import threading
import random

MAX_THREADS = 500
counter_lock    = threading.Lock()

# ARTISTS data structure:
# [] [] [] [] [] [] [] [] -- horizontally is a list of artists
# [] [] [] [] [] [] [] [] -- vertically is a list of owned pixels
# [] [] [] [] [] [] [] []
#
ARTISTS = []

# A parallel array to ARTISTS (horizontally) which contains the color
# of each artist
ARTISTCOLORS = []
SHOW = False;
COUNTER = 0;
SHOWSTEPS = 500;

def parseInputs(input):
	# Parse inputs and exit with error if necessary
	parsed = []

	if(len(input) != 5):
		sys.exit("Incorrect number of input parameters")

	num_threads = int(input[2])
	if(num_threads > MAX_THREADS):
		sys.exit("Exceeded thread count limit")

	num_steps = int(input[4])

	parsed.append(num_threads)
	parsed.append(num_steps)
	return parsed

def startingPositionClaimed(x, y):
	# loop through the ARTISTS array and check to make sure the first index (starting
	# position for each artist) is not equal to the position specified by the input
	# parameters x and y
	for artist in ARTISTS:
		if((artist[0]["x"] == x) and (artist[0]["y"] == y)):
			return True
	return False

def initializeArtistPostitions(numArtists):
	# Randomly generate starting positions on a 512x512 image
	x = 512
	y = 512
	for i in range(0, numArtists):
		# get random coordinates
		x = random.randint(0, 511)
		y = random.randint(0, 511)
		while(startingPositionClaimed(x, y)):
			# keep generating new positions until we find one that isn't claimed
			x = random.randint(0, 511)
			y = random.randint(0, 511)
		# create a list of coordinate objects (the list of pixels that will be 
		# colored by this artist), add starting position, and append 
		artist = [{"x": x, "y": y}]
		ARTISTS.append(artist)

def colorClaimed(r, g, b):
	# Check to see if the color specified by r, g, b, is already claimed by 
	# a different artist
	for artist in ARTISTCOLORS:
		if((artist["r"] == r) and (artist["g"] == g) and (artist["b"] == b)):
			return True
	return False

def initializeArtistColors(numArtists):
	# Randomly generate unique colors for each artist
	for x in range(0, numArtists):
		r = random.randint(0, 255)
		g = random.randint(0, 255)
		b = random.randint(0, 255)
		while(colorClaimed(r, g, b)):
			r = random.randint(0, 255)
			g = random.randint(0, 255)
			b = random.randint(0, 255)
		ARTISTCOLORS.append({"r": r, "g": g, "b": b})

def createPicture():
	# create a blank white canvas
	picture = Image.new('RGB', (512, 512), color = (255, 255, 255))
	return picture

def invalidPixel(x, y, PIX_MAP, colorTuple):
	# This function checks to make sure that the proposed coordinate location is
	# both in the valid range for the canvas (We don't want artists painting on
	# the wall) and that the proposed pixel is not already painted
	if(x == 512):
		return True
	if(y == 512):
		return True
	if(x == -1):
		return True
	if(y == -1):
		return True
	if((PIX_MAP[x, y] != (255, 255, 255)) and (PIX_MAP[x, y] != colorTuple)):
		# print("COLLISION")
		# print(colorTuple)
		# print(PIX_MAP[x, y])
		# print
		return True
	return False

def paint(artistIndex, numSteps, PIX_MAP, picture):
	# This function acts as an artist. It starts at the predefined starting location,
	# paints this pixel, randomly chooses a new direction (up, down, left, right), if the
	# pixel at the new location is valid (invalidPixel function) it paints that pixel
	# and repeats. If it is not a valid pixel, then it randomly chooses one of the pixels
	# that it has already painted and it repeats. 

	# get the starting position
	currentPosition = ARTISTS[artistIndex][0]
	# get the color
	color = ARTISTCOLORS[artistIndex]
	colorTuple = (color["r"], color["g"], color["b"])
	global SHOW

	# loop for each step (defined on input)
	for i in range(0, numSteps):
		counter_lock.acquire()
		if(SHOW):
			global COUNTER
			if((i%SHOWSTEPS == 0) and (COUNTER < i/SHOWSTEPS)):
				picture.show()
				COUNTER = i/SHOWSTEPS;
		# paint the current pixel
		x = currentPosition["x"]
		y = currentPosition["y"]
		PIX_MAP[x, y] = colorTuple

		# randomly choose a new direction to go
		direction = random.randint(0, 3)
		if(direction == 0):
			# up
			x = x-1
		elif(direction == 1):
			# right
			y = y+1
		elif(direction == 2):
			# down
			x = x+1
		else:
			# left
			y = y-1

		if(invalidPixel(x, y, PIX_MAP, colorTuple)):
			# if we found an invalid pixel, randomly choose one that we already painted
			newIndex = random.randint(0, len(ARTISTS[artistIndex])-1)
			currentPosition = ARTISTS[artistIndex][newIndex]
		else:
			# otherwise, set this new pixel as the current position and add it to our list
			# of pixels for this artist
			currentPosition = {"x": x, "y": y}
			ARTISTS[artistIndex].append(currentPosition)
		counter_lock.release()



def main(input):
	input = parseInputs(input)
	initializeArtistPostitions(input[0])
	initializeArtistColors(input[0])
	# print(ARTISTS)
	# print(ARTISTCOLORS)
	picture = createPicture()
	# picture.show()
	# print(type(picture.load()))
	PIX_MAP = picture.load()
	# print(PIX_MAP)

	threads = []
	for artistIndex in range(0, len(ARTISTS)):
		threads.append(threading.Thread(target = paint, args = [artistIndex, input[1], PIX_MAP, picture]))

	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	picture.show()
	picture.save("canvas.jpg")

if __name__ == '__main__':
	main(sys.argv)