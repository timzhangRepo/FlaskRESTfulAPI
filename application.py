from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
from datetime import date
from flask import send_from_directory
import os
from datetime import date
from dateutil.relativedelta import relativedelta
import requests
import json 



application=Flask(__name__)
api = Api(application)
CORS(application)

url = "https://api.tiingo.com/tiingo/daily/"
stock_url = "https://api.tiingo.com/iex/"
token = "token=a24173cb58feb7109d23ffe4d3f16abe1594f938"



today = str(date.today());
six_months = date.today() + relativedelta(months=-6);
six_months=str(six_months);

newsurl = "http://newsapi.org/v2/everything?q="
newsToken = "&sortBy=publishedAt&apiKey=dbc03e0b69d34663a517e07fa02a0c9f"


@application.route("/")
def home():
    return send_from_directory(os.path.join(os.getcwd(), 'static'), "g9velrLOqh.html")

class statusCheck(Resource):
	def get(self):
		return {"data":"OK"}

class companyOutlook(Resource):
	def get(self, ticker):
		headers = {'Content-Type': 'application/json'}
		requestResponse = requests.get(url+ticker+"?"+token, headers=headers)
		data = json.loads(requestResponse.text)
		return data
class stockSummary(Resource):
	def get(self, ticker):
		headers = {'Content-Type': 'application/json'}
		requestResponse = requests.get(stock_url+ticker+"?"+token, headers=headers)
		data = json.loads(requestResponse.text)
		return data

class news(Resource):
	def get(self, ticker):
		headers = {'Content-Type': 'application/json'}
		response = requests.get(newsurl+ticker+"&from"+today+newsToken)
		data = json.loads(response.text)
		return data
class charts(Resource):
	def get(self, ticker):
		headers = {'Content-Type': 'application/json'}
		response = requests.get(stock_url+ticker+"/prices?startDate="+six_months+"&resampleFreq=12hour&columns=open,high,low,close,volume&"+token)
		data = json.loads(response.text)
		return data

api.add_resource(companyOutlook,"/response/<string:ticker>")
api.add_resource(stockSummary,"/stock/<string:ticker>")
api.add_resource(news,"/news/<string:ticker>")
api.add_resource(charts,"/charts/<string:ticker>")

if __name__ == '__main__':
	application.run(debug=True)