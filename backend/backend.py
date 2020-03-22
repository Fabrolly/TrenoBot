from flask import Flask, request, jsonify, abort
import requests

app = Flask(__name__)

# request the Station_ID of the train by the number of the train.
# For the requets both the Number and Station_ID are necessary for the query. Then i must have the Statation_ID from the number given by user
def find_station_id(train_number):
    try:
        response = requests.get(
            "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/%s"
            % train_number
        )
    except requests.ConnectionError:
        raise train_not_found # probably the trenitalia API are offline. But if they are offline, the response is empity

    response.encoding = "utf-8"
    response = response.text

    if len(response) != 0 and "<H1>" not in response and response is not None:
        if (
            "-" in response
        ):  # this thing is necessary because for some reasons there are train with the same number but different station_ID.
            response = response[(response.index("|") + 1) :]
            response = response[(response.index("-") + 1) : (response.index("\n"))]
            return response  # return the ID of the train
        else:
            raise train_not_found  # Il treno non esiste


# return the JSON containing all the real time information of a train, by it's number
@app.route("/api/train/<int:number>", methods=["GET"])
def realTimeInformation(number):

    station_id = find_station_id(number)  # I need also the Station_ID for the request

    if station_id is None:
        return abort(404)


    url = f"{station_id}/{number}"  # See api docs: the request urls is composed by TRAIN_ID/TRAIN_NUMBER

    try:
        raw_json = requests.get(
            "http://www.viaggiatreno.it/viaggiatrenomobile/resteasy/viaggiatreno/andamentoTreno/%s"
            % url
        )
        return jsonify(raw_json.json())
    except:
        return abort(500)  # trenitalia api offline



class train_not_found(Exception):
    pass

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
