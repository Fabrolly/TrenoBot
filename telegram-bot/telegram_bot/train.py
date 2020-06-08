"""
Class to model a train
"""
import os
import json
import time
from datetime import datetime, timedelta
import datetime as dt
import requests


class Train:
    """
    Class to model a train
    """

    def __init__(
        self,
        id,
        number,
        origin,
        destination,
        departure_datetime,
        arrival_datetime,
        duration,
        delay,
        state,
        last_detection_time,
        last_detection_station,
        stations,
        alert,
        last_update,
    ):
        self.id = id
        self.number = number
        self.origin = origin
        self.destination = destination
        self.departure_datetime = departure_datetime
        self.arrival_datetime = arrival_datetime
        self.duration = duration
        self.delay = delay
        self.state = state
        self.last_detection_time = last_detection_time
        self.last_detection_station = last_detection_station
        self.stations = stations
        self.alert = alert
        self.last_update = last_update

    def display(self):
        """
        Return the train as string
        """
        str = '''Id -> %s
             numero -> %s
             origine -> %s
             destinazione -> %s
             orario partenza -> %s
             orario arrivo -> %s
             durata -> %s
             RITARDO -> %s
             Stato -> %s
             ultimo rilevamento -> %s alla stazione di -> %s
             alert -> %s
             ultimo aggiornamento db -> %s"''' % (
            self.id,
            self.number,
            self.origin,
            self.destination,
            self.departure_datetime,
            self.arrival_datetime,
            self.duration,
            self.delay,
            self.state,
            self.last_detection_time,
            self.last_detection_station,
            self.alert,
            self.last_update,
        )

        print(str)

    def realTimeMsg(self):
        """
        Generate a status message from the train
        Returns:
            String with train status
        """
        self.display()
        stations = self.stationsParser()

        if self.delay >= 3 and self.delay < 15:
            delayMsg = ":warning: <b>Ritardo:</b> %s min :warning:" % (self.delay)
        elif self.delay >= 15:
            delayMsg = ":warning: <b>Ritardo:</b> %s min :red_circle:" % (self.delay)
        elif self.delay == 0:

            delayMsg = ":white_check_mark: Treno <b>in orario</b>"
        else:
            delayMsg = ":warning: <b>Anticipo</b>: %s min" % (self.delay * -1)

        if "--" in self.last_detection_station:
            msg = (
                "\t\t:bullettrain_front: <i>Treno %s</i>\n%s :arrow_right: %s\n\n<b>Ora - Bin - Stazione</b>%s\n\n:clock3: <b>Durata</b>: %s ore\n:loudspeaker: <b>Stato</b>: %s\n\n:satellite:<b>Treno NON ancora partito da %s</b>\n\n%s"
                % (
                    self.number,
                    self.origin,
                    self.destination,
                    stations,
                    self.duration,
                    self.state,
                    self.origin,
                    self.alert,
                )
            )
        else:
            msg = (
                "\t\t:bullettrain_front: <i>Treno %s</i>\n%s :arrow_right: %s\n\n<b>Ora - Bin - Stazione</b>%s\n\n:clock3: <b>Durata</b>: %s ore\n:loudspeaker: <b>Stato</b>: %s\n\n%s\n\n:satellite:<b>Ultimo rilevamento</b> %s\n:earth_africa: Presso <b>%s</b>\n\n%s"
                % (
                    self.number,
                    self.origin,
                    self.destination,
                    stations,
                    self.duration,
                    self.state,
                    delayMsg,
                    self.last_detection_time,
                    self.last_detection_station,
                    self.alert,
                )
            )

        backend = os.environ.get("HOST_BACKEND", "backend")
        train_stats = requests.get(
            # f"http://{backend}:5000/api/train/{self.number}/stats"
            f"http://{backend}:5000/api/train/{self.number}/stats?days=30"
        )
        if train_stats.status_code == 200:
            train_stats = train_stats.json()
            # delay_stats = train_stats["stats"][-30:]
            delay_stats = train_stats["stats"]
            avg_delay = [day_stats["delay"] for day_stats in delay_stats]
            if avg_delay:
                avg_delay = sum(avg_delay) / len(avg_delay)
                msg = msg + ":bar_chart: Ritardo medio 30 giorni: %d min" % avg_delay
                msg = msg + "\n⏰ Indice affidalibitá treno: %.1f " % (
                    (
                        avg_delay
                        / delay_stats[0]["duration"]
                        / delay_stats[0]["JSON_LENGTH(stations)"]
                    )
                    * -1000
                )

        return msg

    def departingMsg(self, origin, destination):
        """
        Generate a message for when the train is starting
        """
        stations = self.stationsParser()

        if self.delay >= 3 and self.delay < 15:
            delayMsg = ":warning: <b>Ritardo:</b> %s min :warning:" % (self.delay)
        elif self.delay >= 15:
            delayMsg = ":warning: <b>Ritardo:</b> %s min :red_circle:" % (self.delay)
        elif self.delay == 0:
            delayMsg = ":white_check_mark: Treno <b>in orario</b>"
        else:
            delayMsg = ":warning: <b>Anticipo</b>: %s min" % (self.delay * -1)

        if "--" in self.last_detection_station:
            msg = (
                ":bullettrain_front:Il tuo <i>Treno %s</i> dovrebbe partire <b>tra 5 minuti!</b> :running:\n\n%s :arrow_right: %s\n\n<b>Ora - Bin - Stazione</b>%s\n\n:clock3: <b>Durata</b>: %s ore\n:loudspeaker: <b>Stato</b>: %s\n\n:satellite:<b>Treno NON ancora partito da %s</b>\n\n%s"
                % (
                    self.number,
                    origin,
                    destination,
                    stations,
                    self.duration,
                    self.state,
                    self.origin,
                    self.alert,
                )
            )
        else:
            msg = (
                ":bullettrain_front:Il tuo <i>Treno %s</i> dovrebbe partire <b>tra 5 minuti!</b> :running:\n\n%s :arrow_right: %s\n\n<b>Ora - Bin - Stazione</b>%s\n\n:clock3: <b>Durata</b>: %s ore\n:loudspeaker: <b>Stato</b>: %s\n\n%s\n\n:satellite:<b>Ultimo rilevamento</b> %s\n:earth_africa: Presso <b>%s</b>\n\n%s"
                % (
                    self.number,
                    origin,
                    destination,
                    stations,
                    self.duration,
                    self.state,
                    delayMsg,
                    self.last_detection_time,
                    self.last_detection_station,
                    self.alert,
                )
            )
        return msg

    def middleMsg(self):

        stations = self.stationsParser()

        if self.delay >= 3 and self.delay < 15:
            delayMsg = ":warning: <b>Ritardo:</b> %s min :warning:" % (self.delay)
        elif self.delay >= 15:
            delayMsg = ":warning: <b>Ritardo:</b> %s min :red_circle:" % (self.delay)
        elif self.delay == 0:
            delayMsg = ":white_check_mark: Treno <b>in orario</b>"
        else:
            delayMsg = ":warning: <b>Anticipo</b>: %s min" % (self.delay * -1)

        if "--" in self.last_detection_station:
            msg = (
                ":bullettrain_front:<i>Treno %s</i> direzione %s\n\nDovresti essere a meta' viaggio!\n\n<b>Stato</b>: %s\n\n:satellite:<b>Treno NON ancora partito da %s</b>\n\n%s"
                % (self.number, self.destination, self.state, self.origin, self.alert)
            )
        else:
            msg = (
                ":bullettrain_front:<i>Treno %s</i> direzione %s\n\nDovresti essere a meta' viaggio!\n\n<b>Stato</b>: %s\n\n%s\n\n:satellite:<b>Ultimo rilevamento</b> %s\n:earth_africa: Presso <b>%s</b>\n\n%s"
                % (
                    self.number,
                    self.destination,
                    self.state,
                    delayMsg,
                    self.last_detection_time,
                    self.last_detection_station,
                    self.alert,
                )
            )
        return msg

    def stationsParser(self):
        parsed_json = json.loads(self.stations)
        nf = len(parsed_json)
        stations = ""

        for cont in range(0, nf):
            oraleggibile = dt.datetime.fromtimestamp(
                float(parsed_json[cont]["programmata"] // 1000.0)
            )

            track = parsed_json[cont]["binarioEffettivoPartenzaDescrizione"]
            if not track:
                track = parsed_json[cont]["binarioProgrammatoPartenzaDescrizione"]
                if not track:
                    track = parsed_json[cont]["binarioEffettivoArrivoDescrizione"]
                    if not track:
                        track = parsed_json[cont]["binarioProgrammatoArrivoDescrizione"]
                        if not track:
                            track = "?"

            stationName = parsed_json[cont]["stazione"]
            if self.last_detection_station in stationName:
                stationName = stationName[:20].title()
                stations += "\n%s - <b>%s</b> - %s:round_pushpin:" % (
                    oraleggibile.strftime("%H:%M"),
                    track,
                    stationName,
                )
            else:
                stationName = stationName[:20].title()
                stations += "\n%s - <b>%s</b> - %s" % (
                    oraleggibile.strftime("%H:%M"),
                    track,
                    stationName,
                )

        return stations

    def station_time(self, requested_station):

        requested_station = requested_station.upper()
        parsed_json = json.loads(self.stations)
        nf = len(parsed_json)

        for cont in range(0, nf):
            for cont in range(0, nf):
                stationName = parsed_json[cont]["stazione"].upper()
                oraleggibile = dt.datetime.fromtimestamp(
                    float(parsed_json[cont]["programmata"] // 1000.0)
                )

                if requested_station in stationName:
                    return oraleggibile, stationName

        return "Error, stazione non esistente", "Error"
