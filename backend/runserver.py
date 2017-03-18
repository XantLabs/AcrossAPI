"""Run the server according to arguments."""
from sys import argv

from __init__ import DEBUG, app

if __name__ == "__main__":
    argc = len(argv)

    if argc == 2:
        try:
            argHost, argPort = argv[1].split(":")
            app.run(argHost, int(argPort), debug=DEBUG)
        except Exception as e:
            print("Error: input not understood.")
    else:
        print("Error: please provide ip:port as only one positional argument.")
