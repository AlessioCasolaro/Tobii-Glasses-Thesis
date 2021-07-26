import gzip
import json


# Funzione usata per creare una lista avente la durata di ogni scena trovata.
def durEachScen(char):

    # Apro il file imudata del video corrispondente
    with gzip.open('dataImu/imudata'+str(char)+'.gz') as f:

        # Variabili
        positionX = []
        positionY = []
        positionZ = []
        positionXG = []
        positionYG = []
        positionZG = []
        time = []

        # Riempio le liste per ogni riga del file
        for raw in f:
            d = json.loads(raw)
            timestamp = d.get('timestamp')
            accelerometer = d.get('data', {}).get('accelerometer')
            gyroscope = d.get('data', {}).get('gyroscope')
            if accelerometer != None:
                time.append(timestamp)
                positionX.append(accelerometer[0])
                positionZ.append(accelerometer[2])
                positionXG.append(gyroscope[0])
                positionYG.append(gyroscope[1])
                positionZG.append(gyroscope[2])

        # Mi restituisce la durata di ogni scena trovata
        NumChangeScen = frameVideoCapt(positionX, positionZ, positionXG, positionYG, positionZG, time)

        return NumChangeScen


# Funzione che restituisce una lista avente i valori medii del tempo di ogni cambio di scena
def numberScene(char):
    NumChangeScen = durEachScen(char)                        # Richiamo la funzione durEachScen
    #return NumChangeScen

    ImgCapt = []                                            # Lista vuota
    for i in range(0,len(NumChangeScen)):

        # Prendo il valore massimo del tempo della lista NumCambScen
        for j in NumChangeScen:
            maxNum = j

        # Confronto l' i-esimo valore della lista 'NumCambScen'. Se è minore del massimo valore di tale lista
        # allora inserisco il valore medio, tra 'i-esimo valore e il successivo valore, nella lista ImgCapt
        if NumChangeScen[i] < maxNum:
            med = (NumChangeScen[i]+NumChangeScen[i+1])/2
            ImgCapt.append(med)
    return ImgCapt

# Funzione per restituire il numero di immagini in base ai valori dell'accelerometro
# Funzione usata per per restituire il tempo finale di ogni cambio di scena del video
# I parametri sono: listX = valori X dell' accelerometro; listZ = valori Z dell'accelerometro
#                   listTime = valori Time dell'accelerometro
def frameVideoCapt(listX, listZ, listXG, listYG, listZG, listTime):
    a = len(listX)                              # Taglia della lista 'listX'
    SScen = []                                  # Lista vuota per i valori iniziali di ogni cambio di scena del video
    FScen = []                                  # Lista vuota per i valori finali di ogni cambio di scena del video

    for i in listTime:
        maxTime = i                             # Valore massimo del tempo della lista 'listTime'
    si = 0
    dist = 0.0
    cont = 0
    scenStart = False
    count2= 0
    # Loop per la taglia della lista 'listX'
    for i in range(a):

        # Calcolo le distanze quadratiche tra l'i-esimo valore e il suo successivo
        quadr_dist_X = (listX[si] - listX[i]) ** 2
        #quadr_dist_Y = (listY[si] - listY[i]) ** 2
        quadr_dist_Z = (listZ[si] - listZ[i]) ** 2
        # Mi trovo la radice delle distanze quadratiche e le sommo
        if quadr_dist_X>0:
            dist_X = quadr_dist_X ** 0.5
            #dist_Y = quadr_dist_Y ** 0.5
            dist_Z = quadr_dist_Z ** 0.5
            dist = dist_X + dist_Z
           
        # Controllo se gli occhiali si sono spostati dal punto precedente di 3 (distanza di x e y)
        # Controllo il valore di dist, se la distanza è minore di 3 e non è iniziata una scena allora
        # inizio una nuova scena altrimenti se la distanza è maggiore di 4.5 ed è già iniziata una scena
        # allora termino la scena
        if dist <= 3 and not scenStart:
            count2+=1
            # inizia una nuova scena
            si = 0 + i
            scenStart = True
            SScen.append([listTime[i]])
            
        elif dist > 4.5 and scenStart:
            
            # termino scena
            scenStart = False

            # Controllo se la durata del cambio di scena è maggiore di 18 secondi
            # Se è inferiore è inutile prendere il dato in considerazione perchè non saranno presenti punti di fissazioni
            # o aree di interesse
            if listTime[i-1] - SScen[-1][0] >= 1:
                FScen.append(SScen[-1][0])
                cont += 1
            else:
                SScen.pop(-1)
            si = 0 + i
        elif not scenStart:
            si += 1
    # Se avrò una sola scena, nella lista 'FScen' inserisco anche il tempo iniziale oltre a quello finale
    if len(FScen)==0:
        FScen.append(0)
    FScen.append(maxTime)
    if count2 <=10:

        a2 = len(listXG)  # Taglia della lista 'listX'
        SScen2 = []  # Lista vuota per i valori iniziali di ogni cambio di scena del video
        FScen2 = []  # Lista vuota per i valori finali di ogni cambio di scena del video

        for i in listTime:
            maxTime2 = i  # Valore massimo del tempo della lista 'listTime'
        si2 = 0
        dist2 = 0.0
        cont2 = 0
        scenStart2 = False
        for i in range(a2):

            # Calcolo le distanze quadratiche tra l'i-esimo valore e il suo successivo
            quadr_dist_X = (listXG[si2] - listXG[i]) ** 2
            quadr_dist_Y = (listYG[si2] - listYG[i]) ** 2
            quadr_dist_Z = (listZG[si2] - listZG[i]) ** 2
            # Mi trovo la radice delle distanze quadratiche e le sommo
            if quadr_dist_X > 0:
                dist_X = quadr_dist_X ** 0.5
                dist_Y = quadr_dist_Y ** 0.5
                dist_Z = quadr_dist_Z ** 0.5
                dist2 = dist_X + dist_Y + dist_Z
                
            # Controllo se gli occhiali si sono spostati dal punto precedente di 3 (distanza di x e y)
            # Controllo il valore di dist, se la distanza è minore di 3 e non è iniziata una scena allora
            # inizio una nuova scena altrimenti se la distanza è maggiore di 4.5 ed è già iniziata una scena
            # allora termino la scena
            if dist2 <= 45 and not scenStart2:
                # inizia una nuova scena
                si2 = 0 + i
                scenStart2 = True
                SScen2.append([listTime[i]])
               
            elif dist2 > 45 and scenStart2:
             
                # termino scena
                scenStart2 = False

                # Controllo se la durata del cambio di scena è maggiore di 18 secondi
                # Se è inferiore è inutile prendere il dato in considerazione perchè non saranno presenti punti di fissazioni
                # o aree di interesse
                if listTime[i - 1] - SScen2[-1][0] >= 1:
                    FScen2.append(SScen2[-1][0])
                    cont2 += 1
                else:
                    SScen2.pop(-1)
                si2 = 0 + i
            elif not scenStart:
                si2 += 1
        # Se avrò una sola scena, nella lista 'FScen' inserisco anche il tempo iniziale oltre a quello finale
        if len(FScen2) == 0:
            FScen2.append(0)
        FScen2.append(maxTime2)
        return FScen2
    else:
        return FScen


