@echo off
title Snake Game Installer

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python 3.4 or higher.
    pause
    exit /b
)

:: Check if requirements.txt exists
if not exist requirements.txt (
    echo requirements.txt not found in the current directory.
    pause
    exit /b
)

:: Check if all dependencies in requirements.txt are installed
echo Checking if dependencies are installed...
python -m pip freeze > installed_packages.txt

for /f "delims=" %%i in (requirements.txt) do (
    findstr /i "%%i" installed_packages.txt >nul
    if %ERRORLEVEL% NEQ 0 (
        echo Dependency "%%i" is not installed. Installing...
        python -m pip install %%i
        if %ERRORLEVEL% NEQ 0 (
            echo Failed to install "%%i".
            pause
            exit /b
        )
    ) else (
        echo "%%i" is already installed.
    )
)

:: Clean up installed packages list
del installed_packages.txt

echo All dependencies are installed successfully!
pause
