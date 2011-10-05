MODULE hlleuler2d

  implicit none
  include "omp_lib.h"

  DOUBLE PRECISION :: g = 1.4 !gamma
  DOUBLE PRECISION :: CFL = 0.8
  DOUBLE PRECISION :: maxalphax = 0.0
  DOUBLE PRECISION :: maxalphay = 0.0
  DOUBLE PRECISION :: dx = 0.0
  DOUBLE PRECISION :: dy = 0.0
  DOUBLE PRECISION :: dt = 0.0
  DOUBLE PRECISION :: t = 0.0

  CONTAINS

  SUBROUTINE init(ig, idx, idy, iCFL)
    !f2py DOUBLE PRECISION, intent(optional) :: ig, idx, iCFL
    DOUBLE PRECISION :: ig, idx, idy, iCFL

    dx = idx
    dy = idy
    g = ig
    CFL = iCFL
    dt = 0.0
    maxalphax = 0.0
    maxalphay = 0.0
    t = 0.0
  END SUBROUTINE

  SUBROUTINE step(u,n, m)
    !f2py DOUBLE PRECISION, DIMENSION(n,m, 4), INTENT(in,out) :: u
    !f2py INTEGER, INTENT(hide) :: n, m
    DOUBLE PRECISION, DIMENSION(n,m, 4) :: u, Lx, Ly
    DOUBLE PRECISION, DIMENSION(n, 4)   :: FHLL
    INTEGER                 :: n, m, i, j

    maxalphax = 0.0
    maxalphay = 0.0

    !$OMP PARALLEL DO SHARED(Lx,u,n) PRIVATE(FHLL) REDUCTION(MAX:maxalphax) DEFAULT(none)
    do i=1,n
      FHLL = gethllflux(u(i,:,:),n,maxalphax)
      Lx(i,:,:) = FHLL - CSHIFT(FHLL, -1, 1)
    end do

    !$OMP PARALLEL DO SHARED(Ly,u,n) PRIVATE(FHLL) REDUCTION(MAX:maxalphay) DEFAULT(none)
    do j=1,m
      FHLL = gethllflux(u(:,j,(/ 1,3,2,4 /)),n,maxalphay)
      Ly(:,j,(/ 1,3,2,4 /)) = FHLL - CSHIFT(FHLL, -1, 1)
    end do

    dt = CFL * dx * dy / (dy * maxalphax + dx * maxalphay)
    u = u - dt / dx * Lx - dt / dy * Ly

    t = t + dt

  END SUBROUTINE

  FUNCTION gethllflux(u,n,maxalpha) result(FHLL)
    DOUBLE PRECISION, DIMENSION(n, 4) :: u, FHLL, ap, am
    DOUBLE PRECISION, DIMENSION(n, 6) :: F
    DOUBLE PRECISION, DIMENSION(n, 2) :: alpha
    DOUBLE PRECISION                  :: maxalpha
    INTEGER               :: n

    F = getflux(u,n)

    !               v_i---\       /---c_s
    alpha(:,1) = MAX(-F(:,5)+F(:,6), CSHIFT(-F(:,5)+F(:,6),+1,1))
    alpha(:,2) = MAX( F(:,5)+F(:,6), CSHIFT( F(:,5)+F(:,6),+1,1))
    where (alpha .lt. 0) alpha = 0

    maxalpha = MAX(maxalpha,MAXVAL(alpha))

    am = SPREAD(alpha(:,1), 2, 4)
    ap = SPREAD(alpha(:,2), 2, 4)

    FHLL = (                                       &
            ap * F(:,1:4)                    +     &
            am * CSHIFT(F(:,1:4),+1,1)       -     &
            ap * am * (CSHIFT(u,+1,1) - u)         &
           )                                 /     &
           (ap + am)

    return
  END FUNCTION

  FUNCTION getflux(u,n) result(f)
    DOUBLE PRECISION, DIMENSION(n, 4) :: u
    DOUBLE PRECISION, DIMENSION(n, 6) :: f
    DOUBLE PRECISION, DIMENSION(n)    :: P
    INTEGER               :: n

    P = eqOfState(u,n)

    f(:,5) = u(:,2)/u(:,1)
    f(:,1) = u(:,2)
    f(:,2) = u(:,1) * f(:,5) * f(:,5) + P
    f(:,3) = f(:,5) * u(:,3)
    f(:,4) = (u(:,4) + P) * f(:,5)
    f(:,6) = SQRT(g * P / u(:,1))

    return
  END FUNCTION

  FUNCTION eqOfState(u,n) result(P)
    DOUBLE PRECISION, DIMENSION(n, 4) :: u
    DOUBLE PRECISION, DIMENSION(n)    :: P
    INTEGER               :: n

    P = (g - 1) * (u(:,4) - .5 * u(:,2) * u(:,2) / u(:,1))
    return
  END FUNCTION
    
END MODULE hlleuler2d
