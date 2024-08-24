### Hexlet tests and linter status:
[![Actions Status](https://github.com/Pavel-Kr/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Pavel-Kr/python-project-52/actions)
[![Build Status](https://github.com/Pavel-Kr/python-project-52/actions/workflows/build.yml/badge.svg)](https://github.com/Pavel-Kr/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/549890e87e6337b69c25/maintainability)](https://codeclimate.com/github/Pavel-Kr/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/549890e87e6337b69c25/test_coverage)](https://codeclimate.com/github/Pavel-Kr/python-project-52/test_coverage)

# Task Manager

This is a simple task manager website, similar to [Redmine](https://www.redmine.org/).

This project is hosted on [Render](https://render.com/).

Link to the website: https://python-project-52-tyby.onrender.com/.

### How to run locally

Firstly, you need to install Poetry. Official installation guide can be found [here](https://python-poetry.org/docs/#installation).

Then run `make install`. This will install all necessary dependencies and apply all database migrations. After this, you can run `make dev` to start a development server, or `make run-server`, to run a production server.