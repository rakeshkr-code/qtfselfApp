# Basic Requirement
- You should have Python installed in your machine 

# Local Setup
- Clone the project (double click to Run)
- Run `local_setup.sh` if you are using Linux machine.
- Run `local_setup.bat` if you are using Windows machine.
- It will create the .env and will setup the environment (install required packages)

# Local Development Run
- Run `local_run.sh` if you are using Linux machine.
- Run `local_run.bat` if you are using Windows machine. 
- It will start the flask app in `development` mode. Suited for local development.

# Folder Structure

- `db_directory` has the sqlite DB. It can be anywhere on the machine. Adjust the path in ``application/config.py`. Repo ships with one required for testing.
- `application` is where our application code is
- `local_setup.sh` or `local_setup.bat` set up the virtualenv inside a local `.env` folder. 
- `local_run.sh` or `local_run.bat` Used to run the flask application in development mode
- `static` - default `static` files folder. It serves at '/static' path. More about it is [here](https://flask.palletsprojects.com/en/2.0.x/tutorial/static/).
- `static/bootstrap` We have already added the bootstrap files so it can be used
- `static/style.css` Custom CSS.
- `static/images` and `static/icons` stores all the images and icons resp.
- `templates` - Default flask templates folder


```
├── application
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── controllers.py
│   ├── database.py
│   ├── models.py
│   └── __pycache__
│       ├── config.cpython-36.pyc
│       ├── config.cpython-37.pyc
│       ├── controllers.cpython-36.pyc
│       ├── controllers.cpython-37.pyc
│       ├── database.cpython-36.pyc
│       ├── database.cpython-37.pyc
│       ├── __init__.cpython-36.pyc
│       ├── __init__.cpython-37.pyc
│       ├── models.cpython-36.pyc
│       └── models.cpython-37.pyc
├── db_directory
│   └── database.sqlite3
├── local_run.bat
├── local_run.sh
├── local_setup.bat
├── local_setup.sh
├── app.py
├── readme.md
├── requirements.txt
├── static
│   ├── bootstrap
│   │   ├── css
│   │   │   ├── bootstrap.css
│   │   │   ├── bootstrap.css.map
│   │   │   ├── bootstrap-grid.css
│   │   │   ├── bootstrap-grid.css.map
│   │   │   ├── bootstrap-grid.min.css
│   │   │   ├── bootstrap-grid.min.css.map
│   │   │   ├── bootstrap-grid.rtl.css
│   │   │   ├── bootstrap-grid.rtl.css.map
│   │   │   ├── bootstrap-grid.rtl.min.css
│   │   │   ├── bootstrap-grid.rtl.min.css.map
│   │   │   ├── bootstrap.min.css
│   │   │   ├── bootstrap.min.css.map
│   │   │   ├── bootstrap-reboot.css
│   │   │   ├── bootstrap-reboot.css.map
│   │   │   ├── bootstrap-reboot.min.css
│   │   │   ├── bootstrap-reboot.min.css.map
│   │   │   ├── bootstrap-reboot.rtl.css
│   │   │   ├── bootstrap-reboot.rtl.css.map
│   │   │   ├── bootstrap-reboot.rtl.min.css
│   │   │   ├── bootstrap-reboot.rtl.min.css.map
│   │   │   ├── bootstrap.rtl.css
│   │   │   ├── bootstrap.rtl.css.map
│   │   │   ├── bootstrap.rtl.min.css
│   │   │   ├── bootstrap.rtl.min.css.map
│   │   │   ├── bootstrap-utilities.css
│   │   │   ├── bootstrap-utilities.css.map
│   │   │   ├── bootstrap-utilities.min.css
│   │   │   ├── bootstrap-utilities.min.css.map
│   │   │   ├── bootstrap-utilities.rtl.css
│   │   │   ├── bootstrap-utilities.rtl.css.map
│   │   │   ├── bootstrap-utilities.rtl.min.css
│   │   │   └── bootstrap-utilities.rtl.min.css.map
│   │   └── js
│   │       ├── bootstrap.bundle.js
│   │       ├── bootstrap.bundle.js.map
│   │       ├── bootstrap.bundle.min.js
│   │       ├── bootstrap.bundle.min.js.map
│   │       ├── bootstrap.esm.js
│   │       ├── bootstrap.esm.js.map
│   │       ├── bootstrap.esm.min.js
│   │       ├── bootstrap.esm.min.js.map
│   │       ├── bootstrap.js
│   │       ├── bootstrap.js.map
│   │       ├── bootstrap.min.js
│   │       └── bootstrap.min.js.map
│   ├── icons
│   │   └── favicon.ico
│   ├── images
│   │   ├── hist.png
│   │   └── monthlygraph.png
│   └── style.css
└── templates
    ├── about.html
    ├── addNewLog.html
    ├── contactus.html
    ├── createTracker.html
    ├── dashboard.html
    ├── errorPage.html
	├── help.html
    ├── invalid_input.html
    ├── loginPage.html
    ├── profile.html
    ├── registerPage.html
    ├── trackerDetails.html
    ├── trackerExists.html
    ├── updateLogEntry.html
    └── updateTracker.html
```