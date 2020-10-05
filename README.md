# Peaks
A simple webservice for storing and retrieving moutain peaks.

<hr>

## Installation guide

**You will need git, docker & docker-compose for this to work.**



**Note :** If you are on windows execute this config command before cloning the repository, it prevents windows from converting \n in \r\n which breaks bash scripts.

```
git config --global core.autocrlf false
```
First clone the repository to your machine :
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