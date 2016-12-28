# California Water Bot

[Waterbot][] is a bot that tweets the current level of major California reservoirs.  It's a project by [@matttrent][matttrent].

[waterbot]:     https://twitter.com/waterbotca
[matttrent]:    https://matttrent.com

## Development Setup

create `.env` containing the following variables:

    DATABASE_URL=
    TWITTER_API_KEY=
    TWITTER_API_SECRET=
    TWITTER_ACCESS_TOKEN=
    TWITTER_ACCESS_TOKEN_SECRET=
    ENVIRONMENT=

run following commands:

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    arnold up 0

## Deploy

    heroku create
    heroku addons:create heroku-postgresql:hobby-dev
    heroku addons:create scheduler:standard
    git push heroku master
