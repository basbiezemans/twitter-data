from flask import Flask, request
from flask_restful import Resource, Api, abort
from api_lib import filter_response
from TwitterAPI import TwitterAPI
import yaml

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
        r = twitter.request('search/tweets', {'until': date, 'geocode': location})
        if r.status_code == 200:
            return {'tweets': filter_response(r)}
        else:
            return abort(r.status_code)

# Collect tweets from a specific location (longitude and latitude pair)
#
# Returns tweets by users located within a given radius of the given latitude/longitude.
# The parameter value is specified by "latitude,longitude,radius", where radius units must 
# be specified as either "mi" (miles) or "km" (kilometers).
class Collect(Resource):
    def get(self, location):
        r = twitter.request('search/tweets', {'geocode': location})
        if r.status_code == 200:
            return {'tweets': filter_response(r)}
        else:
            return abort(r.status_code)

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
api.add_resource(Collect, '/collect/<location>')
api.add_resource(Schedule, '/schedule/')

if __name__ == '__main__':
    app.run(debug=True) # TODO: REMOVE [debug] PARAM BEFORE MOVING TO PRODUCTION