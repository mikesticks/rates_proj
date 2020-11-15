# Web service to expose current exchange rate of USD to MXN
This web service is going to take current exchange rate from three different sources and expose them into the same endpoint.


## Installation

```
pip install virtualenv

python -m virtualenv venv --python=python3.8

source venv/bin/activate

pip install Flask-RESTful
pip install flask-jwt-extended
pip install Flask-Limiter
pip install bs4
pip install requests
```


## Deployment
- Enable virtual environment
```
source venv/bin/activate
```
- Go to the folder where app.py is located
- Execute app.py
```
python app.py
```


## Requests
To access a protected view, what we need to do is,

1. Request an access token by making a POST to our endpoint *__/auth__*
and pass a *username* and a *password* in `Content-Type header: Application/json` as the next json object:
```
{
    "username": "testuser",
    "password": "z1c3b5m7"
}
```

2. Pass the returned access token value as the `Authorization header: Bearer <access_token>`

**NOTE:** Current reta limit is set to 200 request per day or 50 request per hour