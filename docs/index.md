# Welcome to e-Coke
Live version at: `#link`

## Running locally
1. You should have Python(3.5 or greater) and pip installed in your system.
2. Clone the project into your local machine `git clone https://github.com/ErickMwazonga/e-Coke.git`
3. `cd e-Coke`
4. `pip install -r requirements.txt`
5. Run `python manage.py migrate` to create the database. Kindly note that PostgreSQL database is   used. Use or override the database settings declared in `ecoke/settings/base.py` accordingly.
6. Run `python manage.py runserver` to start the server.
7. Visit `localhost:8000` in your browser.

## Running tests locally
All tests are located in `/tests`
To run: `python manage.py test tests`
