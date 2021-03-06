# Wall Flower

## Image Analysis and Search Playground

This is a software environment for playing around with image classification for desktop
wallpapers. It is intended to be maleable and fun!

The intent behind this is to try to gather cool looking background images and organize them into
collections of various types whcih can then be searched and retreived.


### Configure

Base configuration information.
Use a `.env` file in the root of the app to load sesitive variable.

`IMAGE_DIRECTORY` - Location to save and access image files.

`REDDIT_CLIENT_ID` - Your client id issued by reddit.
`REDDIT_CLIENT_SECRET` - Your client secret issued by reddit.
`REDDIT_USERNAME` - Your reddit username.
`REDDIT_PASSWORD` - Your reddit password.

`IMGUR_CLIENT_ID` - Your Imgur client id
`IMGUR_CLIENT_SECRET` - Your Imgur client secret
`IMGUR_ACCESS_TOKEN` - Access token gathered from Imgur
`IMGUR_REFRESH_TOKEN` - Refresh token associated with the access token

`GOOGLE_APPLICATION_CREDENTIALS` (optional) - Location for GCP application credentials.

### Database

```bash
# Start db fresh
docker run -d --name db -v /data/db -p 27017:27017 mongo:latest

# Halt db container but leave data
docker stop db

# Remove persistent db data
docker rm db
```

### Install & Run

This will create a virtual environment and install the right dependencies to it.
Then this cli will be installed with `wallflower.py` as the entrypoint.

```bash
pipenv install
pipenv shell
pip install --editable .
```

TDOD: Something is busted with this install thats needs further invesitgation

## Code Quality

Lint 
```
pylint app
```

Type Checking
```
mypy --ignore-missing-imports --follow-imports=skip app/clients
```
