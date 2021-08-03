import csv
import gzip
import json
import pandas as pd
import matplotlib

from fixatDetection import *
from fixColor import *
from pupil import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#Funzione per stampare il file pupil.csv sulla console
def readFileFix():
    csv_file = 'out/pupil.csv'
    data = pd.read_csv(csv_file)
    print(data)
    csv_file2 = 'out/pupilsStatistics.csv'
    data2 = pd.read_csv(csv_file2)
    print(data2)

# Funzione utilizzata per leggere i dati del file gazedata.gz e scrivere un nuovo file .csv
def readData(char):
    # Confronto il nome del video
    with gzip.open('dataGaze/gazedata' + str(char) + '.gz') as f1:

        # Liste vuote
        positionX = []
        positionY = []
        positionZ = []
        time = []
        eyeLFdiameter = []
        eyeRGdiameter = []
        averageLFRG = []
        TotalAverageLFandRG = []

        # Loop per leggere ogni riga nel file
        for data in f1:

            # Assegno  le righe al dictionary dicto
            d = json.loads(data)

            # Salvo nelle variabili i campi che servono dal dictionary
            timestamp = d.get('timestamp')
            gaze2d = d.get('data', {}).get('gaze2d')
            gaze3d = d.get('data', {}).get('gaze3d')
            eyeleftdiameter = d.get('data', {}).get('eyeleft', {}).get('pupildiameter')
            eyerightdiameter = d.get('data', {}).get('eyeright', {}).get('pupildiameter')
        
            # Controllo se il campo gaze3d è vuoto
            # Se lo è assegno alle liste il valore 0
            # Altrimenti assegno i valori delle variabili

            if eyeleftdiameter == None:
                 eyeLFdiameter.append(0)  # lista eyelfdiameter
            else:
                 eyeLFdiameter.append(eyeleftdiameter)  # lista eyelfdiameter

            if eyerightdiameter == None:
                 eyeRGdiameter.append(0)  # lista eyergdiameter
            else:
                 eyeRGdiameter.append(eyerightdiameter)  # lista eyergdiameter

            if gaze3d == None:
                positionX.append(0)
                positionY.append(0)
                positionZ.append(0)
            else:
                positionX.append(gaze2d[0])  # lista coordinata x
                positionY.append(gaze2d[1])  # lista coordinata y
                positionZ.append(gaze3d[2])  # lista coordinata z
                time.append(timestamp)  # lista timestamp

        # for per iterare su ciascun diametro di ogni istante
        for diamLF,diamRG in zip(eyeLFdiameter,eyeRGdiameter):
            averageLFRG.append(averageLeftAndRight(diamLF,diamRG))
        
        minAndMaxDiameter = minLeftAndRight(eyeLFdiameter,eyeRGdiameter)
 
        # fields è una lista avente i nomi dei campi del nuovo file csv
        fields = ['Timestamp','EyeLeftDiameter','EyeRightDiameter','AverageLeftAndRight']

        # Creazione e apertura del file di nome pupil.csv
        with open('out/pupil.csv', 'w', newline="") as cvs:

            # w è una dictionary con i campi della lista fields
            w = csv.DictWriter(cvs, fieldnames=fields, delimiter=',')
            w.writeheader()

            # Loop per inserire i valori delle liste nei campi del dictionary
            for stime,diamLF,diamRG, average in zip(time,eyeLFdiameter,eyeRGdiameter, averageLFRG):
               raw = {'Timestamp':stime, 'EyeLeftDiameter': diamLF, 'EyeRightDiameter': diamRG, 'AverageLeftAndRight':average}
               w.writerow(raw)
            
        # Apertura del file di nome pupil.csv in modalità append
        with open('out/pupilsStatistics.csv', 'w', newline="") as csvfile:

            # fieldnames è una lista avente i nomi dei campi per l'append
            fieldnames = ['TotalAverageLeft','TotalAverageRight','TotalAverageLFandRG','MinDiameterLeft','MinDiameterRight','MaxDiameterLeft','MaxDiameterRight']

            # writer è una dictionary con i campi della lista fieldnames
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Inserisco i valori nei campi del dictionary
            writer.writerow({'TotalAverageLeft': averangeTotal(eyeLFdiameter),'TotalAverageRight': averangeTotal(eyeRGdiameter), 'TotalAverageLFandRG':averangeLFRGTotal(averangeTotal(eyeLFdiameter),averangeTotal(eyeRGdiameter)),'MinDiameterLeft':minAndMaxDiameter[0],'MinDiameterRight':minAndMaxDiameter[1],'MaxDiameterLeft':minAndMaxDiameter[2],'MaxDiameterRight':minAndMaxDiameter[3]})

        readFileFix()
        cvs.close()  # Chiusura del file


# Funzione per creare e visualizzare il grafico delle fissazioni
def graficFix(nImg, scene):
    
    print("All'utente verranno mostrate %d immagini" % nImg)
    # dati del grafico fixation
    csv_file = 'out/pupil.csv'
    # Salvo in un dataFrame il file letto
    dataFrame = pd.read_csv(csv_file)
    # Salvo in un array i valori dei campi che dovrò utilizzare
    data = dataFrame.iloc[:, [1, 2, 3]].values
    s = 1
    time = [element for element in data[:, 0]]
    z1 = [element for element in data[: ,2]]
    time2 = []
    smin = 0
    w=0

    z1.sort()  # Ordino le coordinate z
    # Loop per trovare il minimo e massimo delle coordinate z
    for i in z1:
        maxZ = i
        minZ = z1[0]
    print('''Scegliere l'opzione da eseguire: 
                                1. Settare intervalli uguali
                                2. Settare intervalli misti
                                3. Unico intervallo con gradazione dei colori
                            ''')
    choose = input("Digita l'opzione scelta: ")

    while(True):
        if choose != str(1) and choose != str(2) and choose != str(3):
            print("Numero o parola inserita non valida")
            choose = input("Ridigita: ")
        else:
            break
    if choose == str(1) or choose == str(2):
        n = interChoose()
    print("All'utente verranno mostrate %d immagini" % nImg)
    # Loop per il numero delle immagini
    # Per ogni immagine prendo i valori x, y, z, dur e time dal tempo di inizio al tempo di fine di quell'immagine
    for z in range(0,(nImg)):
        print("Immagine n. %s " % str(z+1))
        img = mpimg.imread('image/img'+str(z)+'.png')
        # Utilizzati per moltiplicare gli elementi x e y per la dimensione dell immagine
        width = img.shape[1]
        height = img.shape[0]

        for t in time:
            if t <= scene[s]:
                time2.append(t)

        x = [element * width for element in data[smin:len(time2), 0]]       # x contiene gli elementi della colonna 2 di data dal tempo minimo al tempo massimo
        y = [element * height for element in data[smin:len(time2),1]]       # y contiene gli elementi della colonna 3 di data dal tempo minimo al tempo massimo
        z = [element for element in data[smin:len(time2),2]]                # z contiene gli elementi della colonna 4 di data dal tempo minimo al tempo massimo
        dur = [element for element in data[smin:len(time2),0]]              # dur contiene gli elementi della colonna 1 di data dal tempo minimo al tempo massimo
        time3 = [element for element in data[smin:len(time2),0]]            # dur contiene gli elementi della colonna 0 di data dal tempo minimo al tempo massimo

        # Utilizzato per restituire il tempo massimo del video
        
        #Confronto la scelta
        if choose == str(1) or choose == str(2):
            if choose == str(1):
                #n = interChoose()    # Restituisco il numero di intervalli selezionati
                col = []              # Creo una lista e aggiungo il valore 0

                col.append(scene[s-1])
                div = (scene[s]-scene[s-1])/len(n)  # Divido il tempo massimo per n intervalli per trovare la grandezza fissa
                div1 = div + scene[s-1]
                
                # Loop per il numero di intervalli
                for i in range(len(n)):
                    col.append(div1)                        # Aggiungo la grandezza fissa dell'intervallo nella lista
                    div1 = scene[s-1] + ((div) * (i+2))     # Sommo la grandezza fissa per se stessa
                bounds = col                                # Assegno la lista col ad una nuova lista

            elif choose == str(2):
                #n = interChoose()                                       # Restituisce il numero di intervalli selezionati
                bounds = durInter(len(n), scene[s-1], scene[s])         # Restituisce un array avente i limiti degli intervalli

            cmap = matplotlib.colors.ListedColormap(n)                  # Restituisce la lista dei colori

            norm = matplotlib.colors.BoundaryNorm(bounds, len(n))       # Resistuisce i limiti degli intervalli
            fig, ax = plt.subplots(num='Immagine %d' %s,figsize=(11, 6))
            ax.autoscale(enable=True)
            ax.imshow(img, aspect='auto')

            # Visualizzo i cerchi per ogni valore x e y, con cambio di colore in base al tempo,
            # alla lista dei colori scelti dall'utente, i limiti degli intervalli e la durata di ogni fissazione
            scatter = plt.scatter(x, y, c=time3, cmap=cmap, norm=norm, linewidths=dur)

            # Modifica della barra di colori
            cbar = plt.colorbar(scatter, spacing="proportional")
            cbar.set_label('Durata della scena (s)', rotation=270, labelpad=10)

            # Dettagli del grafico
            ax.set_aspect('equal')
            plt.xlim([0, width])
            plt.ylim([height, 0])
            plt.xlabel('Posizione X')
            plt.ylabel('Posizione Y')

            # Loop per la legenda del grafico che segna la dimensione e durata delle fissazioni
            for dur in [1.5, 3, 5]:
                plt.scatter([], [], c='k', alpha=0.3, s=dur * 50, label=str(dur) + 's')

            plt.legend(scatterpoints=1, labelspacing=1, title='Durata delle fissazioni')
            plt.axis('off')
            plt.title('Visualizzazione delle fissazioni')

            fig.set_size_inches(11, 6)
            w += 1
            fig.savefig('grafic/fixation' + str(w) + '.jpg')
            plt.show()
            s += 1
            diff = len(time2) - smin
            smin = smin + diff              #smin sarà il nuovo tempo iniziale utile per restituirmi i dati che mi serviranno

            # Svuoto le liste
            time3.clear()
            x.clear()
            y.clear()
            time2.clear()


        elif choose == str(3):

            #z.sort()
            # Dettagli del grafico
            fig, ax = plt.subplots(num='Immagine %s' %str(w+1),figsize=(11, 6))
            ax.autoscale(enable=True)
            # img = mpimg.imread('image/img' + str(charV) + '0' + str(q) + '.png')
            ax.imshow(img, aspect='auto')

            plt.scatter(x, y, c=z,vmin = minZ, vmax = maxZ, linewidths=dur)
            ax.set_aspect('equal')
            plt.xlim([0, width])
            plt.ylim([height, 0])
            plt.xlabel('Posizione X')
            plt.ylabel('Posizione Y')
            for dur in [1.5, 3, 5]:
                plt.scatter([], [], c='k', alpha=0.3, s=dur * 50, label=str(dur) + 's')

            plt.legend(scatterpoints=1, labelspacing=1, title='Durata delle fissazioni')
            plt.colorbar(label='Valore Z in millimetri\n ( Distanza tra la camera e il punto fissato )')  # Visualizzazione della barra di colori
            plt.clim(minZ, maxZ)  # Setta il minimo e massimo valore della barra di colori
            plt.axis('off')
            plt.title('Visualizzazione delle fissazioni\n  ( Gradazione del colore )')
            w += 1
            fig.savefig('grafic/fixation' + str(w) + '.jpg')
            plt.show()
            s += 1

            diff = len(time2) - smin
            smin = smin + diff
            time3.clear()
            x.clear()
            y.clear()
            time2.clear()


