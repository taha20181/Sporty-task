# Sporty-task

Clone the above repo
cd Sporty-task

## Create and activate virtual env
run python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Run flask app
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
