# Pipeline & Deployment

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
  * Effettua il build e il publish della documentazione tecnica

## Deployment

Per ora non è stata predisposto alcun deployment automatico.

Per deployare il software è necessario clonare la repository sul server ed eseguire:

```
docker-compose build backend stats_website telegram-bot
docker-compose stop backend stats_website telegram-bot
docker-compose rm backend stats_website telegram-bot
docker-compose up -d backend stats_website telegram-bot
```
