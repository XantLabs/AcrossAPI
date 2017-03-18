# BackendApp
Backend of the Codebrew 2017 application

## Requirements

Requirements do not include those included in `requirements.txt`.

- python>=3.5.2
- virtualenv

## Installation

After cloning the repository, run the following in a shell:

```sh
$ virtualenv env
$ source ./env/bin/activate
(env) $ pip install -r requirements
```

Then, edit/provide the information required in backend/secret.py. This file is not included in the repo so you must create it manually each time you clone. You'll also need to create the

```sh
(env) $ cd backend
(env) $ cp secret.py.example secret.py
(env) $ mkdir backend/media
(env) $ python runserver.py
```
