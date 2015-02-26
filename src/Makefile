PYTHONVERSION=python2
#PYTHONVERSION=python

EXECUTABLE=main.py

all : run

run:
	python2 $(EXECUTABLE)

cpp:
	g++ -c -fPIC GL/shadow_volume.cpp -std=c++11 -o GL/shadow_volume.o
	g++ -shared -Wl,-soname,shadow_volume.so -o GL/shadow_volume.so GL/shadow_volume.o

.PHONY: clean

clean:
	find -name "*.pyc" -type f -delete

