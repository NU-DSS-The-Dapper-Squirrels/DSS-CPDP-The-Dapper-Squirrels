# Data Integration on CPDP Refresh Data

## Table of Content

- [Overview](#overview)
- [Prerequisite](#prerequisite)
  - [System and Python](#system-and-python)
  - [Dependency Installation](#dependency-installation)
- [Running the Program](#running-the-program)

## Overview

The overall structure of the directory is as follows:

```bash
.
├── Pipfile
├── Pipfile.lock
├── README.md
├── output
│   ├── trr-actionresponse.csv
│   ├── trr-charge.csv
│   ├── trr-subjectweapon.csv
│   ├── trr-trr.csv
│   ├── trr-trrstatus.csv
│   └── trr-weapondischarge.csv
├── requirements.txt
└── src
    ├── data
    │   ├── data_officer.csv
    │   ├── data_policeunit.csv
    │   ├── trr_actionresponse_refresh.csv
    │   ├── trr_charge_refresh.csv
    │   ├── trr_subjectweapon_refresh.csv
    │   ├── trr_trr_refresh.csv
    │   ├── trr_trrstatus_refresh.csv
    │   └── trr_weapondischarge_refresh.csv
    └── data_integration.py
```

The `output/` directory contains all the output from the source code. The `src/`
directory contains the python program and the input datas. The program `data_integration.py`
takes data in `data/` directory.

## Prerequisite

### System and Python

This application was built on MacOS, the Python version was 3.9.
[Pyenv](https://github.com/pyenv/pyenv) is recommended for Python version management.
Here is a good [tutorial](https://realpython.com/intro-to-pyenv/) on how to install
Pyenv on your system.

[Pipenv](https://github.com/pypa/pipenv) was used to manage the Python dependencies,
here is a good [tutorial](https://realpython.com/pipenv-guide/) on how to install
and use Pipenv.

### Dependency Installation

**1. pipenv**

To install the dependencies, use `pipenv install` to install from Pipfile. If you
want to install by importing the `requirement.txt`, use
`pipenv install -r path/to/requirements. txt` to install.

The complete dependency list is as follows, please also refer to [Pipfile](Pipfile)
and [requirement.txt](requirement.txt).

```
pandas = "*"
numpy = "*"
```

**2. virtualenv**

We need to create a virtual environment first:

```bash
python3 -m venv --system-site-packages ./venv
```

Then, activate the virtual environment:

```bash
source ./venv/bin/activate
```

Finally, install the requirements:

```bash
pip3 install -r requirements.txt
```

After you are done with the project, run:

```bash
deactivate
```

**3. Anaconda**

First we create a virtual environment by using conda, you
should replace x with the python version you have:

```bash
conda create -n data_integration_env python=3.x
```

Then, we activate the environment:

```bash
conda activate data_integration_env
```
Finally, we install the environments:

```bash
while read requirement; do conda install --yes $requirement; done < requirements.txt 2>error.log
```

If there are uninstalled packages, the error message can be
found in error.log

After you are done with the project, run:

```bash
conda deactivate
```

## Running the Program

**1. Run by pipenv**

Run the following commend under `src/`:

```bash
pipenv run python data_integration.py
```

**2. Anaconda and virtualenv**

Run the following commend under `src/` based on your python
system path:

```bash
python data_integration.py
```
or
```bash
python3 data_integration.py
```
