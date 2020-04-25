# Trenobot - Laboratorio di Progettazione

A Telegram Bot to monitor italian trains

## Prima dello sviluppo

Per lo sviluppo del progetto è richiesto l'IDE [VSCode](https://code.visualstudio.com/)

Estensioni di VSCode richieste per lo sviluppo:

* [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
* [Visual Studio IntelliCode](https://marketplace.visualstudio.com/items?itemName=VisualStudioExptTeam.vscodeintellicode)
* [EditorConfig](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig)

### Impostazione ambiente di sviluppo

Da eseguire la prima volta:

* Eseguire `git config core.autocrlf true`
* Posizionarsi sul branch `sprintN` ed effettuare il pull
* Installare [git-lfs](https://help.github.com/en/github/managing-large-files/installing-git-large-file-storage)
* Creare un virtual env con: `python3 -m venv venv`
* Attivare il virtual env: `source venv/bin/activate`
* Installare i pacchetti necessari al supporto allo sviluppo: `pip install -r requirements.txt`
* Eseguire lo script `.repo/setup-git-hooks.sh` per impostare l'esecuzione di script prima del commit, per formattare in automatico il codice secondo [PEP8]()
* Installare (se presenti) i file `requirements.txt` presenti nelle varie cartelle dei sottoprogetti, ad esempio `pip install -r backend/requirements.txt`
* Si e' pronti per sviluppare

### Per le volte successive

* Attivare il virtualenv con `source venv/bin/activate`

## Sviluppo

Per avviare tutta l'infrastruttura necessaria all'esecuzione del progetto e' consigliabile l'utilizzo di Docker e Docker Compose.

Per avviare tutto il progetto in sviluppo e' necessario eseguire `docker-compose -f docker-compose.yaml -f docker-compose.development.yaml up` che avvia i tutti i servizi. L'applicazione del file di deployment aggiunge un mount delle cartelle del codice dentro il docker, in modo da velocizzare lo sviluppo in caso si utilizzino framework che supportino il live-reload del codice.

Per i singoli servizi e' possibile sia eseguire manualmente il servizio o eseguire solo il docker corrispondente con: `docker-compose -f docker-compose.yaml -f docker-compose.development.yaml up NOMESERVIZIO`.

### Utilizzo di Git

#### Messaggi di commit

Leggere [questo](https://chris.beams.io/posts/git-commit/)

> * Separate subject from body with a blank line
> * Limit the subject line to 50 characters (if possible)
> * Capitalize the subject line
> * Do not end the subject line with a period
> * Use the imperative mood in the subject line (When applied this commit will... "YOUR COMMIT MESSAGE")
> * Wrap the body at 72 characters (if possible)
> * Use the body to explain what and why vs. how

#### Modello di branching

Per la gestione della repository viene utilizzato un modello di branching basato su [git flow](https://nvie.com/posts/a-successful-git-branching-model/), con un focus sul feature-branching.

* Il branch `master` contiene i commit di tutti gli sprint conclusi fino a questo momento
* I branch `sprintN` contengono i commit dello sprint N-esimo, a fine sprint il branch N-esimo viene mergiato dentro `master`
* Dal branch dello sprint corrente scaturiscono i `feature-branch` relativi alle storie del progetto che vengono mergiati nel branch dello sprint a fine feature

#### Come comportarsi al momento del merge

* Assicurarsi di essere su una `feature-branch` con `git status`
* Assicurarsi di aver committato tutti i cambimenti necessari
* `git checkout sprintN`
* `git pull origin sprintN` per scaricare tutti i cambiamenti già mergiati nel branch dello sprint
* `git checkout feature-branch`
* `git merge sprintN` per unire i cambiamenti già mergiati a quelli che si vuole mergiare ed evitare conflitti in fase di merge
* Risolvere gli eventuali conflitti
* Assicurarsi che i test di integrazione funzionino
  * `docker-compose build backend frontend telegram-bot`
  * `docker-compose run --rm NOME_SERVIZIO ./wait-for.sh database:3306 -- python -m unittest discover NOME_SERVIZIO/tests_integration/`

* `git push origin feature-branch`
* Una volta portata a termine la storia/quando si vuole creare la merge request (non è necessario farlo all'ultimo momento)
  * Andare sulla pagina [Issues](https://gitlab.com/laboratorio-di-progettazione-trenobot/trenobot-laboratorio-di-progettazione/-/issues) ed assicurarsi che la propria branch/feature abbia una issue dedicata
  * Andare sulla pagina delle [Merge Request](https://gitlab.com/laboratorio-di-progettazione-trenobot/trenobot-laboratorio-di-progettazione/-/merge_requests) e creare la merge request
  * Attendere la code-review e l'approvazione di almeno un collega
  * Effettuare il merge una volta risolti tutti i problemi segnalati dai colleghi

### Scrittura dei test

Per la scrittura dei test è necessario utilizzare il framework di testing [`unittest`](https://docs.python.org/3/library/unittest.html).

Si deve dare la priorità ai test di unità e solo in seguito a quelli di integrazione. Ciascuna parte del sistema deve essere testabile da sola, senza la necessità che le altre funzionino.


## Pipeline

La pipeline che realizza la CI per il progetto si occupa delle seguenti task:

* Pre-test:
  * Controlla che il codice sia correttamente formattato
  * Esegue il build di tutte le immagini docker e le pusha con il tag `test`
* Test
  * In ciascuna immagine docker di test esegue i test di unità
* Build:
  * Ritagga le immagini con `$COMMIT_SHA` e le pusha
  * Utile per un eventuale server di development
* Release:
  * Eseguito solo in caso di commit su `sprintN` o `master`, tagga le immagini con il nome del branch
  * Utile per un eventuale server di staging
