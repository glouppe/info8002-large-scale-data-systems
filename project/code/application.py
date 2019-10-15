"""
User-level application (stub).
NB: Feel free to extend or modify.
"""

import argparse

from dftfs import Storage


def main(arguments):
    storage = allocate_application(arguments)

    # Put data into a file
    path = "/my/awesome/file-location.txt"
    file_bytes = "fun"
    storage.put(path, file_bytes, block=False)

    # Retrieve data
    retrieved_file_bytes = storage.get(path)

    assert(file_bytes == retrieved_file_bytes)


def allocate_application(arguments):
    application = Storage(bootstrap=arguments.bootstrap)

    return application


def parse_arguments():
    parser = argparse.ArgumentParser("DFTFS")
    parser.add_argument("--bootstrap", type=str, default=None,
                        help="Sets the address of the bootstrap or master node.")
    arguments, _ = parser.parse_known_args()

    return arguments


if __name__ == "__main__":
    arguments = parse_arguments()
    main(arguments)
