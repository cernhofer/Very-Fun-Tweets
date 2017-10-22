# CS122-Project, Very Fun Tweets

## Chelsea Ernhofer, Sushmita Gopalan, and Haylee Ham

## [www.veryfuntweets.com](http://www.veryfuntweets.com)
* To see a current list of searchable hashtags, go to [www.veryfuntweets.com/checkup](http://www.veryfuntweets.com/checkup)

### Index of Files
* streaming_api.py
	* Connects to Twitter API, streams sample of tweets in mongo database
	* Constantly running on RCC servers
* spikes.py  
	* Detects spikes in hashtag usage- up to 3 per hashtag
* scraping folder
	* tweet_scraper.py - calculates most common words in tweet text
	* news_scraper.py - finds relevant news stories by date & hashtag
* whole_rcc.py
	* main script used to pass data from mongo, through spikes and scraping
	scripts, and through to postgres
* push_to_postgres.py
	* transfers data from whole_rcc.py into postgres database, in proper format
* django_app
	* contains all necessary files to run django application
	* includes views, templates, and models

### Data Collection
This project uses MongoDB to collect a sample of data from Twitter using the streaming API. Here are the steps to set up a MongoDB instance and start collecting Twitter Data.
* [ ] Make sure you have Mongo installed (`brew install mongo`)
* [ ] Create a Mongo database called `cs122`
* [ ] Put Twitter API keys in a .env (`ACCESS_TOKEN`, `ACCESS_TOKEN_SECRET`, `CONSUMER_KEY`, `CONSUMER_KEY_SECRET`)
  * [ ] You can supply a valid MongoDB URI in place of creating the MongoDB locally (`MONGODB_URI`)
* [ ] Run `pip3 install -r requirements.txt`
* [ ] Run `python3 streaming_api.py`

This will start feeding tweets into your MongoDB. A random sample of 1% of all English tweets will start streaming.

### Django App
We have created a Django app that makes visualizations to understand spikes in hashtag usage and the news stories that give context to those spikes. Before we can transfer the data from our large MongoDB instance, we need to set up Django app.
* [ ] Make sure you have postgres installed (`brew install postgres`)
  * [ ] The database should be named `cs122` unless provided a valid postgres URI in the .env as `DATABASE_URL`
* [ ] Run the app locally with `python3 django_app/tweets/manage.py runserver`

Once the app is set up, we can start moving data from the large MongoDB into a more consumable format that Django has access to using our provided scripts which tease out spikes and scrape google news for context. When spikes and stories are found, the corresponding data will be pushed to a PostgresDB to be accessed by the Django app. In order to run these scripts:
* [ ] Make sure you have the correct `REQUEST_BASE` set in `push_to_postgres.py` (it will be `localhost:8000` when running locally)
* [ ] Run `python3 whole_rcc.py`

### Useful commands for RCC and Heroku environments
#### Running on Heroku
* Command to creat a worker dyno and start the stream
  * `heroku ps:scale worker=1`
* Command to stop the script from Terminal
  * `heroku ps:scale worker=0`
* View processes with `heroku ps` and logs with `heroku logs`

#### Getting set up with streaming on RCC
To run mongo, use the `run_mongo` alias (if it exists) or `~/bin/mongodb/bin/mongod --dbpath ~/data/db`

  * [ ] `source ~/.bash_profile`
  * [ ] `run_mongo`
  * [ ] `module load python/3.4-2015q1`
  * [ ] `pip3 install -r requirements.txt --user`
  * [ ] `streaming_api.py`

#### Checking up on MongoDB in RCC
 * `~/bin/mongodb/bin/mongo`
 * `show dbs`
 * `use cs122`
 * `db.tweets.count()`
 * `db.tweets.find().limit(1)`

#### To run migrations
 * `python3 manage.py makemigrations`
 * `python3 manage.py migrate`
 * To check: `psql cs122`
 * To run migrations to Heroku: `heroku run python3 django_app/tweets/manage.py migrate`

#### Checking up on Postgres in Heroku
 * `heroku run django_app/tweets/manage.py shell`
 * `from tweet_search.models import Hashtag`
 * `Hashtag.objects.count()`

#### Deleting data from Postrgres on Heroku
 * `heroku run django_app/tweets/manage.py shell`
 * `from tweet_search.models import Hashtag`
 * `Hashtag.objects.all().delete()`

tiny baby test 