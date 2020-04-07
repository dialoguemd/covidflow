# covidflow

Flow for covid-19 assessment, navigation and follow-ups.

## Development

### Make

Make is expected to be installed on the developer workstation.

### Docker

Docker is expected to be installed on the developer workstation.

- _Windows_: Docker Desktop 2.1.0.5 is recommended
- _Linux_: docker >= 19.03.5 and docker-compose >= 1.24.0

### Python version

Python version 3.6.8 is required to properly install Rasa components. It should be installed using [pyenv](https://github.com/pyenv/pyenv).

### Environment initialization

When working in the project for the first time, the Python virtual environment (using `venv`) must be created by performing:

`make init`

### Installing / upgrading libraries

Before beginning to work on the project or whenever a dependency is added / upgraded, it is import to update the Python virtual environment. Dependencies are managed by using `pip` directly since we had a really bad experience with `pipenv`.

#### Application dependencies

Applications dependencies are defined in `requirements.txt` and can be installed using `make install`.

#### Development dependencies

Development dependencies (linters, formatter, etc...) are defined in `requirements-dev.txt` and can be installed using `make install-dev`.

#### Rasa SDK

To allow the IDE to perform autocompletion and to run unit tests, Rasa SDK must also be installed in your virtual environment. This can be performed by using `make install-rasa-sdk` and is usually a one-time deal unless you upgrade Rasa SDK version which is defined in the `Makefile`.

## Instructions for running the bot

### Prerequisites

Windows / Mac: [Docker Desktop](https://www.docker.com/products/docker-desktop) must be installed on your machine.

### Train the models

Before running the bot, the model must be trained.

Run the following commands:

```
make train-en
make train-fr
```

### Interact with the bot

Before launching the bot, you must copy the `.env.example` file to `.env` and edit it to properly set the Docker environment variables. Further instructions on how to modify in are included in the file.

To start all services in a single step, run the following command:

```
docker-compose up
```

This will start the following services:

- _core-en_(`localhost:5005`): The Rasa application with the English model.
- _core-fr_(`localhost:5006`): The Rasa application with the French model.
- _action_server_(`localhost:5055`): The Rasa action server that executes forms and custom code.
- _tracker_store_(`localhost:5432`): The PostgreSQL backed Rasa tracker store.

The tracker store database is volatile.

#### Using rasa shell

You can still access the bot using `rasa shell` by spawning a new core instance like this:

`make shell-en` or `make shell-fr` depending on the model you want to use.
