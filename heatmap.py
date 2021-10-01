import os
import numpy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import tkinter as tk
import cv2

precision = 200  # Precisione
edge = 200 / 6  # Smussa gli angoli di calore
#Acquisisco la grandezza del display

root = tk.Tk()#Libreria tkinter 
displayWidth = root.winfo_screenwidth()
displayHeight = root.winfo_screenheight()

def draw_heatmap(): 

    # dati del grafico fixation
    csv_file = 'out/fixation.csv'
    # Salvo in un dataFrame il file letto
    dataFrame = pd.read_csv(csv_file)
    # Salvo in un array i valori dei campi che dovrò utilizzare
    data = dataFrame.iloc[:, [2, 3, 4]].values

    dur = [element for element in data[:, 0]]
    posX = [element for element in data[:, 1]]
    posY = [element for element in data[:, 2]]
    posXPix = []
    posYPix = []
  
    # Costruisco l'immagine
    fig, ax = imgDraw() 

    # Chiamo la funzione per trasformare da posizione schermo normalizzata ([0,0] a [1,1]) in pixel
    for x, y in zip(posX, posY):
        posXPix.append(int(to_pixel_coords(x, displayWidth)))  # Rendere dinamico
        posYPix.append(int(to_pixel_coords(y, displayHeight)))
    # Creo la matrice usando il Kernel Gaussiano
    M = kernelG(precision, edge)
    
    halfp = precision / 2
    # Definisco la grandezza dell'heatmap
    heatmapsize = int(displayHeight + precision), int(displayWidth + precision)
    # Inizializzo la matrice dell'heatmap riempiendola di zero
    heatmap = numpy.zeros(heatmapsize, dtype=float)
    # Crea l'heatmap
    for i in range(0, len(dur)):
        x = posXPix[i]
        y = posYPix[i]
        # Correggo il kernel Gaussiano per non uscire dai confini del display
        if (not 0 < x < displayWidth) or (not 0 < y < displayHeight):
            adjustedX = adjustedY =  [0, precision]
            
            if displayWidth < x:  # Controllo se la coordinata x esce dal display
                adjustedX[1] = precision - int(x - displayWidth)
           
            elif displayHeight < y:  # Controllo se la coordinata y esce dal display
                adjustedY[1] = precision - int(y - displayHeight)
    
            heatmap[y:y + adjustedY[1], x:x + adjustedX[1]] += M[adjustedY[0]:adjustedY[1], adjustedX[0]:adjustedX[1]] * dur[i]
            
        else:
            # Aggiunta del kernel gaussiano alla heatmap
            heatmap[int(y):int(y + precision), int(x):int(x + precision)] += M * dur[i]

    #Aggiusto la grandezza dell'heatmap per adattarsi al display
    heatmap = heatmap[int(halfp):int(displayHeight + halfp), int(halfp):int(displayWidth + halfp)]
    # Rimuovo gli zero dalla matrice
    avg = numpy.mean(heatmap[heatmap > 0])# Media dei valori nell'array
    heatmap[heatmap < avg] = numpy.NaN
    # Applico l'heatmap sull'immagine
    ax.imshow(heatmap, cmap='jet', alpha=0.5)

    # Inverte gli assi, necessario su Windows e macOs
    ax.invert_yaxis()
    fig.savefig("out/Heatmap/heatmap.jpg")  # Salvo l'immagine
    return fig


# Funzioni di aiuto
# Trasforma le coordinate da deviazione standard [0,0] a Pixel
def to_pixel_coords(coord, dimension):
    return round(coord * dimension)


def imgDraw():
   
    path = 'out/Heatmap/FrameForHeatmap.jpg'
    screen = numpy.zeros((displayHeight, displayWidth, 3), dtype='uint8') #Utilizzo uint8 per .jpg
  
    # Controlla se il path dell'immagine esiste
    if not os.path.isfile(path):
        print("Immagine non trovata nel percorso")

    # Carica l'immagine
    img = mpimg.imread(path)
    # Larghezza e altezza dell'immagine
    w, h = len(img[0]), len(img)
    # x e y posizioni dell'immagine sul display
    x = int(displayWidth / 2 - w / 2)
    y = int(displayHeight / 2 - h / 2)
    
    # Disegna l'immagine sullo schermo
    screen[y:y + h, x:x + w, :] += img

    # Determina la grandezza per la figura in dpi 100
    figsize = (displayWidth / 100.0 , displayHeight / 100.0)
    # Crea una figura
    fig = plt.figure(figsize=figsize, dpi=100.0, frameon=False)
    ax = plt.Axes(fig, [0, 0, 1, 1])
    ax.set_axis_off()
    fig.add_axes(ax)

    ax.axis([0, displayWidth, 0, displayHeight])
    ax.imshow(screen)

    return fig, ax


# Funzione per calcolare l'intensità del nucleo 
def kernelG(x, y):
    # Centro
    xC = yC = x / 2
    # Rimpio la matrice di zero
    M = numpy.zeros([x, x], float)
    # Riempio la matrice con la formula di Gauss
    for i in range(x):
        for j in range(x):
            M[j, i] = numpy.exp(-1.0 * (((float(i) - xC) ** 2 / (2 * y * y)) + ((float(j) - yC) ** 2 / (2 * y * y))))

    return M

# Estrae un frame al centro del video
def extractMiddleFrame(pathVideo):
    # Apro il video
    cap= cv2.VideoCapture(pathVideo)
    #Contro il numero totale di frame
    frameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    middle = frameCount/2 #Trovo il centro del video
    i=1
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:# Se il frame non è stato letto
            break
        if i%int(middle) == 0:# Ho trovato il centro, salvo il frame
            cv2.imwrite('out/Heatmap/FrameForHeatmap.jpg',frame)
            print("Sto salvando l'immagine")
            break
        i+=1   
    
    cap.release()
    cv2.destroyAllWindows()
