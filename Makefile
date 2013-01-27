all: build test docs

install:
	python setup.py install --prefix=$(PWD)/install

test:
	python setup.py test

build:
	python setup.py build

docs:
	python setup.py doc

clean:
	python setup.py clean
