from simframe.integration import AbstractScheme

# Butcher coefficients
a20, a21     = 1/4, 1/4
b0 , b1, b2  = 1/6, 1/6, 2/3
c2           = 1/2


def _f_expl_3_ssprk(x0, Y0, dx, *args, **kwargs):
    """Explicit 3rd-order Strong Stability Preserving Runge-Kutta method
    
    Parameters
    ----------
    x0 : Intvar
        Integration variable at beginning of scheme
    Y0 : Field
        Variable to be integrated at the beginning of scheme
    dx : IntVar
        Stepsize of integration variable
    args : additional positional arguments
    kwargs : additional keyworda arguments
        
    Returns
    -------
    dY : Field
        Delta of variable to be integrated
        
    Butcher tableau
    ---------------
      0  |  0   0   0
      1  |  1   0   0
     1/2 | 1/4 1/4  0
    -----|-------------
         | 1/6 1/6 2/3
    """
    k0 = Y0.derivative(x0        , Y0                       )
    k1 = Y0.derivative(x0 +    dx, Y0 +      k0          *dx)
    k2 = Y0.derivative(x0 + c2*dx, Y0 + (a20*k0 + a21*k1)*dx)
    
    return dx*(b0*k0 + b1*k1 + b2*k2)

expl_3_ssprk = AbstractScheme(_f_expl_3_ssprk, description="Explicit 3rd-order Strong Stability Preserving Runge-Kutta method")