# Introduction

this is a scaffold for a python flask backend

# Getting Started

1. Clone the repository
2. Confirmed that you have python 3.9 or later installed
3. Install the dependencies with `pip install -r requirements.txt`
4. Run the server with `python main.py`

# structure of the project

A basic user login and register system is implemented in this scaffold, that will help you to understand the structure of the project.

- `main.py` is the entry point of the application
- `config` the configuration of the application
    - `basic.py` the base configuration
    - `debug.py` the configuration for the development environment
    - `prod.py` the configuration for the production environment
    - `controller_test.py` the configuration for the controller test environment, don't use it in production

- `controller` the controllers of the application, creat controllers here

- `model` the ORM models of the application, create models here

- `service` the services of the application, create services here

- `util` the utilities of the application, create utilities here
    - `exception.py` the exceptions of the application
    - `logger.py` a logger implement for the application
    - `security.py` security utilities for the application
    - `time.py` a datetime utilities for the application

- `test` the tests of the application, create tests here