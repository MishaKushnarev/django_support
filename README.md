# **DJANGO SUPPORT**
## Program for administration supports requests
___
## Setup the environment
```
pipenv install
```
## Install supporting modules
```
pipenv install black==22.6.0
pipenv install isort==5.10.1
pipenv install flake8==5.0.3
```
## Create environment configuration files
```
.flake8 - flake8 settings
pyproject.toml - settings for black, isort
pipfile - contains a list of modules that are used for the correct operation of the project.
Pipfile.lock - contains a list of modules with a fixed version, which are used for the correct operation of the project.
.pre-commit-config.yaml
```

## Install pre-commit hooks
> Note: Install pre-commit tool before
pre-commit install 
```
pre-commit 2.20.0
```

# Main information
|File|Info|
| -- | -- |
|manage.py|Script for operation with django|
|history.json|contains history of exchange_rates|
___
### Application  ***authentication***

Application for manage user login/logon.
|File|Info|
| -- | -- |
|migrations/| description of all fields of the authenticator database data model|
|admin.py|description administration panel|
|models.py|description of the database model of the administration panel|
___
### Folder ***config***
Settings for project
|File|Info|
| -- | -- |
|settings.py|In file - settings for project|
|urls.py|the files describe the connection of scripts with external access|
___
### Application ***core***
Content for process
|File|Info|
| -- | -- |
|migrations/|description of all fields of the core database data model|
|admin.py|description display tickets, comments|
|models.py|description of the database model of the tickets, comments|
___
### Application ***exchange_rates***
Content for process
|File|Info|
| -- | -- |
|exchange_rates.py|Script for obtaining and processing exchange rates|
|history.json|Storage of the result from exchange_rates.py|
|tickets.py|Script for handling customer requests|
### Application ***shared***
Application for change data
|File|Info|
| -- | -- |
|django/models.py|The script contains temporary data for adding/editing data in the database. The script does not use imports from other applications|
___