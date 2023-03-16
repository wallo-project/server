# WALL-O Server

This server is a bridge between the Arduino and web application, on one hand, it handle communication over Bluetooth using serial ports, and on the other, it uses a REST API to serve data for the web application. This server also store all the data in CSV files each time a run is in progress.

## Requirements

This application require a Windows system and some several librairies listed below:

- [FastAPI](https://pypi.org/project/fastapi/)
- [Uvicorn](https://pypi.org/project/uvicorn/)
- [PySerial](https://pypi.org/project/pyserial/)

> In order to run the code, Python 3.10 or greater is also required

## Setup

The setup of the server can be done in several ways. and depends on the OS you are running on.

> **The server is only working on Windows system.**

### Automatic setup

If you are using Windows Powershell, use `./setup.ps1` to install all the dependencies. Once done, run the server using `./setup.ps1 -run`.

If you are using Windows Command Prompt, use `./setup.bat` to install all the dependencies. Once done, run the server using `./setup.bat -run`.

### Manual Setup

To setup manually the server follow the instructions below:

- Create the python environment using the command `python venv -m .venv` in your terminal. (you need to go in the project directory)
- Activate the python environment using the command `[path of the project]/.venv/Scripts/Activate.ps1/.bat` (Select .ps1 if you are using Windows Powershell, .bat otherwise)
- Install the libraries using `pip install -r requirements.txt`
- Run the server using `python ./src/main.py`

## Documentation

You can generate the documentation of the project using Doxygen. A Doxyfile is already created and configured for this project. You can also head over [this link](https://wall-o.benjaminpmd.fr/docs) to find informations about the project documentation.
