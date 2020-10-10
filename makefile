start:
	FLASK_ENV=development pipenv run python -m flask run --host=0.0.0.0 --port=5010

serve:
	# https://flask.palletsprojects.com/en/1.1.x/deploying/uwsgi/#starting-your-app-with-uwsgi
	# https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html
	pipenv run uwsgi --master --http :6010 -s /tmp/parsedate.sock --manage-script-name --mount /=app:app --processes 2 --threads 2

install:
	pipenv install

install-all:
	# https://packaging.python.org/
	# sudo apt-get install python3.8
	pip install --upgrade pip setuptools wheel pipenv
	# build/install uwsgi
	# https://stackoverflow.com/questions/21669354/rebuild-uwsgi-with-pcre-support
	sudo apt-get install build-essential python-dev python3-dev
	sudo apt-get install libpcre3 libpcre3-dev
	pip install uwsgi -I --no-cache-dir
	pipenv install

