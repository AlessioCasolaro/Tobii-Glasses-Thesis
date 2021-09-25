import csv as cs
import os
import gzip
import json
import pandas as pd
import matplotlib
import numpy
import cv2 



from fixatDetection import *
from fixColor import *
from pupil import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import sys
from PIL import Image, ImageDraw

SCREEN_DIMENSIONS = (1920, 1080)

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
def drawScanpath(imagefile=None, alpha=0.5, savefilename=None):

     # dati del grafico fixation
    csv_file = 'out/fixation.csv'
    # Salvo in un dataFrame il file letto
    dataFrame = pd.read_csv(csv_file)
    # Salvo in un array i valori dei campi che dovrò utilizzare
    data = dataFrame.iloc[:, [0,1,2, 3, 4]].values
    numFix = [element for element in data[:, 0]]
    start = [element for element in data[:, 1]]
    dur = [element for element in data[:, 2]]
    posX = [element for element in data[: ,3]]
    posY = [element for element in data[: ,4]]
    posXPix = []
    posYPix = []
    durS = []

    #Chiamo la funzione per trasformare da posizione schermo normalizzata ([0,0] a [1,1]) in pixel
    for x,y in zip(posX,posY):
        posXPix.append(to_pixel_coords(x,1920))
        posYPix.append(to_pixel_coords(y,1080))
        
    #Immagine
    fig, ax = draw_display(imagefile=imagefile)

    #Crea una lista di durate utile per la dimensione dei cerchi dello scanpath
    for d in dur:
        durS.append(d*300)
    
     #Disegna le fissazioni
    ax.scatter(posXPix,posYPix, durS)
     #Disegna le annotazioni, i numeri delle fissazioni
    for i in range(len(numFix)):
        ax.annotate(str(i+1), (posXPix[i],posYPix[i]), color=COLS['aluminium'][5], alpha=1, horizontalalignment='center', verticalalignment='center', multialignment='center')
     

    #Creazione saccadi
    for x, y,i in zip(posXPix,posYPix,range(len(numFix)-1)):
        #Creazione frecce che uniscono saccadi di inizio e fine
        ax.arrow(x, y, posXPix[i+1]-x, posYPix[i+1]-y, alpha=alpha, fc=COLS['aluminium'][0], ec=COLS['aluminium'][5], fill=True, shape='full', width=5, head_width=0, head_starts_at_zero=False, overhang=0)

    #Inverte l'asse y,(0,0) è in alto a sinistra del display
    ax.invert_yaxis()
    #Salva l'immagine col nome assegnato
    if savefilename != None:
        fig.savefig(savefilename)
    plt.close('all')
    return fig
    

#Funzioni di aiuto
def to_pixel_coords(coord,dimension):
    return round(coord * dimension)

def draw_display(imagefile=None):
    # Costruisci il black background
    _, ext = os.path.splitext(imagefile)
    ext = ext.lower()
    data_type = 'float32' if ext == '.png' else 'uint8'
    screen = numpy.zeros((SCREEN_DIMENSIONS[1],SCREEN_DIMENSIONS[0],3), dtype=data_type)
    # Se il path dell'immagine esiste, continua
    if imagefile != None:
        # Controlla se il path dell'immagine esiste
        if not os.path.isfile(imagefile):
            raise Exception("ERRORE in draw_display: immagine non trovata nel percorso '%s'" % imagefile)
        #Carica l'immagine
        img = mpimg.imread(imagefile)
        #Larghezza e altezza dell'immagine
        w, h = len(img[0]), len(img)
        #x e y posizioni dell'immagine sul display
        x = int(SCREEN_DIMENSIONS[0]/2 - w/2)
        y = int(SCREEN_DIMENSIONS[1]/2 - h/2)
        print(w,h,x,y)
        #Disegna l'immagine sullo schermo
        screen[y:y+h,x:x+w,:] += img
    # dots per inch
    dpi = 100.0
    # Determina la grandezza per la figura in dpi
    figsize = (SCREEN_DIMENSIONS[0]/dpi, SCREEN_DIMENSIONS[1]/dpi)
    #Crea una figura
    fig = plt.figure(figsize=figsize, dpi=dpi, frameon=False)
    ax = plt.Axes(fig, [0,0,1,1])
    ax.set_axis_off()
    fig.add_axes(ax)
    #Plot display
    ax.axis([0,SCREEN_DIMENSIONS[0],0,SCREEN_DIMENSIONS[1]])
    ax.imshow(screen)
    
    return fig, ax

def getVideoFrame(path):
    # Opens the Video file
    cap= cv2.VideoCapture(path)
    i=1
    currentframe=0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        if i%120 == 0:
            name = './frames/frame' + str(currentframe) + '.jpg'
            print ('Captured...' + name)
            cv2.imwrite(name,frame)
            currentframe += 1
        i+=1
    
    cap.release()
    cv2.destroyAllWindows()

