# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import os
import string
import sys
import time
import traceback

from twisted.internet.threads import deferToThread
from twisted.python import log

def makefile(filename):
    dir = os.path.dirname(filename)
    try:
        os.stat(dir)
    except:
        try:
            os.mkdir(dir)
        except OSError:
            pass
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("")


def makefiles(l):
    for f in l:
        makefile(f)


class _Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(object):
    """
    This class is used to colour and log output.
    It handles colours, printing, and logging to console.log and the individual level log files.
    """
    # TODO Async all methods
    __metaclass__ = _Singleton

    cols = {
        "&0": "",
        "&1": "",
        "&2": "",
        "&3": "",
        "&4": "",
        "&5": "",
        "&6": "",
        "&7": "",
        "&8": "",
        "&9": "",
        "&a": "",
        "&b": "",
        "&c": "",
        "&d": "",
        "&e": "",
        "&f": "",
        "\x01" + "0": "",
        "\x01" + "1": "",
        "\x01" + "2": "",
        "\x01" + "3": "",
        "\x01" + "4": "",
        "\x01" + "5": "",
        "\x01" + "6": "",
        "\x01" + "7": "",
        "\x01" + "8": "",
        "\x01" + "9": "",
        "\x01" + "0": "",
        "\x01" + "a": "",
        "\x01" + "b": "",
        "\x01" + "c": "",
        "\x01" + "d": "",
        "\x01" + "e": "",
        "\x01" + "f": "",
        "\x01" + "g": "",
        }

    nocol = cols

    def __init__(self, debug=False, level=20):
        self.isDebug = debug
        self.logs = {
            "main": "logs/console/console.log",
            "info": "logs/levels/info.log",
            "warn": "logs/levels/warn.log",
            "error": "logs/levels/error.log",
            "critical": "logs/levels/critical.log",
            "debug": "logs/levels/debug.log",
        }
        makefiles([f for f in self.logs.values()])
        try:
            from colorama import Fore, Back, Style
        except ImportError:
            pass
        else:
            self.cols = {
                # Standard Minecraft colours
                "&0": Fore.BLACK + Back.WHITE + Style.NORMAL, # Black, inverse
                "&1": Fore.BLUE + Back.RESET + Style.DIM, # Blue, dark
                "&2": Fore.GREEN + Back.RESET + Style.DIM, # Green, dark
                "&3": Fore.CYAN + Back.RESET + Style.DIM, # Cyan, dark
                "&4": Fore.RED + Back.RESET + Style.DIM, # Red, dark
                "&5": Fore.MAGENTA + Back.RESET + Style.DIM, # Magenta, dark
                "&6": Fore.YELLOW + Back.RESET + Style.DIM, # Yellow, dark
                "&7": Fore.WHITE + Back.RESET + Style.NORMAL, # Grey, light
                "&8": Fore.WHITE + Back.RESET + Style.NORMAL, # Grey, dark
                "&9": Fore.BLUE + Back.RESET + Style.NORMAL, # Blue, light
                "&a": Fore.GREEN + Back.RESET + Style.NORMAL, # Green, light
                "&b": Fore.CYAN + Back.RESET + Style.NORMAL, # Cyan, light
                "&c": Fore.RED + Back.RESET + Style.NORMAL, # Red, light
                "&d": Fore.MAGENTA + Back.RESET + Style.NORMAL, # Magenta, light
                "&e": Fore.YELLOW + Back.RESET + Style.NORMAL, # Yellow, light
                "&f": Fore.WHITE + Back.RESET + Style.BRIGHT, # White, normal
                # Special colours for highlighting text in the console
                "\x01" + "0": Fore.WHITE + Back.RESET + Style.BRIGHT, # A reset. Inverse inverse black on black?
                "\x01" + "1": Fore.BLUE + Back.WHITE + Style.DIM, # Blue, dark, inverse
                "\x01" + "2": Fore.GREEN + Back.WHITE + Style.DIM, # Green, dark, inverse
                "\x01" + "3": Fore.CYAN + Back.WHITE + Style.DIM, # Cyan, dark, inverse
                "\x01" + "4": Fore.RED + Back.WHITE + Style.DIM, # Red, dark, inverse
                "\x01" + "5": Fore.MAGENTA + Back.WHITE + Style.DIM, # Magenta, dark, inverse
                "\x01" + "6": Fore.YELLOW + Back.WHITE + Style.DIM, # Yellow, dark, inverse
                "\x01" + "7": Fore.WHITE + Back.WHITE + Style.NORMAL, # Grey, light, inverse
                "\x01" + "8": Fore.WHITE + Back.WHITE + Style.DIM, # Grey, dark, inverse
                "\x01" + "9": Fore.BLUE + Back.WHITE + Style.NORMAL, # Blue, light, inverse
                "\x01" + "a": Fore.GREEN + Back.WHITE + Style.NORMAL, # Green, light, inverse
                "\x01" + "b": Fore.CYAN + Back.WHITE + Style.NORMAL, # Cyan, light, inverse
                "\x01" + "c": Fore.RED + Back.WHITE + Style.NORMAL, # Red, light, inverse
                "\x01" + "d": Fore.MAGENTA + Back.WHITE + Style.NORMAL, # Magenta, light, inverse
                "\x01" + "e": Fore.YELLOW + Back.WHITE + Style.NORMAL, # Yellow, light, inverse
                "\x01" + "f": Fore.WHITE + Back.RESET + Style.BRIGHT, # A reset. White on white?
                # Extra colours which don't exist ingame
                "\x01" + "g": Fore.MAGENTA + Back.RESET + Style.BRIGHT, # Magenta, bright
            }

    def stdout(self, data):
        """
        Output to stdout, parsing colours.
        """
        origdata = data
        for element in self.cols.keys():
            data = string.replace(data, element, self.cols[element])
        try:
            sys.stdout.write(data + "\n")
        except Exception:
            print("Unable to write directly to stdout! Data: %s" % origdata)
            print(traceback.format_exc())

    def stderr(self, data):
        """
        Output to stderr, parsing colours.
        """
        origdata = data
        for element in self.cols.keys():
            data = string.replace(data, element, self.cols[element])
        try:
            sys.stderr.write(data + "\n")
        except Exception as e:
            self.stdout(origdata)

    def log(self, data, f):
        """
        Write outputs to log files.
        """
        if f not in self.logs.keys():
            raise ValueError
        for element in self.nocol.keys():
            data = string.replace(data, element, self.nocol[element])  # Do not log colour codes in file
        with open(self.logs[f], "a") as fo:
            fo.write(data + "\n")
            fo.flush()
            fo.close()

    def info(self, data):
        atime = time.strftime("%d %b (%H:%M:%S)")
        status = " - &2INFO&f - "
        done = "&f" + atime + status + data
        self.log(done, "info")
        self.log(done, "main")
        self.stdout(done)

    def warn(self, data):
        atime = time.strftime("%d %b (%H:%M:%S)")
        status = " - &eWARN&f - "
        done = "&f" + atime + status + data
        self.log(done, "warn")
        self.log(done, "main")
        self.stderr(done)

    warning = warn

    def error(self, data):
        atime = time.strftime("%d %b (%H:%M:%S)")
        status = " - &cERROR&f - "
        done = "&f" + atime + status + data
        self.log(done, "error")
        self.log(done, "main")
        self.stdout(done)

    def critical(self, data):
        atime = time.strftime("%d %b (%H:%M:%S)")
        status = " - " + "\x01" + "c" + "CRITICAL&f - "
        done = "&f" + atime + status + data
        self.log(done, "critical")
        self.log(done, "main")
        self.stdout(done)

    def debug(self, data):
        if self.isDebug:
            atime = time.strftime("%d %b (%H:%M:%S)")
            status = " - &9DEBUG &f - "
            done = "&f" + atime + status + data
            self.log(done, "debug")
            self.log(done, "main")
            self.stdout(done)