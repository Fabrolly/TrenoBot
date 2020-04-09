import buttons


def mainMenu():
    mess = (
        ":house: <b>Menu' Principale</b>\n\nScegli l'operazione che desideri effettuare"
    )
    keyboard = buttons.mainMenuButtons()

    return (mess, keyboard)


def realTimeMenu():
    mess = ":train2: <b>Visualizza lo stato di un Treno in tempo reale</b>\n\nTi basta scrivere il numero del tuo treno come l'esempio che segue:\n\n<i>Treno 5050</i>\n\n"
    keyboard = buttons.trainMenuButtons()

    return (mess, keyboard)


def searchMenu():
    mess = ":eyes: <b>Cerca una soluzione di viaggio!</b>\n\n<b>Per esempio</b> per cercare da <b>Milano</b> a <b>Roma</b>:\n\n<i>Ricerca da Milano a Roma\nRicerca da Milano a Roma alle 20:30\nRicerca da Milano a Roma alle 20:30 il 10-2</i>\n\n:exclamation: Se ometti la data o l'ora viene considerata la data/ora attuale."
    keyboard = buttons.searchMenuButtons()

    return (mess, keyboard)


def addListMenu():
    mess = ":eyes: <b>Aggiungi un treno alla tua Lista!</b>\n\nVerrai aggiornato automaticamente sui ritardi, cancellazioni, modifiche e binari del tuo treno!\n\n<b>Esempio</b>\nper aggiungere il treno <b>35091</b>, puoi scrivere:\n\n<i>Programma 35091\nProgramma 35091 da Piacenza a Parma\nProgramma 35091 lunedi venerdi</i>\n\n:exclamation: Se ometti i giorni della settimana viene considerato da Lunedi' a Venerdi'.\n:exclamation: Se ometti le stazioni intermedie viene considerata l'intera tratta"
    keyboard = buttons.searchMenuButtons()

    return (mess, keyboard)


def directressAddMenu():
    mess = ":eyes: <b>Aggiungi una Direttrice Trenord alla tua Lista!</b>\n\n<i>Quando trenord pubblica un tweet o un avviso relativo a delle problematiche su una direttrice verrai immediatamente avvisato!</i>\n\nIndividua la tua direttrice nell'elenco qui sopra."
    mess += "\n\n<b>Per aggiungere una direttrice, scrivi:\n</b> <i>'Direttrice Numero'</i>\n\n<b>Esempio:</b>\n<i>Direttrice 1</i>"
    keyboard = buttons.trenordAlertMenu()
    return (mess, keyboard)


def programMenu():
    mess = "<b>Con Trenobot puoi tenere monitorato un treno e ricevere avvisi prima e durante la sua corsa.</b>\n\nTerro' monitorato il tuo treno a partire da 30 minuti prima della partenza fino a quando non sarai arrivato.\n\nIn caso di problemi e poco prima della partenza, ti avvisero' sui binari e sui dettagli degli eventuali disagi.\n\n<i>Usa il menu' qui sotto per aggiungere un treno, oppure per visualizzare quelli gia' monitorati.</i>"
    keyboard = buttons.programMenuButtons()

    return (mess, keyboard)
