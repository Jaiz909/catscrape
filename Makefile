install: catscrape setup.py
	./setup.py install

develop: catscrape setup.py
	./setup.py develop

test:
	nosetests

zip: catscrape
	mkdir -p dist
	echo '#!/usr/bin/env python' > dist/catscrape
	cd catscrape && zip -r ../dist/catscrape.zip *
	cat dist/catscrape.zip >> dist/catscrape
	rm dist/catscrape.zip
	chmod +x dist/catscrape

