import requests
import json
from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

rates = list()

# Define Resources
class Rate(Resource):
    def get(self, source_name):
        # verify the requeted element exists
        for rate in rates:
            if rate["source_name"] == source_name:
                return {"rate": rate}
        return {"message": "rate source '{}' doesn't exist".format(source_name)}, 404

    def post(self, source_name):
        # verify the requested element exists
        for rate in rates:
            if rate["source_name"] == source_name:
                return {"message": "rate source '{}' already exists".format(source_name)}, 400

        # todo: it's required to check for arguments before to add them
        payload = request.get_json()

        # store the requested rate source and its content
        new_rate = {
            "source_name": source_name,
            "timestamp": payload["timestamp"],
            "value": float(payload["value"])
        }
        rates.append(new_rate)
        return new_rate, 201

    def put(self, source_name):
        # todo: parse arguments in order to include only necessary elements
        payload = request.get_json()

        # verify the requested element exists
        for rate in rates:
            if rate["source_name"] == source_name:
                # update values for rate source
                rate["timestamp"] = payload["timestamp"]
                rate["value"] = float(payload["value"])
                return rate, 202

        # if it doesn't exist then create a new rate sources
        new_rate = {
            "source_name": source_name,
            "timestamp": payload["timestamp"],
            "value": float(payload["value"])
        }
        rates.append(new_rate)
        return new_rate, 201

    def delete(self, source_name):
        # verify the requested element exists
        for idx, rate in enumerate(rates):
            if rate["source_name"] == source_name:
                idx_to_remove = idx
                break
        if idx_to_remove:
            rates.pop(idx_to_remove)
            return {"message": "rate source '{}' deleted"}.format(source_name)
        else:
            return {"message": "rate source '{}' doesn't exist".format(source_name)}, 404


class Rates(Resource):
    def get(self):
        return {"rates": rates}

    def post(self):
        def get_exchange_rate_fixer():
            endpoint = "latest"
            payload = {"access_key": "059b15fd0d1497de7413112acba27991", "base": "EUR", "symbols": "MXN,USD"}
            request = requests.get("http://data.fixer.io/api/{}".format(endpoint), params=payload)
            result = json.loads(request.text)
            value = round((result["rates"]["MXN"] / result["rates"]["USD"]), 2)
            return value, result["date"]

        def get_exchange_rate_banxico():
            # 88fc2150f9717d4a6c16f4d531a5675b5df6a16b7770678f08431b8e35d06a02
            pass

        def get_exchange_rate_dof():
            pass

        default_rates = [
            ("fixer", get_exchange_rate_fixer),
            # ("banxico", get_exchange_rate_banxico),
            # ("diario_oficial_federacion", get_exchange_rate_dof)
        ]
        for default_rate in default_rates:
            value, date = default_rate[1]()
            new_rate = {
                "source_name": default_rate[0],
                "timestamp": date,
                "value": value
            }
            rates.append(new_rate)
        return {"rates": rates}


# Define Routes
api.add_resource(Rate, "/rate/<string:source_name>")
api.add_resource(Rates, "/rates")


if __name__ == "__main__":
    app.run(debug=True)
