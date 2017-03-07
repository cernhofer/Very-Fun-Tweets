# CS122-Project, Following Twitter Hashtags

### Running on Heroku
* Command to creat a worker dyno and start the stream
  * `heroku ps:scale worker=1`
* Command to stop the script from Terminal
  * `heroku ps:scale worker=0`
* View processes with `heroku ps` and logs with `heroku logs`

### TODO (for RCC)
To run mongo, use the `run_mongo` alias (if it exists) or `~/bin/mongodb/bin/mongod --dbpath ~/data/db`

* [ ] Write a script to run everything at once
  * [ ] `source ~/.bash_profile`
  * [ ] `run_mongo`
  * [ ] `module load python/3.4-2015q1`
  * [ ] `pip3 install -r requirements.txt --user`
  * [ ] `streaming_api.py`

### To look at the MongoDB in RCC
 * `~/bin/mongodb/bin/mongo`
 * `show dbs`
 * `use cs122`
 * `db.tweets.count()`
 * `db.tweets.find().limit(1)`

### To run migrations
 * `python3 manage.py makemigrations`
 * `python3 manage.py migrate`
 * To check: `psql cs122`
 * To run migrations to Heroku: `heroku run python3 django_app/tweets/manage.py migrate`

### To check up on Postgres from Terminal
 * `heroku run django_app/tweets/manage.py shell`
 * `from tweet_search.models import Hashtag`
 * `Hashtag.objects.count()`

### To delete data from Postrgres
 * `heroku run django_app/tweets/manage.py shell`
 * `from tweet_search.models import Hashtag`
 * `Hashtag.objects.all().delete()`
