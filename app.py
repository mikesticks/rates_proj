import json
import requests

from bs4 import BeautifulSoup
from datetime import datetime
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
            "last_update": payload["last_update"],
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
                rate["last_update"] = payload["last_update"]
                rate["value"] = float(payload["value"])
                return rate, 202

        # if it doesn't exist then create a new rate sources
        new_rate = {
            "source_name": source_name,
            "last_update": payload["last_update"],
            "value": float(payload["value"])
        }
        rates.append(new_rate)
        return new_rate, 201

    def delete(self, source_name):
        # verify the requested element exists
        idx_to_remove = None
        for idx, rate in enumerate(rates):
            if rate["source_name"] == source_name:
                idx_to_remove = idx
                break
        if idx_to_remove is not None:
            rates.pop(idx_to_remove)
            return {"message": "rate source '{}' deleted".format(source_name)}
        else:
            return {"message": "rate source '{}' doesn't exist".format(source_name)}, 404


class Rates(Resource):
    def get(self):
        return {"rates": rates}

    def post(self):
        global rates
        rates = []
        def get_exchange_rate_fixer():
            endpoint = "latest"
            payload = {"access_key": "059b15fd0d1497de7413112acba27991", "base": "EUR", "symbols": "MXN,USD"}
            request = requests.get("http://data.fixer.io/api/{}".format(endpoint), params=payload)
            result = json.loads(request.text)
            value = round((result["rates"]["MXN"] / result["rates"]["USD"]), 4)
            return value, result["date"]

        def get_exchange_rate_banxico():
            endpoint = "series/SF43718/datos/oportuno"
            payload = {"mediaType": "json",
                       "token": "88fc2150f9717d4a6c16f4d531a5675b5df6a16b7770678f08431b8e35d06a02"}
            request = requests.get("https://www.banxico.org.mx/SieAPIRest/service/v1/{}".format(endpoint),
                                   params=payload)
            result = json.loads(request.text)
            result = result["bmx"]["series"][0]["datos"][0]
            date = str(datetime.strptime(result["fecha"], "%d/%m/%Y").date())
            return round(float(result["dato"]), 4), date

        def get_exchange_rate_dof():
            url = "https://www.dof.gob.mx"
            endpoint = "/indicadores_detalle.php"

            for i in range(3):
                req_date = date.today() - timedelta(days=i)
                payload = "cod_tipo_indicador=158&dfecha={0}%2F{1}%2F{2}&hfecha={0}%2F{1}%2F{2}".format(req_date.day,
                                                                                                        req_date.month,
                                                                                                        req_date.year)
                request = requests.get("{}{}".format(url, endpoint), params=payload)
                soup = BeautifulSoup(request.content, "html.parser")
                results = soup.find_all("table", class_="Tabla_borde")
                for result in results:
                    if hasattr(result, "contents"):
                        if len(result.contents) > 3:
                            last_update, value = result.contents[3].text[1:-1].split("\n")
                            return round(float(value), 4), str(datetime.strptime(last_update, "%d-%m-%Y").date())
                        else:
                            break
            return None, None

        default_rates = [
            ("fixer", get_exchange_rate_fixer),
            ("banxico", get_exchange_rate_banxico),
            ("diario_oficial_federacion", get_exchange_rate_dof)
        ]
        for default_rate in default_rates:
            value, date = default_rate[1]()
            new_rate = {
                "source_name": default_rate[0],
                "last_update": date,
                "value": value
            }
            rates.append(new_rate)
        return {"rates": rates}


# Define Routes
api.add_resource(Rate, "/rate/<string:source_name>")
api.add_resource(Rates, "/rates")


if __name__ == "__main__":
    app.run(debug=True)
