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

* Creare un virtual env con: `python3 -m venv venv`
* Attivare il virtual env: `source venv/bin/activate`
* Installare i pacchetti necessari al supporto allo sviluppo: `pip install -r requirements.txt`
* Eseguire lo script `.repo/setup-git-hooks.sh` per impostare l'esecuzione di script prima del commit, per formattare in automatico il codice secondo [PEP8]()
* Installare (se presenti) i file `requirements.txt` presenti nelle varie cartelle dei sottoprogetti, ad esempio `pip install -r backend/requirements.txt`
* Si e' pronti per sviluppare

### Per le volte successive

* Attivare il virtualenv con `source venv/bin/activate`

### Modello di branching

Per la gestione della repository viene utilizzato un modello di branching basato su [git flow](https://nvie.com/posts/a-successful-git-branching-model/), con un focus sul feature-branching.

* Il branch `master` contiene i commit di tutti gli sprint conclusi fino a questo momento
* I branch `sprintN` contengono i commit dello sprint N-esimo, a fine sprint il branch N-esimo viene mergiato dentro `master`
* Dal branch dello sprint corrente scaturiscono i `feature-branch` relativi alle storie del progetto che vengono mergiati nel branch dello sprint a fine feature
