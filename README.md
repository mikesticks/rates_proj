# Web service to expose current exchange rate of USD to MXN

## Installation

```
pip install virtualenv

python -m virtualenv venv --python=python3.8

source venv/bin/activate

pip install Flask-RESTful
pip install bs4
pip install requests
```

## Description

This web service is going to take current exchange rate from three different sources and expose them into the same endpoint.
