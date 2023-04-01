# WALL-O Server

This server is a bridge between the Arduino and web application, on one hand, it handle communication over Bluetooth using serial ports, and on the other, it uses a REST API to serve data to the web application. This server also store all the data in CSV files each time a run is in progress.

## Requirements

> The server is only working on Windows system and require Python 3.10 or greater.

This application also require several librairies listed below:

- [FastAPI](https://pypi.org/project/fastapi/)
- [Uvicorn](https://pypi.org/project/uvicorn/)
- [PySerial](https://pypi.org/project/pyserial/)

## Setup

The setup of the server can be done with two different methods. The first one use a script to setup automatically the server and the second one require to use commands manually to setup the server.

First, no matter the method you select, you need to pair the Bluetooth device of the robot. In order to do this, go in the Bluetooth setting, add a device, the Bluetooth module of the robot should appear as `HC-05`. Note that it may take up to one minute for the device to appear in the list.

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
