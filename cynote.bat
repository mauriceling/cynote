
if exist web2py.exe goto web2pyexe
if exist web2py.py goto web2py

:web2pyexe
web2py.exe --config=options.py

:web2py
python web2py.py --ip=127.0.0.1 --port=8000 --password=admin