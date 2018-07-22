from flask import Flask, request
from flask_restful import Resource, Api, abort
from api_lib import filter_items, collect_tweets
from time import time
from TwitterAPI import TwitterAPI
import yaml
import multiprocessing as mp

app = Flask(__name__)
api = Api(app)

schedule = []

# Load credentials from YAML file
with open('../var/twitter_credentials.yaml', 'r') as file:
    credentials = yaml.load(file)

consumer_key = credentials.get('CONSUMER_KEY')
consumer_secret = credentials.get('CONSUMER_SECRET')
access_token_key = credentials.get('ACCESS_TOKEN_KEY')
access_token_secret = credentials.get('ACCESS_TOKEN_SECRET')

twitter = TwitterAPI(consumer_key, 
                     consumer_secret,
                     access_token_key,
                     access_token_secret)

# Search for tweets from a specific period and location
#
# Returns tweets created before the given date. Date should be formatted as YYYY-MM-DD.
# The search index has a 7-day limit. In other words, no tweets will be found for a date 
# older than one week.
class Search(Resource):
    def get(self, date, location):
        response = twitter.request('search/tweets', {'until': date, 'geocode': location})
        if response.status_code == 200:
            return {'tweets': filter_items(response)}
        else:
            return abort(response.status_code)

# Collect tweets from a specific location (longitude and latitude pair)
#
# Returns tweets by users located within a given radius of the given latitude/longitude.
# The parameter value is specified by "latitude,longitude,radius", where radius units must 
# be specified as either "mi" (miles) or "km" (kilometers).
class Collect(Resource):
    def get(self, count, location):
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

# Schedule when tweets should be collected and from what location
class Schedule(Resource):
    def put(self):
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
    app.run(debug=True, use_reloader=False) # TODO: SET [debug=False] BEFORE MOVING TO PRODUCTION