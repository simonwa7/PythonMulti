import sys
from PIL import Image
import threading
import random

MAX_THREADS = 2000
counter_lock    = threading.Lock()

# ARTISTS data structure:
# [] [] [] [] [] [] [] [] -- list of artists
# [] [] [] [] [] [] [] [] -- vertically is a list of owned pixels
# [] [] [] [] [] [] [] []
#

ARTISTS = []
ARTISTCOLORS = []
# PIX_MAP = None

def parseInputs(input):
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
	for artist in ARTISTS:
		if((artist[0]["x"] == x) and (artist[0]["y"] == y)):
			return True
	return False

def initializeArtistPostitions(numArtists):
	x = 512
	y = 512
	for i in range(0, numArtists):
		x = random.randint(0, 511)
		y = random.randint(0, 511)
		while(startingPositionClaimed(x, y)):
			x = random.randint(0, 511)
			y = random.randint(0, 511)
		artist = [{"x": x, "y": y}]
		ARTISTS.append(artist)

def colorClaimed(r, g, b):
	for artist in ARTISTCOLORS:
		if((artist["r"] == r) and (artist["g"] == g) and (artist["b"] == b)):
			return True
	return False

def initializeArtistColors(numArtists):
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
	picture = Image.new('RGB', (512, 512), color = (255, 255, 255))
	return picture

def invalidPixel(x, y, PIX_MAP, colorTuple):
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

def paint(artistIndex, numSteps, PIX_MAP):
	currentPosition = ARTISTS[artistIndex][0]
	color = ARTISTCOLORS[artistIndex]
	colorTuple = (color["r"], color["g"], color["b"])
	for i in range(0, numSteps):
		x = currentPosition["x"]
		y = currentPosition["y"]
		PIX_MAP[x, y] = colorTuple

		direction = random.randint(0, 3)
		if(direction == 0):
			x = x-1
		elif(direction == 1):
			y = y+1
		elif(direction == 2):
			x = x+1
		else:
			y = y-1

		if(invalidPixel(x, y, PIX_MAP, colorTuple)):
			newIndex = random.randint(0, len(ARTISTS[artistIndex])-1)
			currentPosition = ARTISTS[artistIndex][newIndex]
		else:
			currentPosition = {"x": x, "y": y}
			ARTISTS[artistIndex].append(currentPosition)



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
		threads.append(threading.Thread(target = paint, args = [artistIndex, input[1], PIX_MAP]))

	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	picture.show()

if __name__ == '__main__':
	main(sys.argv)