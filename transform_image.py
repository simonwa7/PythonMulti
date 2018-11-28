import sys
from PIL import Image
import threading

MAX_THREADS = 500



counter_lock    = threading.Lock()

def parseInputs(input):
	parsed = []

	if((len(input) != 4) and (len(input) != 6)):
		sys.exit("Incorrect number of input parameters")

	if(not (input[3] in transforms)):
		sys.exit("Transform name not recognized")

	rows = 2 
	cols = 2
	if(len(input) == 6):
		rows = int(input[4])
		cols = int(input[5])

	if(rows*cols > MAX_THREADS):
		sys.exit("Exceeded thread count limit")

	parsed.append(input[1])
	parsed.append(input[2])
	parsed.append(input[3])
	parsed.append(rows)
	parsed.append(cols)
	return parsed

def getSubDimensions(pictureName, row, col):
	picture = Image.open(pictureName)
	width, height = picture.size
	print(width)
	print(height)
	coordinates = [];
	left = 0
	while(col > 0):
		down = 0
		remainingHeight = height
		remainingRows = row
		while(remainingRows > 0):
			topLeft = {"x": left, "y": down}
			down += remainingHeight/remainingRows
			remainingHeight -= remainingHeight/remainingRows
			remainingRows -= 1
			bottomRight = {"x": left+width/col, "y": down}
			# if(remainingRows == 0):
			# 	bottomRight["y"] += 1
			# if(col == 1):
			# 	bottomRight["x"] += 1 
			coord = {"topLeft": topLeft, "bottomRight": bottomRight}
			coordinates.append(coord)
		left += width/col
		width -= width/col
		col -= 1
	return coordinates

def switchRB(coordinates, pix_map, picture):
	for col in range(coordinates["topLeft"]["x"], coordinates["bottomRight"]["x"]):
		for row in range(coordinates["topLeft"]["y"], coordinates["bottomRight"]["y"]):
			r, g, b = pix_map[col, row]
			pix_map[col, row] = (b, g, r)

def blue(coordinates, pix_map, picture):
	for col in range(coordinates["topLeft"]["x"], coordinates["bottomRight"]["x"]):
		for row in range(coordinates["topLeft"]["y"], coordinates["bottomRight"]["y"]):
			r, g, b = pix_map[col, row]
			pix_map[col, row] = (r, g, b*b)

def blackAndWhite(coordinates, pix_map, picture):
	for col in range(coordinates["topLeft"]["x"], coordinates["bottomRight"]["x"]):
		for row in range(coordinates["topLeft"]["y"], coordinates["bottomRight"]["y"]):
			r, g, b = pix_map[col, row]
			pix_map[col, row] = (32, 32, 32)

def mirror(coordinates, pix_map, picture):
	width, height = picture.size
	for col in range(coordinates["topLeft"]["x"], coordinates["bottomRight"]["x"]):
		for row in range(coordinates["topLeft"]["y"], coordinates["bottomRight"]["y"]):
			r, g, b = pix_map[width-col-1, row]
			pix_map[col, row] = (r, g, b)

def mirrorVert(coordinates, pix_map, picture):
	width, height = picture.size
	for col in range(coordinates["topLeft"]["x"], coordinates["bottomRight"]["x"]):
		for row in range(coordinates["topLeft"]["y"], coordinates["bottomRight"]["y"]):
			r, g, b = pix_map[col, height-row-1]
			pix_map[col, row] = (r, g, b)

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

	picture = Image.open(input[0])
	pix_map = picture.load()
	threads = []
	for subpicture in coordinates:
		threads.append(threading.Thread(target = transforms[input[2]], args = [subpicture, pix_map, picture]))

	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	picture.show()





if __name__ == '__main__':
	main(sys.argv)