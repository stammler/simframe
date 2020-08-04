from simframe.integration import AbstractScheme

def _f_expl_1_euler(dx, Y):
    return dx*Y.derivative(Y)

expl_1_euler = AbstractScheme(_f_expl_1_euler, description="Explicit 1st-order Euler")