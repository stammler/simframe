"""This package contains pre-defined instances of integration schemes that can be used in ``simframe``.
The naming convention is ``<expl/impl>_<order>_<name>(<_additonal>)``.

For example: The fifth-order adaptive Cash-Karp scheme is ``expl_5_cash_karp_adptv``, the 1st-order implicit Euler
scheme using a GMRES solver is ``impl_1_euler_gmres``."""

from simframe.integration.schemes.expl_1_euler import expl_1_euler
from simframe.integration.schemes.expl_2_fehlberg_adptv import expl_2_fehlberg_adptv
from simframe.integration.schemes.expl_2_heun import expl_2_heun
from simframe.integration.schemes.expl_2_heun_euler_adptv import expl_2_heun_euler_adptv
from simframe.integration.schemes.expl_2_midpoint import expl_2_midpoint
from simframe.integration.schemes.expl_2_ralston import expl_2_ralston
from simframe.integration.schemes.expl_3_bogacki_shampine_adptv import expl_3_bogacki_shampine_adptv
from simframe.integration.schemes.expl_3_gottlieb_shu_adptv import expl_3_gottlieb_shu_adptv
from simframe.integration.schemes.expl_3_heun import expl_3_heun
from simframe.integration.schemes.expl_3_kutta import expl_3_kutta
from simframe.integration.schemes.expl_3_ralston import expl_3_ralston
from simframe.integration.schemes.expl_3_ssprk import expl_3_ssprk
from simframe.integration.schemes.expl_4_38rule import expl_4_38rule
from simframe.integration.schemes.expl_4_ralston import expl_4_ralston
from simframe.integration.schemes.expl_4_runge_kutta import expl_4_runge_kutta
from simframe.integration.schemes.expl_5_cash_karp_adptv import expl_5_cash_karp_adptv

from simframe.integration.schemes.impl_1_euler_direct import impl_1_euler_direct
from simframe.integration.schemes.impl_1_euler_gmres import impl_1_euler_gmres
from simframe.integration.schemes.impl_2_midpoint_direct import impl_2_midpoint_direct

from simframe.integration.schemes.update import update

__all__ = ["expl_1_euler",
           "expl_2_fehlberg_adptv",
           "expl_2_heun",
           "expl_2_heun_euler_adptv",
           "expl_2_midpoint",
           "expl_2_ralston",
           "expl_3_bogacki_shampine_adptv",
           "expl_3_gottlieb_shu_adptv",
           "expl_3_heun",
           "expl_3_kutta",
           "expl_3_ralston",
           "expl_3_ssprk",
           "expl_4_38rule",
           "expl_4_ralston",
           "expl_4_runge_kutta",
           "expl_5_cash_karp_adptv",

           "impl_1_euler_direct",
           "impl_1_euler_gmres",
           "impl_2_midpoint_direct",

           "update"
           ]
