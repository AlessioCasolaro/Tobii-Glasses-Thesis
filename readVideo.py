import cv2

from readDataImu import *

# Funzione per ridimensionare i frame del video
def rescaleFrame(frame):
    scale_percent = 60
    width = int(frame.shape[1] * (scale_percent / 100))         # Restituisco la lunghezza per ogni frame
    height = int(frame.shape[0] * (scale_percent / 100))        # Restituisco l' altezza per ogni frame
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

def resImage(name, char):
    cap = cv2.VideoCapture('video/'+str(name))
    listDur = numberScene(char)
    fps = cap.get(cv2.CAP_PROP_FPS)  # Prendo il valore degli fps del video

    # Moltipli ogni valore della lista 'listDur' per gli fps del video in modo che mi restituisca
    # una lista di frame
    frameList = [int(element * fps) for element in listDur]

    for x in range(len(frameList)):
        cap.set(1, frameList[x])
        ret, frame = cap.read()
        cv2.imwrite('image/img%d.png' % x, frame)


# Funzione per riprodurre il video, riceve in input il nome del video
def streamVideo(name):
    cap =cv2.VideoCapture('video/'+str(name))       # Acquisizione del video dal file video
    print("Digitare 'q' sulla finestra del video per interrompere tale video ")
    #charV = name[10]                                # Prendo il carattere nella posizione 10 del nome del video, corrisponde al numero del video

    # Acquisizione dell'accelerometro
    # Mi deve restituire quante immagini considerare.

    #listDur = numberScene(char)                    # Mi restituisce i valori del tempo di quando è cambiata la scena in una lista

    # Confronto se il video è aperto o no
    if(cap.isOpened() == False):
        print("Errore apertura video")
    #i = 0
    #j = 0
    #a = 0
    """
    fps = cap.get(cv2.CAP_PROP_FPS)                 # Prendo il valore degli fps del video



    # Moltipli ogni valore della lista 'listDur' per gli fps del video in modo che mi restituisca
    # una lista di frame
    frameList = [int(element * fps) for element in listDur]
    
    for x in range(len(frameList)):
        cap.set(1,frameList[x])
        ret, frame = cap.read()
        cv2.imwrite('image/img%d.png' % x, frame)
    """
    while(cap.isOpened()):
        ret, frame = cap.read()                     # Lettura di ogni frame

        if ret == True:
            frame2 = rescaleFrame(frame)            # Richiamo la funzione rescaleFrame per ridimensionare ogni frame
            cv2.imshow('Video', frame2)             # Visualizzo il video

            # Se finisce il video oppure digito 'q' allora chiude la finestra del video
            if cv2.waitKey(1) ==ord('q'):
                print("Video interrotto!.")
                break


        else:
            print("Video riprodotto con successo!")
            break


    # Quando tutto è fatto, allora libera cap e distruggi ogni finestra
    cap.release()
    cv2.destroyAllWindows()
