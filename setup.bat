@echo off

set "python=python"
set "venv=.venv"
set "activate=%venv%\Scripts\activate.bat"
set "requirements=requirements.txt"
set "main=src\main.py"

if "%1" neq "run" (
    rem Check if Python is installed
    %python% --version >nul 2>&1 || (
        echo Python is required to run this script
        exit /b 1
    )

    rem Create virtual environment
    echo Creating Python virtual environement...
    if not exist %venv% (
        %python% -m venv %venv% || (
            echo Failed to create virtual environment
            exit /b 1
        )
    )

    rem Activate virtual environment
    echo Activating Python virtual environement...
    call %activate% || (
        echo Failed to activate virtual environment
        exit /b 1
    )

    echo Updating pip...
    python.exe -m pip install --upgrade pip || (
        echo Failed to update pip
        exit /b 1
    )

    rem Install requirements
    echo Installing libraries...
    pip install -r %requirements% || (
        echo Failed to install requirements
        exit /b 1
    )
)
rem Run main.py if requested
if "%1"=="run" (
    call %activate% || (
        echo Failed to activate virtual environment
        exit /b 1
    )

    %python% %main% || (
        echo Failed to run main.py
        exit /b 1
    )
)

echo Server is set up. You can run it using setup.bat run
