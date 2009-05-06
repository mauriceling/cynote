set python_directory=c:\Python26

python ez_setup.py
if errorlevel 1 goto setpath
if errorlevel 0 goto check_python_modules

:setpath
set PATH=%PATH%;%python_directory%;%python_directory%/Scripts
python ez_setup.py
goto check_python_modules

:check_python_modules
easy_install "biopython==1.50"
easy_install "pil==1.1.6"
goto run_web2py

:run_web2py
python web2py.py --ip=localhost --port=8000 --password=admin