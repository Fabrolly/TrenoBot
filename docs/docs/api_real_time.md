# Trenitalia Real Time Data

## Before starting
I will be brief: there are no public APIs for any Italian railway company.
This, in my opinion, is a very bad thing: a public service should expose the API to develop third-party app.

## Where the TrenoBot data comes from

When I started to develop this project the first question was where to catch the information about italian trains.
I try with the official site of trenitalia, but it doesn't contain real time information (only allows train searches).
I found a site of trenitalia (www.viaggiatreno.it) that allows to view real-time information about all trains in the Italian territory, including those of other companies like Trenord.

It's exactly what I was looking for!

## Getting the APIs from viaggiatreno.it

As mentioned before, there is no public documentation for these APIs. So the answer to this chapter is: going to attempts.
I used the Google Chrome development console by simulating the search for some trains and analyzing the site's requests by intercepting some JSON files that were returned.

### Find the Station_ID for identify a train
![](https://i.imgur.com/Oksw49d.png)

For example, I look for the train with number "5040". It is a regional train that goes from Bergamo to Lecco.
As you can see in the Google Chrome development Console on the right, there are 2 files very interting called both "5040" (...).

However, the first one contains the start station ID which is a different code than the train number. I have no idea why the train number (which is unique) is not sufficient to identify the train. Each train has a unique number that is progressive! But, for unknown reasons, the start station ID is also associated with each train.

Example:
* Bergamo - Lecco ->5040-S01529
* Lecco - Bergamo ->5041-S01520
* Bergamo - Lecco ->5042-S01529
* Lecco - Bergamo ->5043-S01520
* Bergamo - Lecco ->5044-S01529

In fact, at each request the train number is passed to this url: http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/TRAIN_NUMBER which returns the station ID of the 5040 train.

In our example the answer to the number 5040 is this:
![](https://i.imgur.com/Df1g6Hb.png)
What we need to preceed is the string 'S01529'. This will be the necessary code (station id) to identify our train in the next step.

Now we have everything we need:
* The train number (put by us) -> 5040
* Id of the train reference station -> S01529

### Retrive real time information

If you remember the first image we said that there are two '5040' files. The first is used to retrieve the id of the reference station and the second is to have (finally) all the necessary information on that train.

Let's start by the url of this second 5040 file: http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/S01529/5040

As you can see the part that interests us is composed by: '....S01529/5040'

So we can conclude that the syntax of this url is:
http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/STATION_ID/TRAIN_ID

Where station ID is the code we have previously recovered.

Well, finally we are there. We have what we want:
![alt text](https://i.imgur.com/SxGOLIP.jpg)

I could spend hours writing a poem about how badly this JSON file is:
* There are some terrible things, such as the fields called "nextTrattaType" and "nextFermataType" a mix between Italian and English.
* Many fields (I'm very sure after 2 years of testing) are always NULL and are useless.
* ....

Anyway, let's go ahead and see which JSON fields I use in TrenoBot:

* ['numeroTreno']
* ['origineZero']
* ['destinazioneZero']
* ['orarioPartenza']
* ['orarioArrivo']
* ['compTipologiaTreno']
* ['compDurata']
* ['oraUltimoRilevamento']
* ['stazioneUltimoRilevamento']
* ['subTitle']
* ['ritardo']
* ['provvedimento']
* ['fermate']

The last one contains all the train stops, and for each stop we have the following information:

<img src="https://i.imgur.com/6bLchWP.png" width="500">

(I parsed it to have a better readability)

The times are in TIMESTAMP (must be converted). Many fields are NULL and unused.
We can see the binary number, delay and other useful information from these fields. 'Fermate' is an array that contains this information for each station: so for regional trains with many stops, this JSON is very long.

## Python Implementation

I don't think many explanations are needed for this (temporary) code. However it's better to see the real file in the TrenoBot Application folder (here on git).

```
#request the Station_ID of the train by the number of the train.
#For the requets both the Number and Station_ID are necessary for the query. Then i must have the Statation_ID from the number given by user
def trainId(train_number):
    try:
       autocomplete=urllib.urlopen('http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/%s' % train_number).read();
    except Exception,e:
        print e #TODO: probably the trenitalia API are offline. I must handle this situation

    if(len(autocomplete)!=0):
             autocomplete=autocomplete[(autocomplete.index('-')+1):(autocomplete.index('\n'))]
             return autocomplete #return the ID of the train
        else:
            return 0  #TODO: i must handle this situation



#return the JSON containing all the real time information of a train, by it's number
def realTimeInformation(number):
    try:
        idTrain=trainId(number) #I need also the Station_ID for the request
        url='%s/%s'%(idTrain, number) #See api docs: the request urls is composed by TRAIN_ID/TRAIN_NUMBER
        raw_json= urllib.urlopen('http://www.viaggiatreno.it/viaggiatrenomobile/resteasy/viaggiatreno/andamentoTreno/%s' % url).read()
        parsed_json = json.loads(raw_json)
        return parsed_json, raw_json
    except Exception,e:
        print e     #TODO: i must handle this situation
  ```


## Parsing the JSON

There is not much to explain regarding the parsing: the python file in the Application folder is easy to understand: I simply take the JSON fields that interest me and enter them in my local database (see the database documentation).

If the record in my database does not exist or is too old, I update it by making the request to viaggiatreno as we see above. Otherwise I provide the user with the information I already have locally in the DB.

To work with JSON in python I use the JSON library and the instruction `parsed_json = json.loads(raw_json)` for deserialize JSON and make it compatible with simple python syntax.

There is a simple conversion table for deserialization:

<img src="https://i.imgur.com/ht85oa0.png" width="280">

I still keep a copy of the original JSON (which I call raw_json) for the 'fermate' field that I insert in the database in the original format, since parsed_json, obvusly, is no longer a valid json format.
