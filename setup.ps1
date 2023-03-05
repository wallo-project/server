param (
    [switch]$run
)

if (-not $run) {
    # Try to create the virtual environment
    Write-Output "Creating Python virtual environement..."
    Invoke-Expression "python -m venv .venv"

    # Activate the virtual environment
    Write-Output "Activating Python virtual environement..."
    if (-not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
        Write-Error "Could not execute .venv\Scripts\Activate.ps1"
        exit 1
    }

    . ".\.venv\Scripts\Activate.ps1"

    # updating pip
    Write-Output "Updating pip..."
    if (-not (Invoke-Expression "python.exe -m pip install --upgrade pip")) {
        Write-Error "Failed to update pip"
        exit 1
    }


    # Install requirements
    Write-Output "Installing libraries..."
    if (-not (Invoke-Expression "pip install -r requirements.txt")) {
        Write-Error "Failed to install requirements"
        exit 1
    }
    Write-Output "Server is set up. You can run it using setup.ps1 -run"
}

if ($run) {
    if (-not (Invoke-Expression "python src/main.py")) {
        Write-Error "Failed to run main.py"
        exit 1
    }
}

