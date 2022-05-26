# Project : Quatified Self

IITM modern application development course final academic project project. Quantified self is a trackers maintaining app
along with their logs. 

## Installation

This project requires Python 3.x and the following Python libraries installed:
1. Flask
2. Flask-restful
3. Flask-SQLAlchemy
4. Matplolib

## Setup

To start this first following commands needs to be executed:

1. Command for Ubuntu terminal:
- python3.7 -m venv .env
- .env/bin/activate
- pip install -r requirements.txt
- python main.py

2.Command for Windows powershell:
- python -m venv .env
- .env\Scripts\activate
- pip install -r requirements.txt
- python main.py

## Folder Structure

- `quant.sqlite3` has the sqlite DB. It can be anywhere on the machine. Adjust the path in ``application/config.py`. Repo ships with one required for testing.
- `static` - default `static` files folder. It serves at '/static' path. 
- `static/style.css` Custom CSS. You can edit it. Its empty currently
- `templates` - Default flask templates folder
- `main.py` - main application to run the web app
- `rest_api.py` - Contains three api, for user login, trackers and logs

## Functionality

- Web app can be used to register new user and once registered user can login
- Once user is logged in, then user can add or modify their trackers
- Upon selecting the tracker user can have add or modify their logs for current log
- Logs and trackers can also be deleted


