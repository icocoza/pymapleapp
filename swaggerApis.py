from flask import Flask
from flask_restplus import Api, Resource

app = Flask(__name__)
api = Api(app)

@api.route("/hello")
class SwaggerApiClass(Resource):
	def get(self):
		return {
			"status": "Got new data"
		}
	def post(self):
		return {
			"status": "Posted new data"
		}