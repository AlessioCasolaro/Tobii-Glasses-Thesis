import csv as cs
import os
import gzip
import json
import pandas as pd
import matplotlib
import numpy



from fixatDetection import *
from fixColor import *
from pupil import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

COLS = {	"butter": [	'#fce94f',
					'#edd400',
					'#c4a000'],
		"orange": [	'#fcaf3e',
					'#f57900',
					'#ce5c00'],
		"chocolate": [	'#e9b96e',
					'#c17d11',
					'#8f5902'],
		"chameleon": [	'#8ae234',
					'#73d216',
					'#4e9a06'],
		"skyblue": [	'#729fcf',
					'#3465a4',
					'#204a87'],
		"plum": 	[	'#ad7fa8',
					'#75507b',
					'#5c3566'],
		"scarletred":[	'#ef2929',
					'#cc0000',
					'#a40000'],
		"aluminium": [	'#eeeeec',
					'#d3d7cf',
					'#babdb6',
					'#888a85',
					'#555753',
					'#2e3436'],
		}

def drawScanpath(dispsize, imagefile=None, durationsize=True, durationcolour=True, alpha=0.5, savefilename=None):

    # dati del grafico fixation
    csv_file = 'out/fixation.csv'
    # Salvo in un dataFrame il file letto
    dataFrame = pd.read_csv(csv_file)
    # Salvo in un array i valori dei campi che dovrò utilizzare
    data = dataFrame.iloc[:, [3, 4, 5,]].values
    dur = [element for element in data[:, 0]]
    posX = [element for element in data[: ,1]]
    posY = [element for element in data[: ,2]]

    # IMAGE
    fig,ax = draw_display(dispsize, imagefile=imagefile)

	# CIRCLES
	# duration weigths
    if durationsize:
	    siz = 1 * (dur/30.0)
    else:
	    siz = 1 * numpy.median(dur/30.0)
    if durationcolour:
	    col = dur
    else:
	    col = COLS['chameleon'][2]
	# draw circles
    ax.scatter(posX,posY, s=siz, c=col, marker='o', cmap='jet', alpha=alpha, edgecolors='none')

	# FINISH PLOT
	# invert the y axis, as (0,0) is top left on a display
    ax.invert_yaxis()
	# save the figure if a file name was provided
    if savefilename != None:
	    fig.savefig(savefilename)
	
    return fig

# HELPER FUNCTIONS
def draw_display(dispsize, imagefile=None):
	
	# construct screen (black background)
	_, ext = os.path.splitext(imagefile)
	ext = ext.lower()
	data_type = 'float32' if ext == '.png' else 'uint8'
	screen = numpy.zeros((dispsize[1],dispsize[0],3), dtype=data_type)
	# if an image location has been passed, draw the image
	if imagefile != None:
		# check if the path to the image exists
		if not os.path.isfile(imagefile):
			raise Exception("ERROR in draw_display: imagefile not found at '%s'" % imagefile)
		# load image
		img = mpimg.imread(imagefile)
		# flip image over the horizontal axis
		# (do not do so on Windows, as the image appears to be loaded with
		# the correct side up there; what's up with that? :/)
		if not os.name == 'nt':
			img = numpy.flipud(img)
		# width and height of the image
		w, h = len(img[0]), len(img)
		# x and y position of the image on the display
		x = dispsize[0]/2 - w/2
		y = dispsize[1]/2 - h/2
		# draw the image on the screen
		screen[y:y+h,x:x+w,:] += img
	# dots per inch
	dpi = 100.0
	# determine the figure size in inches
	figsize = (dispsize[0]/dpi, dispsize[1]/dpi)
	# create a figure
	fig = plt.figure(figsize=figsize, dpi=dpi, frameon=False)
	ax = plt.Axes(fig, [0,0,1,1])
	ax.set_axis_off()
	fig.add_axes(ax)
	# plot display
	ax.axis([0,dispsize[0],0,dispsize[1]])
	ax.imshow(screen)#, origin='upper')
	
	return fig, ax