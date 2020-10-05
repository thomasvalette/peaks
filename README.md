# Peaks
A simple webservice for storing and retrieving moutain peaks.

<hr>

## Installation guide

**You will need git, docker & docker-compose for this to work.**

First clone the reposiory to your machine :
```
git clone https://github.com/thomasvalette/peaks
```

Once all the file are downloaded, go into the directory created, and execute (you may have to use *sudo* depending of your installation) : 
```
docker-compose up
```

Wait until the webserver and database are up and running, then go to http://localhost

A map should appear with the sample data.

The api documentation is available with the url http://localhost/api/docs.