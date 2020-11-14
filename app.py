from flask import Flask
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
        # store the requested rate source and its content
        new_rate = {
            "source_name": source_name,
            "timestamp": None,
            "value": None
        }
        rates.append(new_rate)
        return new_rate, 201

    def put(self, source_name):
        # todo: parse arguments in order to include only necessary elements
        # verify the requested element exists
        for rate in rates:
            if rate["source_name"] == source_name:
                # update values for rate source
                rate["timestamp"] = "Updated_timestamp"
                rate["value"] = "Updated_value"
                return rate, 202
        # if it doesn't exist then create a new rate sources
        new_rate = {
            "source_name": source_name,
            "timestamp": None,
            "value": None
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


# Define Routes
api.add_resource(Rate, "/rate/<string:source_name>")
api.add_resource(Rates, "/rates")


if __name__ == "__main__":
    app.run(debug=True)
