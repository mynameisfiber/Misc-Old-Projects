tvd:
	f2py -c -m tvd --f90flags="-fopenmp" --opt="-O3" --noarch -lgomp --fcompiler=gnu95 isoth3d-fast-mpi.f90

clean:
	rm -rf tvd.so
