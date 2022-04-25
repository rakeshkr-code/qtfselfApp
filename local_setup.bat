@echo off

rem This is a Comment
echo "======================================================================"
echo "Welcome to to the setup. This will setup the local virtual env." 
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"

if exist ".env" (
    echo ".env folder exists. Installing using pip"
) else (
    echo "creating .env and install using pip"
	python -m venv .env
)
	rem python -m venv .env
    rem python3.7 -m venv .env

rem Activate virtual env
:: . .env/Scripts/activate
CALL .env\Scripts\activate

:: Upgrade the PIP
:: pip install --upgrade pip
pip install -r requirements.txt
:: Work done. so deactivate the virtual env
deactivate


pause