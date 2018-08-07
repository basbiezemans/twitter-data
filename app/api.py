from flask import Flask, request
from flask_restful import Resource, Api, abort
from api_lib import filter_items, collect_tweets
from os import path, curdir
from time import time
from flasgger import Swagger
from TwitterAPI import TwitterAPI
import yaml
import multiprocessing as mp

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

schedule = []
yamlfile = path.join(path.abspath(curdir), 'conf', 'twitter_credentials.yml')

# Load credentials
with open(yamlfile, 'r') as file:
    credentials = yaml.load(file)

consumer_key = credentials.get('CONSUMER_KEY')
consumer_secret = credentials.get('CONSUMER_SECRET')
access_token_key = credentials.get('ACCESS_TOKEN_KEY')
access_token_secret = credentials.get('ACCESS_TOKEN_SECRET')

twitter = TwitterAPI(consumer_key, 
                     consumer_secret,
                     access_token_key,
                     access_token_secret)

class Search(Resource):
    def get(self, date, location):
        """
        Search for tweets from a specific period and location.
        Returns tweets created before the given date. Date should be formatted as YYYY-MM-DD.
        The search index has a 7-day limit. In other words, no tweets will be found for a date 
        older than one week.
        ---
        parameters:
          - in: path
            name: date
            type: string
            required: true
            description: A date, formatted as YYYY-MM-DD 
          - in: path
            name: location
            type: string
            required: true
            description: A geocode, e.g. 37.78,-122.39,1mi
        responses:
          200:
            description: The response will contain a list of tweets.
        """
        response = twitter.request('search/tweets', {'until': date, 'geocode': location})
        if response.status_code == 200:
            return {'tweets': filter_items(response)}
        else:
            return abort(response.status_code)

class Collect(Resource):
    def get(self, count, location):
        """
        Collect tweets from a specific location (longitude and latitude pair).
        Returns tweets by users located within a given radius of the given latitude/longitude.
        The parameter value is specified by "latitude,longitude,radius", where radius units must 
        be specified as either "mi" (miles) or "km" (kilometers).
        ---
        parameters:
          - in: path
            name: count
            type: integer
            required: true
            description: A number greater than zero
          - in: path
            name: location
            type: string
            required: true
            description: A geocode, e.g. 37.78,-122.39,1mi
        responses:
          202:
            description: The request has been accepted for processing, but processing has not been completed.
        """
        try:
            count = int(count)
        except ValueError:
            count = 0
        if count > 0:
            file_name = '{}-tweets-{}.txt'.format(time(), location.replace(',', '-'))
            data_path = '../data/'
            queue.put((location, count, data_path + file_name))
            message = 'The API will try to collect {} tweets in file: {}'.format(
                count,
                file_name
            )
        else:
            message = 'No tweets were collected.'
        return {'message': message}, 202

class Schedule(Resource):
    def put(self):
        """
        Schedule when tweets should be collected and from what location.
        ---
        parameters:
          - in: body
            name: timestamp
            type: string
            required: true
            description: A date and time, formatted as YYYY-MM-DD 00:00:00
          - in: body
            name: latitude
            type: float
            required: true
            description: A latitude, e.g. 37.78
          - in: body
            name: longitude
            type: float
            required: true
            description: A longitude, e.g. -122.39
        responses:
          201:
            description: The request has been fulfilled, and a new schedule object has been created.
        """
        schedule.append({
            'timestamp': request.form['timestamp'],
            'latitude': float(request.form['latitude']),
            'longitude': float(request.form['longitude'])
        })
        return schedule[-1], 201

# Endpoints
api.add_resource(Search, '/search/<date>/<location>')
api.add_resource(Collect, '/collect/<count>/<location>')
api.add_resource(Schedule, '/schedule/')

if __name__ == '__main__':
    # Start a separate Python process that will handle the collection of tweets
    mp.set_start_method('spawn')
    queue = mp.Queue()
    pool = mp.Pool(3, collect_tweets, (twitter,queue,))
    app.run(debug=False, use_reloader=False) # SET [debug=True] FOR DEVELOPMENT