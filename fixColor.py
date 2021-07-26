# Funzione per settare i colori, ha come paramentro un int
def setColor(color):

    if color == 1:
        c = 'red'
    elif color == 2:
        c = 'blue'
    elif color == 3:
        c = 'yellow'
    elif color == 4:
        c = 'green'
    else:
        c = 'black'
    print("Hai scelto il colore: ",c)

    return c


# Funzione che restituisce i colori di ogni intervallo
def interChoose():
    # L'utente deve inserire il numero di intervalli che vuole creare
    n = int(input("Quanti intervalli(max 5): "))
    print('''Colori nell'elenco:
        1. Red
        2. Blue
        3. Yellow
        4. Green
        5. Black
        ''')

    col = []                                    # Lista di colori
    # Loop del numero di intervalli per settare il colore ad ogni intervallo
    for i in range(n):
        color = int(input("Setta il colore per %s intervallo: " % (i+1)))
        col.append(setColor(color))             # Aggiungo il colore alla lista dei colori
    return col


# Funzione che restituisce i limiti di ogni intervallo, passo per paramentro il numero di intervalli e il tempo massimo del video
def durInter(num,time, scene):

    listInter = []                                  # Lista dei limiti degli intervalli
    listInter.append(time)                          # Aggiungo il primo limite alla lista
    for i in range(num):
        print("Scegli tra %s e  %s:" %(listInter[i], scene))

        # Controllo se è l'ultima iterazione
        # Se è l'ultima allora restituisco nella variable help1 il tempo massimo
        # Altrimenti l'utente digita il limite dell' intervallo per ogni i-esimo intervallo
        if i == num-1:
            help1 = scene
        else:
            while(True):
                help1 = float(input("Digita: "))
                if help1 >= listInter[i] and help1 <= scene:
                    break
                else:
                    print("Numero inserito non valido")
        listInter.append(help1)                       # Aggiungo il numero nella lista

    return listInter