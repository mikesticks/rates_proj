from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

rates = list()

# Define Resources
class Rate(Resource):
    def get(self, source_name):
        pass

    def post(self, source_name):
        pass

    def put(self, source_name):
        pass

    def delete(self, source_name):
        pass


class Rates(Resource):
    def get(self):
        return {"rates": rates}


# Define Routes
api.add_resource(Rate, "/rate/<string:source_name>")
api.add_resource(Rates, "/rates")


if __name__ == "__main__":
    app.run(debug=True)
