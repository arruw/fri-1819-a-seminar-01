install:
	pip3 install -r requirements.txt

clean:
	rm -f app.zip
	rm -f solution

pack: clean
	cd app && \
	zip -r ../app.zip * && \
	cd .. && \
	sed -i '1s;^;#!/usr/bin/env python3\n;' app.zip && \
	mv app.zip solution && \
	chmod u+x solution

test:
	python3 app/test.py inputs/ 2>&1 | tee "outputs/$(shell date +%s).out"
