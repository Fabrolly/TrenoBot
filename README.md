# Trenobot - Laboratorio di Progettazione

A Telegram Bot to monitor italian trains

## Sviluppo

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

## Utilizzo di Git

### Messaggi di commit

Leggere [questo](https://chris.beams.io/posts/git-commit/)

> * Separate subject from body with a blank line
> * Limit the subject line to 50 characters (if possible)
> * Capitalize the subject line
> * Do not end the subject line with a period
> * Use the imperative mood in the subject line (When applied this commit will... "YOUR COMMIT MESSAGE")
> * Wrap the body at 72 characters (if possible)
> * Use the body to explain what and why vs. how

### Modello di branching

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
* `git push origin feature-branch`
* Una volta portata a termine la storia/quando si vuole creare la merge request (non è necessario farlo all'ultimo momento)
  * Andare sulla pagina [Issues](https://gitlab.com/laboratorio-di-progettazione-trenobot/trenobot-laboratorio-di-progettazione/-/issues) ed assicurarsi che la propria branch/feature abbia una issue dedicata
  * Andare sulla pagina delle [Merge Request](https://gitlab.com/laboratorio-di-progettazione-trenobot/trenobot-laboratorio-di-progettazione/-/merge_requests) e creare la merge request
  * Attendere la code-review e l'approvazione di almeno un collega
  * Effettuare il merge una volta risolti tutti i problemi segnalati dai colleghi
