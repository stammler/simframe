import dill


def writedump(object, filename="object.dmp"):
    """Writes object to dump file

    Parameters
    ----------
    object : object
        object to be written to file
    filename : str, optional, default : "object.dmp"
        path to file to be written"""
    with open(filename, "wb") as dumpfile:
        dill.dump(object, dumpfile)


def readdump(filename):
    """Reads dumpfile and returns ``Frame`` object

    Parameters
    ----------
    filename : str
        Path to file to be read

    Returns
    -------
    obj : object
        object read from dump file

    Notes
    -----
    Only read dump files from sources you trust.
    Malware can be injected."""
    with open(filename, "rb") as dumpfile:
        obj = dill.load(dumpfile)
    return obj
