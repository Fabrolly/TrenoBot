# High Level Architecture

## Backend
Il backend é formato da delle API che estrapolano le informazioni relative ai treni per fornirle al gestore del bot telegram. 
Comprende dei database, alcuni ad uso del bot per la gestione utente, altri dedicati alla raccolta dati e per la gestione della cache.
Tutto il backend va organizzato in container per assicurare, come richiesto, portabilitá e affidabilitá del servizio.

Database: MariaDb
Conteinerizzazione: Docker

![Esistente DB](https://i.ibb.co/1K2p0jr/Schermata-2020-03-18-alle-11-40-11.png)

## Frontend - Bot Telegram
Il bot si serve del backend per personalizzare l'esperienza utente e fornire i dati che esso richiede.

Libreria: Telepot

## Frontend - Sito web raccolta dati
Esegue una elaborazione grafica dei dati raccolti dalle API del backend che esso conserva in un DB dedicato.