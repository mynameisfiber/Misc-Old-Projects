MODULE hlleuler

  implicit none

  REAL :: g = 1.4 !gamma
  REAL :: CFL = 0.8
  REAL :: maxalpha = 0.0
  REAL :: dx = 0.0
  REAL :: dt = 0.0
  REAL :: t = 0.0

  CONTAINS

  SUBROUTINE init(ig, idx, iCFL)
    !f2py REAL, intent(optional) :: ig, idx, iCFL
    REAL :: ig, idx, iCFL

    dx = idx
    g = ig
    CFL = iCFL
    dt = 0.0
    maxalpha = 0.0
    t = 0.0
  END SUBROUTINE

  SUBROUTINE step(u,n)
    !f2py REAL, DIMENSION(n, 3), INTENT(in,out) :: u
    !f2py INTEGER, INTENT(hide) :: n
    REAL, DIMENSION(n, 3) :: u, FHLLR, FHLLL
    INTEGER               :: n

    FHLLR = gethllflux(u,n)
    FHLLL = CSHIFT(FHLLR, -1, 1)

    u = u - dt / dx * (FHLLR - FHLLL)

    t = t + dt

  END SUBROUTINE

  function reverse(a,n) result(reversed)
    INTEGER :: n
    REAL ::  a(n,3)
    REAL, DIMENSION(n,3) :: reversed
    reversed(:,:) = a(n:1:-1,:)
    return
  END function reverse


  FUNCTION gethllflux(u,n) result(FHLL)
    REAL, DIMENSION(n, 3) :: u, FHLL, ap, am
    REAL, DIMENSION(n, 5) :: F
    REAL, DIMENSION(n, 2) :: alpha
    INTEGER               :: n

    F = getflux(u,n)

    !               v_i---\       /---c_s
    alpha(:,1) = MAX(-F(:,4)+F(:,5), CSHIFT(-F(:,4)+F(:,5),+1,1))
    alpha(:,2) = MAX( F(:,4)+F(:,5), CSHIFT( F(:,4)+F(:,5),+1,1))
    where (alpha .lt. 0) alpha = 0

    maxalpha = MAXVAL(alpha)
    dt = CFL * dx / maxalpha

    am = SPREAD(alpha(:,1), 2, 3)
    ap = SPREAD(alpha(:,2), 2, 3)

    FHLL = (                                       &
            ap * F(:,1:3)                    +     &
            am * CSHIFT(F(:,1:3),+1,1)       -     &
            ap * am * (CSHIFT(u,+1,1) - u)         &
           )                                 /     &
           (ap + am)

    return
  END FUNCTION

  FUNCTION getflux(u,n) result(f)
    REAL, DIMENSION(n, 3) :: u
    REAL, DIMENSION(n, 5) :: f
    REAL, DIMENSION(n)    :: P
    INTEGER               :: n

    P = eqOfState(u,n)

    f(:,4) = u(:,2)/u(:,1)
    f(:,1) = u(:,2)
    f(:,2) = u(:,1) * f(:,4) * f(:,4) + P
    f(:,3) = (u(:,3) + P) * f(:,4)
    f(:,5) = SQRT(g * P / u(:,1))

    return
  END FUNCTION

  FUNCTION eqOfState(u,n) result(P)
    REAL, DIMENSION(n, 3) :: u
    REAL, DIMENSION(n)    :: P
    INTEGER               :: n

    P = (g - 1) * (u(:,3) - .5 * u(:,2) * u(:,2) / u(:,1))
    return
  END FUNCTION
    
END MODULE hlleuler
