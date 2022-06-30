#!/bin/bash

<<COMMENT
	Starting a development server
=========================================
. venv/bin/activate
export FLASK_APP=blagajna
export FLASK_ENV=development
flask run --host=0.0.0.0
COMMENT

#	Starting a production server
#========================================
. venv/bin/activate
export FLASK_APP=blagajna
export FLASK_ENV=production
waitress-serve --port=8123 --call "blagajna:create_app"