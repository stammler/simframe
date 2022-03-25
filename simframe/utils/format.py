import numpy as np
from simframe.utils.color import colorize


def byteformat(b):
    """Function returns a formatted string for given memory usage.

    Parameters
    ----------
    b : float
        Memory usage in bytes

    Returns
    -------
    s : string
        Formatted string of memory usage
    """

    # Check for negative inputs
    if b < 0:
        raise ValueError("Negative memory usage.")

    # Zero memory usage. This case should technically never happen.
    if 1.*b == 0.:
        return "    < 1 KiB"

    lables = {0: "  B", 1: "KiB", 2: "MiB", 3: "GiB", 4: "TiB",
              5: "PiB", 6: "EiB", 7: "ZiB", 8: "YiB"}
    # Exponent to the base of 1024
    e = np.log(1.*b) / np.log(1024.)
    # Keep exponent inbound of labls
    ef = np.minimum(int(np.floor(e)), 8)

    # Do not show values smaller than 1 KiB
    if ef < 0:
        return "    < 1 " + lables[0]

    # Create formatted string
    s = "{:3.0f} {:}".format(b/1024.**ef, lables[ef])

    # Color string red if more than 100 MiB
    if e >= np.log(100.*1024.**2)/np.log(1024.):
        s = colorize(s, "red")
    # Color string yellow if more than 10 MiB
    elif e >= np.log(10.*1024.**2)/np.log(1024.):
        s = colorize(s, "yellow")

    return s
