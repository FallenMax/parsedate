start:
	FLASK_ENV=development pipenv run python3 -m flask run --host=0.0.0.0

serve:
	# https://flask.palletsprojects.com/en/1.1.x/deploying/uwsgi/#starting-your-app-with-uwsgi
  # https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html
	uwsgi --http :5000 -s /tmp/parsedate.sock --manage-script-name --mount /=app:app --processes 2 --threads 2

install:
	pipenv install

install-all:
	# to build uwsgi
	apt-get install build-essential python-dev python3-dev
	python3 -m pip install --upgrade pip setuptools wheel pipenv uwsgi
	pipenv install

