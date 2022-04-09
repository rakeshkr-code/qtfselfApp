@echo off

rem This is a Comment
echo "======================================================================"
echo "Welcome to to the setup. This will setup the local virtual env." 
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"

if exist ".env" (
    echo "Enabling virtual env"
) else (
	echo "No Virtual env. Please run setup.sh first"
    exit N
    ::echo "creating .env and install using pip"
	::python -m venv .env
)
	rem python -m venv .env
    rem python3.7 -m venv .env

:: Activate virtual env
:: . .env/Scripts/activate
CALL .env\Scripts\activate

set ENV=development
python app.py

:: Work done. so deactivate the virtual env
call deactivate


pause