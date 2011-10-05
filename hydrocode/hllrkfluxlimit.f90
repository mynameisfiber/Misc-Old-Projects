MODULE hllrkfluxlimit

  implicit none

  REAL :: g = 1.4 !gamma
  REAL :: CFL = 0.8
  REAL :: maxalpha = 0.0
  REAL :: dx = 0.0
  REAL :: dt = 0.0
  REAL :: theta = 1.5
  REAL :: t = 0.0

  CONTAINS

  SUBROUTINE init(ig, idx, iCFL,itheta)
    !f2py REAL, intent(optional) :: ig, idx, iCFL, itheta
    REAL :: ig, idx, iCFL, itheta

    dx = idx
    g = ig
    CFL = iCFL
    theta = itheta
    dt = 0.0
    maxalpha = 0.0
    t = 0.0
  END SUBROUTINE

  SUBROUTINE step(u,n)
    !f2py REAL, DIMENSION(n, 3), INTENT(in,out) :: u
    !f2py INTEGER, INTENT(hide) :: n
    REAL, DIMENSION(n, 3) :: u, unew
    INTEGER               :: n

    unew = u + dt * L(u,n)
    unew = 0.75 * u + 0.25 * unew + 0.25 * dt * L(unew,n)
    u = 1./3. * u + 2./3. * unew + 2./3. * dt * L(unew,n)

    t = t + dt

  END SUBROUTINE

  FUNCTION prim2conserv(p,n) result(u)
    !f2py REAL, DIMENSION(n, 3), INTENT(in) :: p
    !f2py INTEGER, INTENT(hide) :: n
    REAL, DIMENSION(n, 3) :: p, u
    INTEGER               :: n

    u(:,1) = p(:,1)                                             !density
    u(:,2) = p(:,1) * p(:,2)                                    !momentum
    u(:,3) = p(:,3) / (g - 1) + .5 * p(:,1) * p(:,2) * p(:,2)   !energy

    return
  END FUNCTION

  FUNCTION conserv2prim(u,n) result(p)
    !f2py REAL, DIMENSION(n, 3), INTENT(in) :: u
    !f2py INTEGER, INTENT(hide) :: n
    REAL, DIMENSION(n, 3) :: p, u
    INTEGER               :: n

    p(:,1) = u(:,1)                             !density
    p(:,2) = u(:,2) / u(:,1)                    !velocity
    p(:,3) = eqOfState(u,n)                     !pressure

    return
  END FUNCTION

  FUNCTION L(u,n) result(Lu)
    !f2py REAL, DIMENSION(n, 3), INTENT(in,out) :: u
    !f2py INTEGER, INTENT(hide) :: n
    REAL, DIMENSION(n, 3) :: u,p,pL,pR, FHLLR, FHLLL, Lu
    INTEGER               :: n


    p = conserv2prim(u,n)

    pl = p + 0.5 * minmod( theta * (p - CSHIFT(p,-1,1)),             &
                             0.5 * (CSHIFT(p,1,1) - CSHIFT(p,-1,1)), &
                           theta * (CSHIFT(p,1,1) - p),              &
                           n)
    pr = CSHIFT(p,1,1) - 0.5 * minmod( theta * (CSHIFT(p,1,1) - p),             &
                                         0.5 * (CSHIFT(p,2,1) - p),             &
                                       theta * (CSHIFT(p,2,1) - CSHIFT(p,1,1)), &
                                       n)

    FHLLR = gethllflux(pl,pr,n)
    FHLLL = CSHIFT(FHLLR,-1,1)

    Lu = - 1.0 / dx * (FHLLR - FHLLL)

    return
  END FUNCTION

  FUNCTION gethllflux(pl,pr,n) result(FHLL)
    REAL, DIMENSION(n, 3) :: pl,pr, ul, ur, FHLL, ap, am
    REAL, DIMENSION(n, 5) :: Fl, Fr
    REAL, DIMENSION(n, 2) :: alpha
    INTEGER               :: n

    ul = prim2conserv(pl, n)
    ur = prim2conserv(pr, n)

    Fl = getflux(ul,n)
    Fr = getflux(ur,n)

    !               v_i---\       /---c_s
    alpha(:,1) = MAX(-Fl(:,4)+Fl(:,5), -Fr(:,4)+Fr(:,5))
    alpha(:,2) = MAX( Fl(:,4)+Fl(:,5),  Fr(:,4)+Fr(:,5))
    where (alpha .lt. 0) alpha = 0

    maxalpha = MAXVAL(alpha)
    dt = CFL * dx / maxalpha

    am = SPREAD(alpha(:,1), 2, 3)
    ap = SPREAD(alpha(:,2), 2, 3)

    FHLL = ( ap * Fl(:,1:3)                    +     &
             am * Fr(:,1:3)                    -     &
             ap * am * (ur - ul)                     &
           )                                   /     &
           (ap + am)

    return
  END FUNCTION

  FUNCTION minmod(a,b,c,n) result(d)
    REAL, DIMENSION(n,3) :: a,b,c,d
    INTEGER              :: n, i, j

    do i=1,n
      do j=1,3
        if (a(i,j) .gt. 0 .and. b(i,j) .gt. 0 .and. c(i,j) .gt. 0) THEN
          d(i,j) = MIN(a(i,j),b(i,j),c(i,j))
        else if (a(i,j) .lt. 0 .and. b(i,j) .lt. 0 .and. c(i,j) .lt. 0) THEN
          d(i,j) = MAX(a(i,j),b(i,j),c(i,j))
        else
          d(i,j) = 0.0
        end if
      end do
    end do

  return
  END FUNCTION

  FUNCTION fluxlimit(f,n) result(flux)
    REAL, DIMENSION(n,3) :: f, flux
    INTEGER              :: n

    flux = f + 0.5 * minmod(theta * (f - cshift(f,-1,1))/dx,            &
                            0.5 * (CSHIFT(f,+1,1) - CSHIFT(f,-1,1))/dx, &
                            theta * (CSHIFT(f,+1,1) - f)/dx,            &
                            n)

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
    
END MODULE hllrkfluxlimit
