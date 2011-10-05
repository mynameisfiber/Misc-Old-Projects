all: hlleuler.so hllrk.so hllrkfluxlimit.so hllrkfluxlimit.so hlleuler2d.so hllrk2d.so hllrkfluxlimit2d.so

hllrkfluxlimit2d.so: hllrkfluxlimit2d.f90
	f2py -c -m hllrkfluxlimit2d --opt="-O3" --f90flags="-Wall -fopenmp" -lgomp -DF2PY_REPORT_ON_ARRAY_COPY=100 hllrkfluxlimit2d.f90

hllrk2d.so: hllrk2d.f90
	f2py -c -m hllrk2d --opt="-O3" --f90flags="-Wall -fopenmp" -lgomp hllrk2d.f90

hlleuler2d.so: hlleuler2d.f90
	f2py -c -m hlleuler2d --opt="-O3" --f90flags="-Wall -fopenmp" -lgomp hlleuler2d.f90

hlleuler.so: hlleuler.f90
	f2py -c -m hlleuler --opt="-O3" hlleuler.f90

hllrk.so: hllrk.f90
	f2py -c -m hllrk --opt="-O3" hllrk.f90

hllrkfluxlimit.so: hllrkfluxlimit.f90
	f2py -c -m hllrkfluxlimit --opt="-O3" hllrkfluxlimit.f90

clean:
	rm -rf hllrk.so hlleuler.so hllrkfluxlimit.so hlleuler2d.so hllrk2d.so hllrkfluxlimit2d.so
