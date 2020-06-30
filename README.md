# all-repo-cloner
## What
Uses the github api to find all of your hosted repositories then clones them locally. If they already exist then the default branch is updated.


## Requirements
This code assumes you have the following:

* A github API token.
* Python
* Pipenv installed in python.

## Usage

First clone this repo (or copy the 3 files however you want) then:

```
pipenv install
pipenv shell
TOKEN = {YOUR_TOKEN} ./clone.py
```
