# PythonMulti
Learning to multithread in Python

## Purpose
The files included in this repository detail some of my attempts to learn how to utilize the mutlithreading capabilities in Python.

## Files
### transform_image.py
#### Purpose
  This program is designed to take in a picture on input and perform a previously defined transformation on it that alters the pixels in the photo to create a new picture. This new picture is then saved under the filename defined on input.
  
#### Usage
  To use this program, the input parameters are as follows:
  ```
  python transform_image.py [input picture filename] [save picture filename] [transform]
  ```
  or
  ```
  python transform_image.py [input picture filename] [save picture filename] [transform] [rows] [cols]
  ```
  Where transform is one of the following defined transforms:
  * ``` switch-r-b ``` - which switches the red and blue pixel values
  * ``` bluify ``` - which exaggerates the blue value for each pixel
  * ``` bw ``` - still under production
  * ``` mirror ``` - which mirrors the picture by the left and right sides
  * ``` mirrorVert ``` - which mirrors the picture by the top and bottom
  
  Additionally, the optional rows and cols input allow the client to define the number of threads used. If no input is given, the program defaults to four threads. When input, the program splits the picture into an even grid based on the number of rows and columns and modifies the picture where each block in the grid is a separate thread.
  
### procedural_artist.py
  This program is designed to "paint a canvas" (a 512x512 jpg) where each thread creates a different artist with a different color. The artists are given a unique starting position on the canvas and paint the canvas pixel by pixel by going up, down, left, or right. If the artist runs into another artist's brush stroke, they choose a random location to begin again from the pixels that they have already painted. It then saves the image as "canvas.jpg".

#### Usage
  To use this program, the input parameters are as follows:
  
  ``` python procedural_artist.py -M [number of artists] -S [number of steps] ```
  
  Where each artist is a separate thread (maximum is preset) and each artist paints for the number of steps defined on input (for example, if we have 5 artists and 3 steps, each of the 5 artists will attempt to paint 3 pixels; they will only be unsuccessful in painting 3 pixels if they run into the edge of the canvas or another artists brush stroke).
