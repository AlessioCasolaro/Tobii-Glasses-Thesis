##############################################################################
# Progetto di tesi sul dispositivo Tobii Pro Glasses 3
# Realizzato da Alessio Casolaro, Giulio Triggiani
#
# Relatori Prof.Andrea Francesco Abate, Dott.ssa Lucia Cimmino, Dott.ssa Lucia Cascone 
##############################################################################
from sys import path
import PySimpleGUI as sg
import os

from numpy.core.fromnumeric import choose
from readVideo import *
from readDataGaze import *
from aoi import *
from barGrafic import *
from scanpath import *
from blinkDetection import *
from heatmap import *
from online import *

def main():
    ##############################################################################
    #Costruisco il Layout di sinistra
    file_list_column = [
        [
            sg.Text("Cartella video:"),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse("Seleziona"),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
            )
        ],
    ]

    ##############################################################################
    strFun = '''
            1. Creazione/Visualizzazione del file pupil.csv
            2. Creazione/Visualizzazione dei grafici delle fissazioni
            3. Creazione del file aoi.csv e visualizzazione dei grafici
            4. Visualizzazione dei grafici a barre
            5. Creazione/Visualizzazione dei file fixation.csv
            6. Disegna Scanpath
            7. Creazione del file blinkDetected.csv
            8. Generazione grafico Blink in intervallo di tempo
            9. Creazione Heatmap
            10.Scanpath Real-time
            '''


    #Costruisco il Layout di destra
    right_viewer_column = [
        [sg.Text("Video scelto:")],
        [sg.Text(size=(40, 1), key="-TEXTVIDEONAME-")],
        [sg.Text("Scegli che funzione eseguire:")],
        [sg.Text(strFun)],
        [sg.Image(key="-IMAGE-")],

        [sg.Button("Funzione 1", key="-KEY1-",size=(10,1)),
        sg.Button("Funzione 2", key="-KEY2-",size=(10,1)),
        sg.Button("Funzione 3", key="-KEY3-",size=(10,1)),
        sg.Button("Funzione 4", key="-KEY4-",size=(10,1))],

        [sg.Button("Funzione 5", key="-KEY5-",size=(10,1)),
        sg.Button("Funzione 6", key="-KEY6-",size=(10,1)),
        sg.Button("Funzione 7", key="-KEY7-",size=(10,1)),
        sg.Button("Funzione 8", key="-KEY8-",size=(10,1))],

        [sg.Button("Funzione 9", key="-KEY9-",size=(10,1)),
        sg.Button("Funzione 10", key="-KEY10-",size=(10,1))
        ],
    
    ]

    ##############################################################################
    #Costruisco il Layout Globale
    layout = [
        [
            sg.Column(file_list_column),#Colonna di sinistra
            sg.VSeperator(),#Separatore
            sg.Column(right_viewer_column),#Colonna di destra
        ], 
        [sg.Button("Riproduci Video", key="-APRI-")]
    ]

    window = sg.Window("Tobii Pro Glasses 3 - Controller", layout)#Assegno il nome alla finestra

    ##############################################################################
  
    while True:
        event, values = window.read()#Leggo gli eventi
        if event == sg.WIN_CLOSED:#Se l'utente chiude la finestra, break
            break
        # Se la cartella è stata scelta, fai una lista con tutti i file video
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            try:
                # Prende la lista di tutti i file nella cartella
                file_list = os.listdir(folder)
            except:
                file_list = []
            #Filtra i file lasciando solo i video
            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".mp4"))
            ]
            window["-FILE LIST-"].update(fnames)#Inserisce i file video nella lista

        elif event == "-FILE LIST-":  # Se un file è stato scelto dalla lista
            #Salvo il path del video selezionato
            pathVideo = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                )
            nameVideo = os.path.basename(pathVideo)#Salvo il nome del video selezionato

            # Divide il nome del video e il suo formato
            strSplit = nameVideo.split('.')
            Numb = ''.join((ch if ch in '0123456789' else ' ') for ch in strSplit[0])
            strNumb =[int(i) for i in Numb.split()]
            strNumb.reverse()
            char = strNumb[0]#Numero video selezionato

        
            window["-TEXTVIDEONAME-"].update(nameVideo)#Scrivo il nome del video  nella colonna di destra
            event, values = window.read()#Rileggo gli eventi
            if event == "-APRI-":#Se è stato premuto il tasto apri, apro il video
                resImage(nameVideo, char)
                streamVideo(nameVideo)

            elif event == "-KEY1-":#Creazione/Visualizzazione del file pupil.csv
                print("Visualizzazione e creazione del file pupil.csv")
                print(pathVideo)
                print(nameVideo)
                readData(char)
                pupilTableViewer(path = "out/pupil.csv",pathStats = "out/pupilsStatistics.csv")
            
            elif event == "-KEY2-":#Creazione/Visualizzazione dei grafici delle fissazioni
                graficFix(char,durEachScen(char))
            
            elif event == "-KEY3-": #AOI
                print("Una area di interesse o AOI è una regione dele fissazioni identiche, per identiche intendiamo piccole distanze tra di loro nello spazio ) "
                            "ed viene utilizzata per estrarre metriche specifiche per quella regione. ")
                choose = sg.popup_get_text(message='''Quale algoritmo vuoi eseguire per generare le aree di interesse?
                                            1. K-means Clustering
                                            2. DBscan clustering
                                            ''',title="AOI")
                chooseAlgo(durEachScen(char),choose)
                if choose == "2":#Se stato scelto DBScan stampa anche la tabella
                    tableViewer(path = "out/aoi.csv")

            elif event == "-KEY4-": #Visualizzazione dei grafici a barre
                chooseGraph(char,durEachScen(char))

            elif event == "-KEY5-": #Creazione/Visualizzazione dei file fixation.csv
                readData(char)
                tableViewer(path = "out/fixation.csv")

            elif event == "-KEY6-": #Disegna Scanpath
                generateScanpath(pathVideo)

            elif event == "-KEY7-": #Creazione del file blinkDetected.csv
                blinkDetect()
                tableViewer(path = "out/blinkDetected.csv")

            elif event == "-KEY8-": #Generazione grafico Blink in intervallo di tempo
                min = sg.popup_get_text(message="Inserisci l'intervallo di tempo inferiore" ,title="Grafico Blink")
                sup = sg.popup_get_text(message="Inserisci l'intervallo di tempo superiore" ,title="Grafico Blink")
                blinkGrafics(min, sup)

            elif event == "-KEY9-":#Creazione Heatmap
                print("Generazione Frame per Heatmap")
                extractMiddleFrame(pathVideo)
                print("Generazione Heatmap")
                draw_heatmap()

            elif event == "-KEY10-":#Apertura streaming video
                streaming()
        
    window.close()


def pupilTableViewer(path,pathStats): 
        #Popola la tabella con i dati
        data = []
        header_list = []
        if path is not None:#Controlla se il path del file pupil.csv è corretto
            try:
                df = pd.read_csv(path, sep=',', engine='python', header=None)
                data = df.values.tolist() # Converte tutti i dati in una lista
                
                # La prima riga rappresenta l'header del file csv
                header_list = df.iloc[0].tolist()
                # Dopo la prima riga le altre sono semplici righe
                data = df[1:].values.tolist()
                
            except:
                sg.popup_error('Errore lettura file pupil.csv')

        if pathStats is not None:
            try:
                df2 = pd.read_csv(pathStats, sep=',', engine='python', header=None)
                data2 = df2.values.tolist()               
            
                header_list2 = df2.iloc[0].tolist()
                
                data2 = df2[1:].values.tolist()
                
            except:
                sg.popup_error('Errore lettura file pupilsStatistics.csv')
                

        layout = [
            [sg.Text("Statistiche pupille:")],
            [sg.Table(values=data2,
                    headings=header_list2,
                    display_row_numbers=True,
                    auto_size_columns=True,
                    hide_vertical_scroll=True,
                    vertical_scroll_only=False,
                    num_rows=2)],
            [sg.Text("Tabella informazioni pupille:")],
            [sg.Table(values=data,
                    headings=header_list,
                    display_row_numbers=True,
                    auto_size_columns=True,
                    num_rows=min(25, len(data)))]
        ]

        window = sg.Window('Tabelle Informazioni Pupilla', layout, grab_anywhere=False,element_justification='c',size=(800,600))
        event, values = window.read()



def tableViewer(path): 
        data = []
        header_list = []
        
        if path is not None:#Controlla se il path del file .csv è corretto
            try:
                df = pd.read_csv(path, sep=',', engine='python', header=None)
                data = df.values.tolist() # Converte tutti i dati in una lista
                
                # La prima riga rappresenta l'header del file csv
                header_list = df.iloc[0].tolist()
                # Dopo la prima riga le altre sono semplici righe
                data = df[1:].values.tolist()

            except:
                sg.popup_error('Errore lettura file')
                

        layout = [
            [sg.Table(values=data,
                    headings=header_list,
                    display_row_numbers=True,
                    auto_size_columns=True,
                    num_rows=min(25, len(data)))]
        ]

        window = sg.Window('Tabella Informazioni', layout, grab_anywhere=False,element_justification='c')
        event, values = window.read()



if __name__ == '__main__':
    main()