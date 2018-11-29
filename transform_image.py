import sys
from PIL import Image
import threading

MAX_THREADS = 500
counter_lock    = threading.Lock()

def parseInputs(input):
	# Parse input parameters and exit if invalid
	parsed = []

	# make sure number of inputs is valid
	if((len(input) != 4) and (len(input) != 6)):
		sys.exit("Incorrect number of input parameters")

	# make sure a valid transform is specified
	if(not (input[3] in transforms)):
		sys.exit("Transform name not recognized")

	# default rows and cols
	rows = 2 
	cols = 2
	if(len(input) == 6):
		rows = int(input[4])
		cols = int(input[5])

	# check if thread count is not exceeded
	if(rows*cols > MAX_THREADS):
		sys.exit("Exceeded thread count limit")

	parsed.append(input[1])
	parsed.append(input[2])
	parsed.append(input[3])
	parsed.append(rows)
	parsed.append(cols)
	return parsed

def getSubDimensions(pictureName, row, col):
	# This function is designed to give the coordinates for each block in the grid
	picture = Image.open(pictureName)
	width, height = picture.size
	coordinates = [];

	# start at the left
	left = 0
	while(col > 0):
		# start at the top
		down = 0
		remainingHeight = height
		remainingRows = row
		while(remainingRows > 0):
			# set the coordinates for every row in this column
			topLeft = {"x": left, "y": down}
			down += remainingHeight/remainingRows
			remainingHeight -= remainingHeight/remainingRows
			remainingRows -= 1
			bottomRight = {"x": left+width/col, "y": down}
			coord = {"topLeft": topLeft, "bottomRight": bottomRight}
			coordinates.append(coord)
		left += width/col
		width -= width/col
		col -= 1
	return coordinates

def switchRB(coordinates, pix_map, picture):
	# Switch the red and blue values for each pixel in the given coordinate range
	for col in range(coordinates["topLeft"]["x"], coordinates["bottomRight"]["x"]):
		for row in range(coordinates["topLeft"]["y"], coordinates["bottomRight"]["y"]):
			counter_lock.acquire()
			r, g, b = pix_map[col, row]
			pix_map[col, row] = (b, g, r)
			counter_lock.release()

def blue(coordinates, pix_map, picture):
	# Squares the blue value for each pixel in the given coordinate range
	for col in range(coordinates["topLeft"]["x"], coordinates["bottomRight"]["x"]):
		for row in range(coordinates["topLeft"]["y"], coordinates["bottomRight"]["y"]):
			counter_lock.acquire()
			r, g, b = pix_map[col, row]
			pix_map[col, row] = (r, g, b*b)
			counter_lock.release()

def blackAndWhite(coordinates, pix_map, picture):
	# Not ready
	for col in range(coordinates["topLeft"]["x"], coordinates["bottomRight"]["x"]):
		for row in range(coordinates["topLeft"]["y"], coordinates["bottomRight"]["y"]):
			counter_lock.acquire()
			r, g, b = pix_map[col, row]
			pix_map[col, row] = (32, 32, 32)
			counter_lock.release()

def mirror(coordinates, pix_map, picture):
	# For each pixel in the current range, set it equal to the pixel reflected over
	# a vertical line through the middle of the image
	width, height = picture.size
	for col in range(coordinates["topLeft"]["x"], coordinates["bottomRight"]["x"]):
		for row in range(coordinates["topLeft"]["y"], coordinates["bottomRight"]["y"]):
			counter_lock.acquire()
			r, g, b = pix_map[width-col-1, row]
			pix_map[col, row] = (r, g, b)
			counter_lock.release()

def mirrorVert(coordinates, pix_map, picture):
	# For each pixel in the current range, set it equal to the pixel reflected over
	# a horizontal line through the middle of the image
	width, height = picture.size
	for col in range(coordinates["topLeft"]["x"], coordinates["bottomRight"]["x"]):
		for row in range(coordinates["topLeft"]["y"], coordinates["bottomRight"]["y"]):
			counter_lock.acquire()
			r, g, b = pix_map[col, height-row-1]
			pix_map[col, row] = (r, g, b)
			counter_lock.release()

# A dictionary containing all the defined transformations
transforms = {
	"switch-r-b": switchRB,
	"bluify": blue,
	"bw": blackAndWhite,
	"mirror": mirror,
	"mirrorVert": mirrorVert	
}

def main(input):
	input = parseInputs(input)
	coordinates = getSubDimensions(input[0], input[3], input[4])

	# open the picture
	picture = Image.open(input[0])
	# load the pixels
	pix_map = picture.load()
	# create a list of threads using the threading library
	threads = []
	for subpicture in coordinates:
		threads.append(threading.Thread(target = transforms[input[2]], args = [subpicture, pix_map, picture]))

	# start each thread
	for thread in threads:
		thread.start()
	# wait for each thread to finish
	for thread in threads:
		thread.join()
	picture.show()
	picture.save(input[1])





if __name__ == '__main__':
	main(sys.argv)