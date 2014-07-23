# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.


def packString(string, length=64, packWith=" "):
    return string + (packWith * (length - len(string)))


def noArgs(f):
    """
    because twisted
    """
    return lambda *args, **kwargs: f()

import logging
logger = logging.getLogger()
def walkDictWithRef(d, rd, f, c):
    """
    Walks through a dictionary with a reference dictionary.
    :param d: The dictionary to walk through.
    :param rd: The reference dictionary, containing the default values.
    :param f: The function to call when a leaf is detected. Should accept 4 arguments - the dict, the reference dict, the key and the value.
    :param c: The condition for detecting a leaf. Should accept two arguments - the key and the value, and return a boolean.
    :return dict
    """
    md = {}
    for k, v in rd.items():
        if c(k, v):
            ok, ov = f(d, rd, k, v)
            md[ok] = ov
        else:
            # Does the node exist?
            if k not in d:
                # Does not exist; create an original entry first
                ok, ov = f(rd, rd, k, v)
                md[ok] = ov
                # use the reference dict as original dict
                md[k] = walkDictWithRef(rd[k], rd[k], f, c)
            else:
                md[k] = walkDictWithRef(d[k], rd[k], f, c)
    return md