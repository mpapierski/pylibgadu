test:
	python test_libgadu.py
swig:
	swig -python -I/usr/local/include libgadu.i
	python setup.py build
	python setup.py install

