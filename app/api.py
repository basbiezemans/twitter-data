from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

schedule = []

# Search for tweets from a specific period and location
class Search(Resource):
    def get(self, date, location):
        return {'tweets': []}

# Collect tweets from a specific location (longitude and latitude pair)
class Collect(Resource):
    def get(self, location):
        return {'tweets': []}

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