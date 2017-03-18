"""Run the server according to arguments."""
from sys import argv

import backend

if __name__ == "__main__":
    argc = len(argv)

    if argc == 2:
        try:
            argHost, argPort = argv[1].split(":")
            backend.app.run(argHost, int(argPort), debug=backend.DEBUG)
        except Exception as e:
            print("Error: input not understood.")
            print(e)
    else:
        print("Error: please provide ip:port as only one positional argument.")
