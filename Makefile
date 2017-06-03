env:
	$(PYVENV)  env
	($(INVENV) pip install -r requirements.txt )

# Many recipes need to be run in the virtual environment, 
# so run them as $(INVENV) command
PYVENV = pyvenv
INVENV = . env/bin/activate ;

run:	env
	($(INVENV) python3 flask_main.py ||  true )

test:	env
	$(INVENV) nosetests

clean:
	rm -rf env
	rm -rf *.pyc
	rm -rf __pycache__

veryclean:
	make clean
	rm -rf CONFIG.py

