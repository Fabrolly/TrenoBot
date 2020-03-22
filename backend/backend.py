from flask import Flask, request, jsonify, abort
import requests

app = Flask(__name__)

# request the Station_ID of the train by the number of the train.
# For the requets both the Number and Station_ID are necessary for the query. Then i must have the Statation_ID from the number given by user
def find_train_id(train_number):
    try:
        response = requests.get(
            "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/%s"
            % train_number
        )
        response.encoding = "utf-8"
        response = response.text
    except Exception as e:
        return 'offline'  # probably the trenitalia API are offline. I must handle this situation

    if len(response) != 0 and "<H1>" not in response:
        if (
            "-" in response
        ):  # this thing is necessary because for some reasons there are train with the same number but different station_ID.
            response = response[(response.index("|") + 1) :]
            response = response[(response.index("-") + 1) : (response.index("\n"))]
            # print(autocomplete)
            return response  # return the ID of the train
        else:
            return None # Il treno non esiste


# return the JSON containing all the real time information of a train, by it's number
@app.route("/api/train/<int:number>", methods=["GET"])
def realTimeInformation(number):

    station_id = find_train_id(number)  # I need also the Station_ID for the request
    if station_id is None:
        return abort(404) #train not found
    if 'offline' in station_id:
        return abort(500) #OfflineApiTrenitalia

    url = f"{station_id}/{number}"  # See api docs: the request urls is composed by TRAIN_ID/TRAIN_NUMBER

    try:
        raw_json = requests.get(
            "http://www.viaggiatreno.it/viaggiatrenomobile/resteasy/viaggiatreno/andamentoTreno/%s"
            % url
        )
        return jsonify(raw_json.json())
    except Exception as e:
        return abort(500) #trenitalia api offline


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
