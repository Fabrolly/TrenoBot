import urllib
import json


#request the Station_ID of the train by the number of the train. 
#For the requets both the Number and Station_ID are necessary for the query. Then i must have the Statation_ID from the number given by user
def trainId(train_number):
    try:
        autocomplete=urllib.urlopen('http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/%s' % train_number).read();
    except Exception,e:
        return 'error' # probably the trenitalia API are offline. I must handle this situation


    if(len(autocomplete)!=0 and '<H1>' not in autocomplete):
        if('-' in autocomplete): #this thing is necessary because for some reasons there are train with the same number but different station_ID.
             autocomplete=autocomplete[(autocomplete.index('|')+1):]
             autocomplete=autocomplete[(autocomplete.index('-')+1):(autocomplete.index('\n'))]
             return autocomplete #return the ID of the train
        else:
            return 'error'

#return the JSON containing all the real time information of a train, by it's number 
def realTimeInformation(number):
    try:
        idTrain=trainId(number) #I need also the Station_ID for the request
        if 'error' in idTrain:
            return '', '', 'error'
        url='%s/%s'%(idTrain, number) #See api docs: the request urls is composed by TRAIN_ID/TRAIN_NUMBER
        raw_json= urllib.urlopen('http://www.viaggiatreno.it/viaggiatrenomobile/resteasy/viaggiatreno/andamentoTreno/%s' % url).read()
        parsed_json = json.loads(raw_json)
        return parsed_json, raw_json, idTrain
    except Exception,e:
        return '', '', 'error'
