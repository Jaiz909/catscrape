install: catscrape setup.py
	./setup.py install

develop: catscrape setup.py
	./setup.py develop

dependencies: requirements.txt
	pip install -r requirements.txt

test: dependencies
	nosetests

zip: catscrape dependencies
	mkdir -p dist
	echo '#!/usr/bin/env python' > dist/catscrape
	cd catscrape && zip -r ../dist/catscrape.zip *
	cat dist/catscrape.zip >> dist/catscrape
	rm dist/catscrape.zip
	chmod +x dist/catscrape

binary: zip dependencies
	echo "Building binary"

clean:
	rm -rf dist
