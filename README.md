# CS122-Project, Following Twitter Hashtags

### Running on Heroku
* Command to creat a worker dyno and start the stream
  * `heroku ps:scale worker=1`
* Command to stop the script from Terminal
  * `heroku ps:scale worker=0`
* View processes with `heroku ps` and logs with `heroku logs`
