PYTHONVERSION=python2
#PYTHONVERSION=python

EXECUTABLE=main.py

all : run

run: cpp
	python2 $(EXECUTABLE)

cpp:
	g++ -c -fPIC GLShadow/shadow_volume.cpp -std=c++11 -o GLShadow/shadow_volume.o
	g++ -shared -Wl,-soname,shadow_volume.so -o GLShadow/shadow_volume.so GLShadow/shadow_volume.o

.PHONY: clean

clean:
	find -name "*.pyc" -type f -delete

