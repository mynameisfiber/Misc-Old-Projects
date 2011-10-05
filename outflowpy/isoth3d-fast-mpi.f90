module tvd

implicit none
include "omp_lib.h"

DOUBLE PRECISION :: csound=1

CONTAINS

  SUBROUTINE set_num_threads(n) 
    !f2py threadsafe
    !f2py intent(in) n
    INTEGER :: n
    call OMP_SET_NUM_THREADS(n)
  END SUBROUTINE set_num_threads

  subroutine step(u, n, CFL, dt, maxv)
    !f2py threadsafe
    !f2py intent(in) u
    !f2py intent(in) n
    !f2py intent(in) CFL
    !f2py intent(in), optional dt
    !f2py intent(in), optional maxv
    !f2py intent(out) :: u, dt, maxv
    !f2py depend(u) n
    INTEGER :: n, k
    DOUBLE PRECISION, DIMENSION(4,n,n,n) :: u
    DOUBLE PRECISION :: CFL, dt, maxv
    
    !$OMP PARALLEL DO shared(u) private(n,k) &
    !$OMP SCHEDULE(dynamic) REDUCTION(MAX:maxv)
    DO k=1,n
      maxv = max( maxval( abs(u(2,:,:,k)) / u(1,:,:,k) ), &
                  maxval( abs(u(3,:,:,k)) / u(1,:,:,k) ), &
                  maxval( abs(u(4,:,:,k)) / u(1,:,:,k) )  &
                )
    END DO
    !$OMP END PARALLEL DO

    !Calculate the timestep based on the courant condition
    if (dt .eq. 0.0) dt = CFL / (csound+maxv) 
    !perform strang splitting using the hydro only 2nd order TVD
    ! algorithm given by http://arxiv.org/abs/astro-ph/0305088
    call doX(u,n,dt, maxv)
     call doY(u,n,dt, maxv)
      call doZ(u,n,dt, maxv)
      call doZ(u,n,dt, maxv)
     call doY(u,n,dt, maxv)
    call doX(u,n,dt, maxv)
  END subroutine step

  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  SUBROUTINE doX(u,n,dt,maxv)
    !f2py threadsafe
    !f2py intent(in) u
    !f2py intent(in) n
    !f2py intent(in) dt
    !f2py intent(in) maxv
    !f2py intent(out) u
    !f2py depend(u) n
    INTEGER :: n, j, k
    INTEGER, DIMENSION(4) :: reorder = (/1, 2, 3, 4/) 
    DOUBLE PRECISION, DIMENSION(4,n,n,n) :: u; 
    DOUBLE PRECISION :: dt , maxv
    DOUBLE PRECISION, DIMENSION(4,n) :: u1d
    !print*,"starting X"
    ! X-operation -- i of (i,j,k). 
    !$omp parallel do private(u1d, k) shared(u,n,dt, reorder,maxv) DEFAULT(SHARED) schedule(dynamic)
    DO j = 1, n
      DO k = 1, n
       u1d = u(reorder,:,j,k) ! pick out x lines from xz planes
       CALL tvdeuler(u1d, n, dt, maxv)
       u(reorder,:,j,k) = u1d;     
      END DO !k
    END DO !j 
    !print*,"done X"
  END SUBROUTINE doX

  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  SUBROUTINE doY(u,n,dt,maxv)
    !f2py threadsafe
    !f2py intent(in) u
    !f2py intent(in) n
    !f2py intent(in) dt
    !f2py intent(in) maxv
    !f2py intent(out) u
    !f2py depend(u) n
    INTEGER :: n, j, k
    INTEGER, DIMENSION(4) :: reorder = (/1, 3, 2, 4/) !switch vy&vx
    DOUBLE PRECISION, DIMENSION(4,n,n,n) :: u; 
    DOUBLE PRECISION :: dt,maxv
    DOUBLE PRECISION, DIMENSION(4,n) :: u1d
    ! Y-operation -- j of (i,j,k). 
    !$omp parallel do private(u1d, k) shared(u,n,dt,reorder,maxv) DEFAULT(SHARED) schedule(dynamic)
    DO j = 1, n
      DO k = 1, n
       u1d = u(reorder, j,:,k) ! pick out y lines from yz plane
       CALL tvdeuler(u1d, n, dt, maxv)
       u(reorder, j,:,k) = u1d;     
      END DO !k
    END DO !j 
  END SUBROUTINE doY

  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  SUBROUTINE doZ(u,n,dt,maxv)
    !f2py threadsafe
    !f2py intent(in) u
    !f2py intent(in) n
    !f2py intent(in) dt
    !f2py intent(in) maxv
    !f2py intent(out) u
    !f2py depend(u) n
    INTEGER :: n, j, k
    INTEGER, DIMENSION(4) :: reorder = (/1, 4, 3, 2 /) !switch vz&vx
    DOUBLE PRECISION, DIMENSION(4,n,n,n) :: u; 
    DOUBLE PRECISION :: dt,maxv 
    DOUBLE PRECISION, DIMENSION(4,n) :: u1d
    ! Z-operation -- k of (i,j,k). 
    !$omp parallel do private(u1d, k) shared(u,n,dt,reorder,maxv) DEFAULT(SHARED) schedule(dynamic) 
    DO j = 1, n
      DO k = 1, n
       u1d = u(reorder, j,k,:) ! pick out z lines from yz planes
       CALL tvdeuler(u1d, n, dt,maxv)
       u(reorder, j,k,:) = u1d;     
      END DO !k
    END DO !j 
  END SUBROUTINE doZ

  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  RECURSIVE SUBROUTINE tvdeuler(u,n,dt,maxv) 
    !f2py threadsafe
    !f2py intent(in) u
    !f2py intent(in) n
    !f2py intent(in) dt
    !f2py intent(in) maxv
    !f2py intent(out) u
    !f2py depend(u) n
    INTEGER :: n, k
    DOUBLE PRECISION :: dt, maxv, c
    DOUBLE PRECISION, DIMENSION(4,n) :: u, uhalf, flux 
    DOUBLE PRECISION, DIMENSION(4,n) :: fluxR, fluxL
    DOUBLE PRECISION, DIMENSION(4,n) :: fwr, fwl
    !print*,"starting tvdeuler"
    uhalf = u  
    DO k = 2,1,-1 !R-K stepper
      !v=u(:,2)/u(:,1);  !rhovx/rho 
      c = maxv+csound ! MAXVAL(abs(v) + csound); 
      flux = getflux(uhalf,n); 
      ! TVD is only proven for constant c. One can also try tricks like 
      ! dividing fluxes by some function (e.g., c) to smooth them out, 
      ! THEN DOing tvd on them, THEN multiplying them by c to reconstruct new 
      ! versions. (Not implemented now.)
      !fwr= wr*cc;     fwl= -wl*cc; 
      fwr= u*c+flux;     fwl= flux-u*c; 
      fluxR = tvdflux(fwr,n); 
      fluxL = cshift(reverse(tvdflux(reverse(fwl,n),n),n),1,2);  
      !fluxL = CSHIFT(fluxR,-1,2)
      flux = (fluxR + fluxL)/2; !flux(n,:) = 0
      !uhalf = u-(flux-cshift(flux,-1,1))*dt/k;
      uhalf(2:n-1,:) = u(:,2:n-1)-(flux(:,2:n-1)-flux(:,1:n-2))*dt/k;
    END DO !k
!      if (minval(uhalf(ghost+1:n-ghost,1)) .lt. 0) then
!        WRITE(6,*),"k=",k
!        call debugoutput(uhalf,u,flux,fluxR,fluxL,n)
!      end if
    u = uhalf; 
    !print*,"done tvdeuler"
  END SUBROUTINE tvdeuler

  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  function reverse(a,n) result(reversed)
    !f2py threadsafe
    !f2py intent(in) a
    !f2py intent(in) n
    !f2py intent(out) reversed
    !f2py depend(n) a
    INTEGER :: n
    DOUBLE PRECISION ::  a(4,n)
    DOUBLE PRECISION, DIMENSION(4,n) :: reversed 
    !print*,"starting reverse"
    reversed(:,:) = a(:,n:1:-1)
    !print*,"done reverse"
  END function reverse

  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  function tvdflux(f,n) result(flux) 
    !f2py threadsafe
    !f2py intent(in) f
    !f2py intent(in) n
    !f2py intent(out) flux
    !f2py depend(n) f
    !rightward flux -> tvd, 2d-order in x
    INTEGER :: n
    DOUBLE PRECISION, DIMENSION(4,n) :: f
    DOUBLE PRECISION, DIMENSION(4,n) :: flux, fr, fl, r, psi
    !print*,"starting tvdflux"
    fr = (cshift(f,1,2)-f)/2      ! deltaflux-right
    fl = (f - cshift(f,-1,2))/2   ! deltaflux-left
    r=0
    where (fr*fl>0) r = fl/fr; 
    !psi = (r+abs(r))/(1+r)        !van Leer
    psi = max(0.,min(abs(r),1.));   !minmod
    ! psi = max(0., min(2*r,1.),min(r,2.)); !superbee
    flux = f + psi*fr; 
    !print*,"done tvdflux"
  END function tvdflux

  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  function getflux(u,n) result(flux)!derive physical flux from state --EULER
    !f2py threadsafe
    !f2py intent(in) u
    !f2py intent(in) n
    !f2py intent(out) flux
    !f2py depend(u) n
    INTEGER :: n
    DOUBLE PRECISION, DIMENSION(4,n) :: u
    DOUBLE PRECISION, DIMENSION(4,n) :: flux
    DOUBLE PRECISION, DIMENSION(n) :: v 
    !print*,"starting getflux"

    v=u(2,:)/u(1,:);
    flux(1,:) = u(2,:); 
    flux(2,:) = u(2,:)*v + u(1,:)*csound*csound; 
    flux(3,:) = u(3,:)*v;  ! passive transport of rho v_y 
    flux(4,:) = u(4,:)*v;  ! passive transport of rho v_z
    !print*,"done getflux"
  END function getflux
  
end module tvd
