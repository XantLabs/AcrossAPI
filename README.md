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
(env) $ pip install -r requirements.txt
(env) $ cd backend
(env) $ mv secure.py.example secure.py
```

Then, edit/provide the information required in backend/secret.py. This file is not included in the repo so you must create it manually each time you clone.

From here, you're ready to run your server:

```sh
(env) $ python runserver.py 0.0.0.0:5000
```
