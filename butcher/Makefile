run: cybutcher writeup.pdf
	python pybutcher.py

cybutcher: cybutcher.c
	gcc -shared -pthread -fPIC -fwrapv -O3 -ffast-math -frerun-loop-opt -frerun-cse-after-loop -Wall -fno-strict-aliasing -I/usr/include/python2.6/ -o cybutcher.so cybutcher.c 

cybutcher.c: cybutcher.pyx 
	cython cybutcher.pyx

writeup.pdf: writeup.tex
	pdflatex writeup.tex
	rm -rf writeup.aux writeup.log

clean:
	rm -rf *.so cybutcher.c *.pyc writeup.aux writeup.log writeup.pdf
