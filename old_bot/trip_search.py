import datetime
import time
import urllib.request, urllib.parse, urllib.error
import json
import telepot
from emoji import emojize
import buttons

# import loginInfo

# TOKEN = loginInfo.telegramKey()
with open('token.txt', 'r') as content_file:
        TOKEN = content_file.read()
bot = telepot.Bot(TOKEN)


def trip_search(command, arrivo, partenza, mese, giorno, ora, data, now, chat_id):

    # Creo url per la richiesta del CODICE DELLE STAZIONI e interrogo
    urlPartenza = (
        "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/autocompletaStazione/%s"
        % partenza
    )
    urlArrivo = (
        "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/autocompletaStazione/%s"
        % arrivo
    )
    # Interrogo per ottenere il codice della stazione di PARTENZA
    CodiceStazionePartenza = urllib.request.urlopen(urlPartenza).read().decode("utf-8")

    if CodiceStazionePartenza == "":
        return (
            "Stazione di <b>PARTENZA</b> non esistente.\n\n<b>CONSIGLI:</b>\n-Prova a scrivere solo le <b>prime parole chiave</b>, non il nome completo!\n\n-Oppure prova a scrivere il <b>nome completo!</b>\nEsempio: Milano Porta Garibaldi",
            "",
        )
    else:
        NomeCompletoStazionePartenza = CodiceStazionePartenza[
            : CodiceStazionePartenza.index("|")
        ]
        if "\n" in CodiceStazionePartenza:
            CodiceStazionePartenza = CodiceStazionePartenza[
                CodiceStazionePartenza.index("|")
                + 2 : CodiceStazionePartenza.index("\n")
            ]
        else:
            CodiceStazionePartenza = CodiceStazionePartenza[
                CodiceStazionePartenza.index("|") + 2 :
            ]

        while CodiceStazionePartenza[0] == "0":
            CodiceStazionePartenza = CodiceStazionePartenza[1:]

    # Interrogo per ottenere il codice della stazione di ARRIVO
    CodiceStazioneArrivo = urllib.request.urlopen(urlArrivo).read().decode("utf-8")

    if CodiceStazioneArrivo == "":
        return (
            "Errore\n\n-Prova a scrivere solo le <b>prime parole chiave</b>, non il nome completo!\nEsempio:\nMilano Porta\n\n-Oppure prova a scrivere il <b>nome completo!</b>\nEsempio: Milano Porta Garibaldi\n\n-Se il nome della stazione comprende piu' parole <b>usa i connettivi 'da' e 'a'</b> come in questo formato:\nDa Milano Centrale a Reggio Calabria\n\n<b>Esempi Corretti:</b>\n<i>Da Roma a Milano\nDa Roma a Milano il 10-8\nDa Roma a Milano alle 20:00\nDa Roma Tiburtina a Milano Lambrate il 10-8 alle 12:30\n</i>",
            "",
        )
    else:
        NomeCompletoStazioneArrivo = CodiceStazioneArrivo[
            : CodiceStazioneArrivo.index("|")
        ]
        if "\n" in CodiceStazioneArrivo:
            CodiceStazioneArrivo = CodiceStazioneArrivo[
                CodiceStazioneArrivo.index("|") + 2 : CodiceStazioneArrivo.index("\n")
            ]
        else:
            CodiceStazioneArrivo = CodiceStazioneArrivo[
                CodiceStazioneArrivo.index("|") + 2 :
            ]
        while CodiceStazioneArrivo[0] == "0":
            CodiceStazioneArrivo = CodiceStazioneArrivo[1:]

    # Interrogo con codici delle stazioni di partenza e ritorno e data e ora CODICEPARTENZA/CODICEARRIVO/AAA-MM-GGTHH:MM:SS occhio alla T che separa data e ora
    DataOra = "%s-%s-%sT%s:00:00" % (now.year, mese, giorno, ora)
    urlRicerca = (
        "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/soluzioniViaggioNew/%s/%s/%s"
        % (CodiceStazionePartenza, CodiceStazioneArrivo, DataOra)
    )
    print(urlRicerca)
    # bot.sendMessage(chat_id, 'UrlRicerca: %s' %(urlRicerca))
    parsed_json = json.loads(urllib.request.urlopen(urlRicerca).read().decode("utf-8"))
    try:
        for sol in range(0, 2):  # ciclo che fa visualizzare le prime 2 opzioni
            risp = ""
            trains = []
            departure_time_keyboard = []
            arrival_time_keyboard = []
            departure = []
            arrival = []
            for cont in range(
                0, len(parsed_json["soluzioni"][sol]["vehicles"])
            ):  # ciclo che crea il messaggio per quando la soluzione ha piu treni
                departure_time = parsed_json["soluzioni"][sol]["vehicles"][cont][
                    "orarioPartenza"
                ]
                departure_day = departure_time[
                    departure_time.index("T") - 2 : departure_time.index("T")
                ]
                departure_month = departure_time[departure_time.index("-") + 1 :]
                departure_month = departure_month[: departure_time.index("-") - 2]
                departure_time = departure_time[
                    departure_time.index("T") + 1 : departure_time.index("T") + 6
                ]
                arrival_time = parsed_json["soluzioni"][sol]["vehicles"][cont][
                    "orarioArrivo"
                ]
                arrival_time = arrival_time[
                    arrival_time.index("T") + 1 : arrival_time.index("T") + 6
                ]

                # keyboard generate

                trains.append(
                    parsed_json["soluzioni"][sol]["vehicles"][cont]["numeroTreno"]
                )
                departure.append(
                    parsed_json["soluzioni"][sol]["vehicles"][cont]["origine"]
                )
                arrival.append(
                    parsed_json["soluzioni"][sol]["vehicles"][cont]["destinazione"]
                )
                departure_time_keyboard.append(departure_time)
                arrival_time_keyboard.append(arrival_time)

                # appendo i vari treni della soluzione in coda al messaggio di risposta
                risp += (
                    ":train2: Treno %s %s\n:arrow_right: <b>%s</b> da %s\n:arrow_left: <b>%s</b> a %s\n\n"
                    % (
                        parsed_json["soluzioni"][sol]["vehicles"][cont][
                            "categoriaDescrizione"
                        ],
                        parsed_json["soluzioni"][sol]["vehicles"][cont]["numeroTreno"],
                        departure_time,
                        parsed_json["soluzioni"][sol]["vehicles"][cont]["origine"],
                        arrival_time,
                        parsed_json["soluzioni"][sol]["vehicles"][cont]["destinazione"],
                    )
                )
            response = risp = (
                ":white_check_mark:<b>Soluzione %s</b>\n\n:calendar: %s-%s-%s\n:clock10:Durata <b>%s</b>\n\n%s"
                % (
                    sol + 1,
                    departure_day,
                    departure_month,
                    now.year,
                    parsed_json["soluzioni"][sol]["durata"],
                    risp,
                )
            )

            keyboard = buttons.searchResultMenuButtons(
                chat_id,
                trains,
                departure_time_keyboard,
                arrival_time_keyboard,
                departure,
                arrival,
            )
            bot.sendMessage(
                chat_id,
                emojize(response, use_aliases=True),
                parse_mode="html",
                disable_web_page_preview=None,
                disable_notification=None,
                reply_markup=keyboard,
            )
    except Exception as e:
        print(e)
        keyboard = buttons.backMainMenuButtons()
        bot.sendMessage(
            chat_id,
            emojize(
                "Le API di viaggiotreno non sono in grado di rispondere a questa richeiesta anche se il tuo comando e' valido.\n\nIl motivo e' sconosciuto e da attributire a viaggiatreno.it\n\nCerca qui il tuo treno: http://www.trenitalia.com/ \n\nQuando sai il numero del tuo treno torna qui!",
                use_aliases=True,
            ),
            parse_mode="html",
            disable_web_page_preview=None,
            disable_notification=None,
            reply_markup=keyboard,
        )


def date_parser(command):

    now = datetime.datetime.now()

    output = ""

    if "-" not in command and "/" not in command:
        output = "%s-%s" % (command, now.month)
    else:
        if "/" in command:
            output = command.replace("/", "-")
        else:
            output = command

    if command == "":
        output = "%s-%s" % (now.day, now.month)

    giorno = output[: output.index("-")]
    mese = output[output.index("-") + 1 :]
    if int(giorno) > 31:
        # il Giorno inserito e' inesistente. Verra' utilizzato il GIORNO ODIERNO
        output = "%s-%s" % (now.day, now.month)

    if int(mese) > 12:
        return (
            "Attenzione, il Mese inserito e' inesistente.\n\\nMese ricevuto = %s\n\nVerra' utilizzato il MESE ODIERNO"
            % (mese),
            "",
        )

    return output
