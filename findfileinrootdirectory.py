#!/usr/bin/env python3
"""Finds the files under the directory that match the input regex keyword.
  
    Usage:
        python3 findfileinrootdirectory.py -r <rootdir> -s <searchstr>

"""

from os import listdir, path as op, walk 
import re
from collections import OrderedDict
from argparse import ArgumentParser, ArgumentError

def parse_commandline():
    """Parses command line arguments and returns a list

    Returns :
        Namespace : Namespace object of argument parser
    """

    parser = ArgumentParser()

    mandatory_group = parser.add_argument_group('Mandatory arguments')
    rootdir_arg = mandatory_group.add_argument(
        "-r",
        "--rootdir",
        metavar="Path",
        dest="rootdir",
        action="store",
        help="Root directory path",
        required=True
    )

    fn_search_string_arg = mandatory_group.add_argument(
        "-s",
        "--searchString",
        metavar="SearchRegex",
        dest="fn_search_string",
        action="store",
        help="Filename search string",
        required=True
    )

    args = parser.parse_args()

    if args.rootdir is None:
        raise ArgumentError(rootdir_arg, "Missing root directory path")
    elif not op.isdir(args.rootdir):
        raise ArgumentError(rootdir_arg, "Incorrect directory path")
    elif args.fn_search_string is None:
        raise ArgumentError(
            fn_search_string_arg,
            "Missing filename search string"
        )
    elif not re.compile(args.fn_search_string):
        raise ArgumentError(
            fn_search_string_arg,
            "Filename search string is not a proper regular expression"
        )
    else:
        return args


def find_files_in_root_dir(root_dir, fn_srch_regex):
    """Finds the files present in the Dir and all the subDirs and returns a
       dictionary.

        Args:
            root_dir: path of the root directory
            fn_srch_regex: filename search regular expression
    """

    dir_files_dict = {}
    for (dirpath, dirnames, filenames) in walk(root_dir):
        dir_files_dict[dirpath] = len([fn for fn in filenames 
                                       if re.match(fn_srch_regex, fn)]
                                     )
    return OrderedDict(sorted(dir_files_dict.items()))


if __name__ == "__main__":
    """Prints a list of directories and the number of files contained in them

    """

    try:
        parsed_args = parse_commandline()
        root_dir_path = parsed_args.rootdir
        fn_search_regex = re.compile(parsed_args.fn_search_string)
        dir_files = find_files_in_root_dir(root_dir_path, fn_search_regex)
        print("{" + ", ".join(" : ".join(["'" + key + "'", str(val)])
                               for key, val in dir_files.items()) + "}")

        try:
            from matplotlib.pyplot import bar
        except ImportError:
            print("Plot is not available, Kindly install 'matplotlib'" + 
			      "library")
        else:
            tick_label = [key for key, val in dir_files.items()]
            x_axis = range(1, len(tick_label) + 1)
            y_axis = [val for key, val in dir_files.items()]
            bar(x_axis, y_axis, tick_label=tick_label,
                width=0.8, color=['red', 'blue'])
    except Exception as e:
        print("Exception occurred, reason : " + str(e))

