from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# request the Station_ID of the train by the number of the train.
# For the requets both the Number and Station_ID are necessary for the query. Then i must have the Statation_ID from the number given by user
def trainId(train_number):
    try:
        response = requests.get('http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/%s' % train_number)
        response.encoding = 'utf-8'
        response = response.text
    except Exception as e:
        return "error"  # probably the trenitalia API are offline. I must handle this situation

    if len(response) != 0 and "<H1>" not in response:
        if (
            "-" in response
        ):  # this thing is necessary because for some reasons there are train with the same number but different station_ID.
            response = response[(response.index("|") + 1) :]
            response = response[
                (response.index("-") + 1) : (response.index("\n"))
            ]
            # print(autocomplete)
            return response  # return the ID of the train
        else:
            return "error"


# return the JSON containing all the real time information of a train, by it's number
@app.route("/api/train/<int:number>", methods=["GET"])
def realTimeInformation(number):
    try:
        idTrain = trainId(number)  # I need also the Station_ID for the request
        if "error" in idTrain:
            return "", "", "error"
        url = "%s/%s" % (
            idTrain,
            number,
        )  # See api docs: the request urls is composed by TRAIN_ID/TRAIN_NUMBER
        raw_json = (
            requests.get(
                "http://www.viaggiatreno.it/viaggiatrenomobile/resteasy/viaggiatreno/andamentoTreno/%s"
                % url
            )
        )
        return jsonify(raw_json.json())
    except Exception as e:
        return e


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
