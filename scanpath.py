import cv2
import pandas as pd
import tkinter as tk
import keyboard

def generateScanpath(path):
    # dati del grafico fixation
    csv_file = 'out/fixation.csv'
    # Salvo in un dataFrame il file letto
    dataFrame = pd.read_csv(csv_file)
    # Salvo in un array i valori dei campi che dovrò utilizzare
    data = dataFrame.iloc[:, [0, 1, 2, 3, 4]].values
    numFix = [element for element in data[:, 0]]
    start = [element for element in data[:, 1]]
    dur = [element for element in data[:, 2]]
    posX = [element for element in data[:, 3]]
    posY = [element for element in data[:, 4]]
    posXPix = []
    posYPix = []
    times = []
    Xtemp = []
    Ytemp = []
    flag = False#Utile per interrompere il video
    

    #Formatto i Tempi
    for s, d in zip(start, dur):
        times.append(float("{:.1f}".format(s + d)))  # Secondi

    #Acquisisco la grandezza del display
    root = tk.Tk()#Libreria tkinter 
    displayWidth = root.winfo_screenwidth()
    displayHeight = root.winfo_screenheight()

    #Formatto x,y per avere le coordinate in pixel
    for x, y in zip(posX, posY):
        posXPix.append(round(x * displayWidth))
        posYPix.append(round(y * displayHeight))


    vid_filename = path #Il video utilizzato, specificato nel main

    cap = cv2.VideoCapture(vid_filename)
    count = 1
    fps = int(cap.get(cv2.CAP_PROP_FPS)) #Salvo il numero di fps del video
    i = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if ret is False:
            break  # Break loop nel caso in cui ret è falso (lo diventa nell'ultimo frame)

        for x, y, t, d in zip(posXPix, posYPix, start, dur):
            if abs(count - (t+d) * fps) <= 1: #Per sincronizzare il tempo in cui si è verificata la fissazione con il frame
                # Disegno i cerchi
                cv2.circle(frame, (int(x), int(y)), 10, (255, 0, 0), -1)

                #Posiziono l'elemento scansionato in una lista temporanea utile a ridisegnare i cerchi precedenti
                Xtemp.append(x)
                Ytemp.append(y)
                for a, b, i in zip(Xtemp, Ytemp, range(len(Xtemp) - 1)):
                    #Ridisegno i cerchi precedenti
                    cv2.circle(frame, (int(a), int(b)), 10, (255, 0, 0), -1)

                    # Creazione saccadi
                    # Creazione frecce che uniscono saccadi di inizio e fine
                    cv2.line(frame, (Xtemp[i], Ytemp[i]), (Xtemp[i + 1], Ytemp[i + 1]), (238, 238, 238), 2)
                    # cv2.putText(frame, str(i), (posXPix[i], posYPix[i]), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.imshow('Scanpath', frame)
                cv2.waitKey(1000)
                #Comando per bloccare l'esecuzione dei cicli e la creazione dello scanpath sul video
                if keyboard.is_pressed('q'):
                    print('Video interrotto.')
                    flag = True#Setto il flag a true
                    break
            if flag == True:#Ci entro solo se è stato premuto il tasto q, faccio terminare i cicli
                break        
                    
        count += 1
            
    cap.release()
    if flag == True:#Ci entro solo se è stato premuto il tasto q, chiudo il video
        cv2.destroyAllWindows() 
        