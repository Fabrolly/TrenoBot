# High Level Architecture

L'applicazione é formata da un backend eseguito su piattafroma cloud che gestisce la raccolta dati tramite database persistenti e li fornisce al bot telegram e al sito web tramite **API rest HTTP**.


*  **Piattaforma Cloud**: Google Cloud Engine

![High Level Architecture schema](https://gitlab.com/laboratorio-di-progettazione-trenobot/trenobot-laboratorio-di-progettazione/-/raw/master/Documents/Resources/High%20Level%20Architecture%20Schema.png)


## Backend - API trenitalia e DB persistenti
Il backend é formato da delle API che estrapolano le informazioni relative ai treni dai siti ufficiali di trenitalia.
Comprende dei database, alcuni ad uso del bot per la gestione utente, altri dedicati alla raccolta dati del sito web delle statistiche e per la gestione della cache.
Tutto il backend va organizzato in container per assicurare, come richiesto, portabilitá e affidabilitá del servizio.

* **Database**: MariaDb
* **Conteinerizzazione**: Docker

Architettura DB pre-esistente ad uso del bot telegram e del backend: https://i.ibb.co/1K2p0jr/Schermata-2020-03-18-alle-11-40-11.png

## Frontend - Sito web visualizzazione statistiche
Esegue una elaborazione grafica dei dati raccolti dalle API del backend che esso conserva in un DB dedicato.

* **Framework web**: [Bootstrap](https://getbootstrap.com/)
* **JavaScript charts**: [Chart.js](https://www.chartjs.org/)


## Frontend - TrenoBot, bot Telegram
Il bot si serve del backend per personalizzare l'esperienza utente e fornire i dati che esso richiede.

* **Framework Telegram**: [Telepot](https://telepot.readthedocs.io/en/latest/)
* **Interfacciamento con Database**: [MySQLdb](https://www.python.it/doc/articoli/mysqldb/mysqldb-3.html)
* **Interfaccia per accedere a risorse di rete**: [urlib](https://docs.python.org/3/library/urllib.html)
* **Libreria per gestire file JSON**: [json](https://docs.python.org/3/library/json.html)

Documentazione pre-esistente del bot telegram: https://github.com/Fabrolly/TrenoBot



