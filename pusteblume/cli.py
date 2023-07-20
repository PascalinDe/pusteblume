#    Pusteblume v1.0
#    Copyright (C) 2023  Carine Dengler
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
:synopsis: Command-line interface.
"""


# standard library imports
import re
import argparse

# third party imports
# library specific imports
import pusteblume.tasks

from pusteblume import METADATA


RESERVED_CHARS = "[]"


def _name(string):
    """Assert string matches 'name' pattern.

    :param str string: string

    :raises: argparse.ArgumentError

    :returns: name
    :rtype: str
    """
    if re.findall(fr"[{re.escape(RESERVED_CHARS)}]", string):
        raise argparse.ArgumentError(
            f"'{string}' contains reserved character(s) ('{RESERVED_CHARS}')"
        )
    return string


def _tag(string):
    """Assert string matches 'tag' pattern.

    :param str string: string

    :raises: argparse.ArgumentError

    :returns: tag
    :rtype: str
    """
    if match := re.match(r"\[(.+?)\]", string):
        return _name(match.group(1))
    raise argparse.ArgumentError(f"'{string}' is not a valid tag")


def split(argv):
    """Split command-line arguments.

    :param list argv: command-line arguments

    :returns: command-line arguments
    :rtype: list
    """
    if len(argv) == 1:
        return argv
    args = [argv[0]]    # argumentless subcommand
    sep = ""
    for split in re.split(
        fr"([{re.escape(RESERVED_CHARS)}])",
        " ".join(argv[1:]),
    ):
        split = split.strip()
        if not split:
            continue
        if split in RESERVED_CHARS:
            if split == "[":
                sep = split
            if split == "]":
                args[-1] += split
            continue
        args.append(sep + split)
        sep = ""
    return args


def init_argument_parser():
    """Initialize argument parser.

    :returns: argument parser
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog=METADATA["name"],
        description=METADATA["description"],
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {METADATA['version']}",
        help="print %(prog)s version",
    )
    _init_subparsers(parser)
    return parser


def _init_subparsers(parser):
    """Initialize subparsers.

    :param argparse.ArgumentParser parser: argument parser
    """
    subcommands = {
        "list": {
            "help": "list tasks",
            "arguments": {},
            "func": pusteblume.tasks.list,
        },
        "start": {
            "help": "start task",
            "arguments": {
                "name": {
                    "type": _name,
                    "help": "task name, e.g. 'debug command-line interface'",
                },
                "tags": {
                    "nargs": "*",
                    "type": _tag,
                    "help": "tag(s), e.g. '[v1.0]'",
                },
            },
            "func": pusteblume.tasks.start,
        },
        "stop": {
            "help": "stop task",
            "arguments": {},
            "func": pusteblume.tasks.stop,
        },
    }
    subparsers = parser.add_subparsers()
    for subcommand in subcommands:
        subparser = subparsers.add_parser(
            subcommand,
            help=subcommands[subcommand]["help"],
        )
        subparser.set_defaults(func=subcommands[subcommand]["func"])
        for argument in subcommands[subcommand]["arguments"]:
            subparser.add_argument(
                argument,
                **subcommands[subcommand]["arguments"][argument],
            )
