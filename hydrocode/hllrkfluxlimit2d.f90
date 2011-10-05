MODULE hllrkfluxlimit2d

  implicit none
  include "omp_lib.h"

  DOUBLE PRECISION :: g = 1.4 !gamma
  DOUBLE PRECISION :: CFL = 0.8
  DOUBLE PRECISION :: maxalphax = 0.0
  DOUBLE PRECISION :: maxalphay = 0.0
  DOUBLE PRECISION :: dx = 0.0
  DOUBLE PRECISION :: dy = 0.0
  DOUBLE PRECISION :: dt = 0.0
  DOUBLE PRECISION :: theta = 1.5
  DOUBLE PRECISION :: t = 0.0

  CONTAINS

  SUBROUTINE init(ig, idx, idy, iCFL, itheta)
    !f2py DOUBLE PRECISION, intent(optional) :: ig, idx, iCFL, itheta
    DOUBLE PRECISION :: ig, idx, idy, iCFL, itheta

    dx = idx
    dy = idy
    g = ig
    CFL = iCFL
    dt = 0.0
    maxalphax = 0.0
    maxalphay = 0.0
    t = 0.0
    theta = itheta
  END SUBROUTINE

  SUBROUTINE step(u,n, m)
    !f2py DOUBLE PRECISION, DIMENSION(n,m, 4), INTENT(in,out) :: u
    !f2py INTEGER, INTENT(hide) :: n, m
    DOUBLE PRECISION, DIMENSION(n,m, 4) :: u, unew
    DOUBLE PRECISION                    :: lCFL
    INTEGER                 :: n, m

    lCFL = CFL
666 continue

    maxalphax = 0.0
    maxalphay = 0.0

    unew = L(u,n,m,1,maxalphax)/dx
    unew = unew + L(u,n,m,2,maxalphay)/dy
    dt = CFL * dx * dy / (dy * maxalphax + dx * maxalphay)
    unew = u - dt * unew

    unew = 0.75 * u + 0.25 * unew + 0.25 * dt * &
           (                                    &
            L(u,n,m,1,maxalphax)/dx +           &
            L(u,n,m,2,maxalphay)/dy             &
           )                                    

    IF (maxalphax * dt / dx + maxalphay * dt / dy .ge. 1.0) THEN
      PRINT*,"Courant condition failed... trying again"
      lCFL = lCFL / 2
      GOTO 666
    END IF

    unew = 1./3. * u + 2./3. * unew + 2./3. * dt * &
              (                                    &
               L(u,n,m,1,maxalphax)/dx +           &
               L(u,n,m,2,maxalphay)/dy             &
             )                                    

    IF (maxalphax * dt / dx + maxalphay * dt / dy .ge. 1.0) THEN
      PRINT*,"Courant condition failed... trying again"
      lCFL = lCFL / 2
      GOTO 666
    END IF

    u = unew

    t = t + dt

  END SUBROUTINE

  FUNCTION L(u,n,m,dir,maxalpha) result(Lx)
    DOUBLE PRECISION, DIMENSION(n,m, 4) :: u, Lx
    DOUBLE PRECISION, DIMENSION(n, 4)   :: FHLLx
    DOUBLE PRECISION                    :: maxalpha
    INTEGER                 :: dir, n, m, i

    if (dir .eq. 1) THEN
      !$OMP PARALLEL DO SHARED(Lx,u,n) PRIVATE(FHLLX,i) &
      !$OMP REDUCTION(MAX:maxalpha) DEFAULT(none) SCHEDULE(dynamic)
      do i=1,n
        FHLLx = gethllflux(u(i,:,:),n,maxalpha)
        Lx(i,:,:) = CSHIFT(FHLLx, -1, 1) - FHLLx
      end do
    else if (dir .eq. 2) THEN
      !$OMP PARALLEL DO SHARED(Lx,u,m) PRIVATE(FHLLX,i) &
      !$OMP REDUCTION(MAX:maxalpha) DEFAULT(none) SCHEDULE(dynamic)
      do i=1,m
        FHLLx = gethllflux(u(:,i,(/ 1, 3, 2, 4 /)),m,maxalpha)
        Lx(:,i,(/ 1, 3, 2, 4 /)) = CSHIFT(FHLLx, -1, 1) - FHLLx
      end do
    end if
    
    return
  END FUNCTION

  FUNCTION gethllflux(u,n,maxalpha) result(FHLL)
    DOUBLE PRECISION, DIMENSION(n, 4) :: u,pl,pr, ul, ur, FHLL, ap, am
    DOUBLE PRECISION, DIMENSION(n, 6) :: Fl, Fr
    DOUBLE PRECISION, DIMENSION(n, 2) :: alpha
    DOUBLE PRECISION                  :: maxalpha
    INTEGER               :: n

    CALL fluxlimit(u,pl,pr,n)

    ul = prim2conserv(pl, n)
    ur = prim2conserv(pr, n)

    Fl = getflux(ul,n)
    Fr = getflux(ur,n)

    !               v_i---\       /---c_s
    alpha(:,1) = MAX(-Fl(:,5)+Fl(:,6), -Fr(:,5)+Fr(:,6))
    alpha(:,2) = MAX( Fl(:,5)+Fl(:,6),  Fr(:,5)+Fr(:,6))
    where (alpha .lt. 0) alpha = 0

    maxalpha = MAX(maxalpha,MAXVAL(alpha))

    am = SPREAD(alpha(:,1), 2, 4)
    ap = SPREAD(alpha(:,2), 2, 4)

    FHLL = ( ap * Fl(:,1:4)                    +     &
             am * Fr(:,1:4)                    -     &
             ap * am * (ur - ul)                     &
           )                                   /     &
           (ap + am)

    return
  END FUNCTION

  SUBROUTINE fluxlimit(u, pl, pr, n)
    DOUBLE PRECISION, DIMENSION(n, 4) :: u,p,pl,pr
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

  END SUBROUTINE

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

  FUNCTION prim2conserv(p,n) result(u)
    !f2py DOUBLE PRECISION, DIMENSION(n, 4), INTENT(in) :: p
    !f2py INTEGER, INTENT(hide) :: n
    DOUBLE PRECISION, DIMENSION(n, 4) :: p, u
    INTEGER               :: n

    u(:,1) = p(:,1)                                                !density
    u(:,2) = p(:,1) * p(:,2)                                       !momentum
    u(:,3) = p(:,1) * p(:,3)                                       !momentum
    u(:,4) = p(:,4) / (g - 1) + .5 * p(:,1) * (p(:,2) * p(:,2)+ &  !energy
                                               p(:,3) * p(:,3))

    return
  END FUNCTION

  FUNCTION conserv2prim(u,n) result(p)
    !f2py DOUBLE PRECISION, DIMENSION(n, 4), INTENT(in) :: u
    !f2py INTEGER, INTENT(hide) :: n
    DOUBLE PRECISION, DIMENSION(n, 4) :: p, u
    INTEGER               :: n

    p(:,1) = u(:,1)                             !density
    p(:,2) = u(:,2) / u(:,1)                    !velocity
    p(:,3) = u(:,3) / u(:,1)                    !velocity
    p(:,4) = eqOfState(u,n)                     !pressure

    return
  END FUNCTION

  FUNCTION eqOfState(u,n) result(P)
    DOUBLE PRECISION, DIMENSION(n, 4) :: u
    DOUBLE PRECISION, DIMENSION(n)    :: P
    INTEGER               :: n

    P = (g - 1) * (u(:,4) - .5 * (u(:,2)*u(:,2) + u(:,3)*u(:,3)) / u(:,1))
    return
  END FUNCTION

  FUNCTION minmod(a,b,c,n) result(d)
    DOUBLE PRECISION, DIMENSION(n,4) :: a,b,c,d
    INTEGER              :: n, i, j

    !$OMP PARALLEL DO SHARED(d,a,b,c,n) PRIVATE(i,j) &
    !$OMP DEFAULT(none) SCHEDULE(dynamic)
    do i=1,n
      do j=1,4
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
    
END MODULE hllrkfluxlimit2d
