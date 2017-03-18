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
(env) $ touch api.keys
```

Then, edit/provide the information required in backend/secret.py. This file is not included in the repo so you must create it manually each time you clone. You must also generate api keys in api.keys, one key per line. Use any method you like.

From here, you're ready to run your server:

```sh
(env) $ python runserver.py 0.0.0.0:5000
```

## Documentation

You can **upload** a file given a correct API key and request headers:

```
HTTP POST http://<SOME_IP>/api/upload
'file': File,
'lat': User's Latitude,
'lon': User's longitude,
'caption': User inputted caption (not required),
'language': User's language (from phone),
'apikey': App's api key.
```

You can request a list of n photo objects with:

```
HTTP GET http://<SOME_IP>/

```

Finally, you can get an image directly from below. Note that you do not need an API key for this operation. Rate limiting still applies.

```
HTTP GET http://<SOME_IP>/api/media/<filename>
```
