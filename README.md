# Twitter Data
Application that collects and stores tweets from a specific location.

## Requirements

* Python >= 3.6
* Packages: Flask, Flask-RESTful, TwitterAPI, PyYaml, Flasgger

## Installation

1. Clone or download the repository. 
2. Install the necessary software packages.

  ```bash
  $ pip install -r /path/to/requirements.txt
  ```
3. Rename the file `twitter_credentials.yml-example` in the `conf` folder to `twitter_credentials.yml`. Afterwards edit the file and add your [Twitter Application](https://apps.twitter.com/) credentials.

After a successful installation you are ready to run a local version of the application. You can run the API in the application root folder with the following command.

```bash
$ python app/api.py
```

## Docker

Instead of a local installation you can run the application in a Docker container. First clone or download the repository, and edit the `twitter_credentials.yml` file.

Build an image with the name `twitter-data`.

```bash
$ docker build -t twitter-data .
```

Create a container from the `twitter-data` image and run it as a daemon on port 5000. Bind a local (data) folder to the container's data folder.

```bash
$ docker run -d -p 5000:5000 -v ~/twitter/data:/usr/src/app/data twitter-data
```

## RESTful API

Open up a new prompt to test the API using curl. Replace YYYY-MM-DD with today's date.

```bash
$ curl http://127.0.0.1:5000/search/YYYY-MM-DD/37.781157,-122.398720,10mi
```

## Unit tests

Once the API is running, you can run the unit tests in the application root. 

```bash
$ python -m unittest discover tests
```

## Documentation

Once the API is running, you can view the API documentation by browsing to the following URL.

```
http://127.0.0.1:5000/apidocs/
```

## Collecting Tweets

To collect, for example, 1000 tweets from Dublin Ireland you can use the API request below.

```bash
$ curl http://127.0.0.1:5000/collect/1000/53.341,-6.248,10mi
```

Collected tweets are stored in the `data` folder, in the application root.

