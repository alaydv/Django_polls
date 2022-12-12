# Platzi Polls with Django [![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This project was develop in Django, this prejects provides with a interactive app, where you can vote for some questions, in fact you can add more questions.

- This project contains tests that you can run.
- Install requirements in your own enviroment.
- ✨You can use Docker, as well.✨

## Features

- You can vote.
- Data is saved in a Database, wheter sqlite3 or postgresql. 
- Donwload and check it out in your own enviroment.

## Tech

This project use Django as main tool, but contains other technologies for deploy:

- [Django] - Logic in the app!
- [Gunicorn] - For deploy project.
- [Docker] - More easy way to distrive and manage project.
- [PostgreSQL] - Use it as a database, for deploy and probes with django.

## Installation

First of all, you need to clone this repo, for that follow the next steps: 

```sh
git clone https://github.com/alaydv/Django_polls.git
```

For local environments with pip...

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
You can see how looks the project, just write:

```sh
python3 manage.py runserver --settings=premiosplatziapp.settings.local
```

## Docker

To use docker follow the next stesps.

To retrive the image just run:
```sh
docker pull alaydv/docker-django
docker-compose up --build
```

Then you are in the right way...

Once done, run the Docker image and map the port to whatever you wish on
your host. In this example, we simply map port 8000 of the host to
port 8080 of the Docker:

```sh
docker-compose -f docker-compose.yml run --rm django python3 manage.py runserver --settings=premiosplatziapp.settings.local
```

Okay, all is made it, so just probe it.
## License

MIT
