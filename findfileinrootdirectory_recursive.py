"""Finds the files under the directory that match the input regex keyword."""

from os import listdir, path as op
import re
from collections import OrderedDict
from argparse import ArgumentParser, ArgumentError


def parse_commandline():
    """parses command line arguments and returns a list

    Returns :
        Namespace : Namespace object of argument parser
    """

    parser = ArgumentParser()

    # Create mandatory argument group
    mandatory_group = parser.add_argument_group('Mandatory arguments')
    # Add rootdir argument
    rootdir_arg = mandatory_group.add_argument(
        "-r",
        "--rootdir",
        metavar="Path",
        dest="rootdir",
        action="store",
        help="Root directory path",
        required=True
    )

    # Add mandatory argument searchString
    fn_search_string_arg = mandatory_group.add_argument(
        "-s",
        "--searchString",
        metavar="Path",
        dest="fn_search_string",
        action="store",
        help="Filename search string",
        required=True
    )

    args = parser.parse_args()

    # Check if the arguments are valid and return them or else raise exception
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
    """Finds the files present in rootDir and all subDirs and returns a dict.

    Input:
        root_dir: The main directory for which you want to find the number
                  of files that match the regular exp string
        fn_srch_regex : The regular expression which should match the file
                        names
    Return:
        dir_files_dict : dictionary containing the number of files for root
                         dir and sub dirs that match the regex string
    """

    dir_files_dict = {}
    filenums = 0
    for f in listdir(root_dir):
        if (op.isfile(op.join(root_dir, f)) and
                re.match(fn_srch_regex, f)):
            filenums += 1
        elif op.isdir(op.join(root_dir, f)):
            dir_files_dict.update(find_files_in_root_dir(op.join(root_dir, f),
                                                         fn_srch_regex))
    dir_files_dict.setdefault(root_dir, filenums)
    return dir_files_dict


if __name__ == "__main__":
    '''prints a list of directories and the number of files contained in them.
    '''

    # Start of try block for catching any exceptions
    try:
        # parse commandline arguments
        parsed_args = parse_commandline()
        root_dir_path = parsed_args.rootdir
        fn_search_regex = re.compile(parsed_args.fn_search_string)

        # Call find_files_in_root_dir with the arguments and get the output
        # dictionary of dirs and number of files
        dir_files = find_files_in_root_dir(root_dir_path, fn_search_regex)
        # Sort the output dictionary
        dir_files = OrderedDict(sorted(dir_files.items()))
        print ("{" + ", ".join(" : ".join(["'" + key + "'", str(val)])
                               for key, val in dir_files.items()) + "}")

        # Add a try block for checking if the matplotlib library is available
        try:
            from matplotlib.pyplot import bar
        except ImportError:
            # If library is not available then display error message
            print ("Plot is not available, Kindly install \"" +
                   "matplotlib\" library using PIP")
        else:
            # If library is available, then plot the graph
            tick_label = [key for key, val in dir_files.items()]
            x_axis = xrange(1, len(tick_label) + 1)
            y_axis = [val for key, val in dir_files.items()]
            bar(x_axis, y_axis, tick_label=tick_label,
                width=0.8, color=['red', 'blue'])
    except Exception as e:
        print str("Exception occurred, reason : " + str(e))

