# AccessibleCooking
A repository for Sightless Chef, a prototype recipe website for people who are visually impaired.

Heroku app: https://sightless-chef.herokuapp.com/

Documentation website: https://arianaolson419.github.io/AccessibleCooking/

## Installation

Working on this project requires some amount of set up. To start, fork and clone this repository. There are some dependencies to install afterwards.

### MongoDB

Install MongoDB. Use [these
instructions](https://docs.mongodb.com/getting-started/shell/installation/). On
macOS with [Homebrew](https://brew.sh/) installed, you can instead run `brew install mongodb`.

`sudo service mongod start` to run the database locally

### Pipenv

For local development, pipenv is a good tool. To install,

```shell
pip install pipenv
```

Then change to the desired directory (in this case, AccessibleCooking).

```shell
cd AccessibleCooking
pipenv install
pipenv shell
```

This should create a virtual environment with all dependencies installed, then launch the environment. To exit,

```shell
deactivate
```

This [guide to pipenv](https://robots.thoughtbot.com/how-to-manage-your-python-projects-with-pipenv) may help debug any issues.

### Flask

Flask should be installed when the pipenv is created. See [this overview of Flask](http://flask.pocoo.org/) if there are any difficulties.

### MongoAlchemy

Flask-MongoAlchemy should be installed with the pipenv. It provides an easy interface with the mongoDB. This [MongoAlchemy documentation site](https://pythonhosted.org/Flask-MongoAlchemy/) provides an overview.

### Set up Heroku App

Follow [startup instructions for Heroku](https://devcenter.heroku.com/start).

[Link a database in mLab to your Heroku app](https://devcenter.heroku.com/articles/mongolab).

## Recipe and Tip Contribution

Read style_guide.md before contributing content to Sightless Chef. Recipes and tips are intended to be for the visually impaired by the visually impaired or career specialists.

## Built With

[Skeleton CSS templates](http://getskeleton.com)

[Flask MongoAlchemy](https://pythonhosted.org/Flask-MongoAlchemy/)
