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
import argparse

# third party imports
# library specific imports
from pusteblume import METADATA


def split(argv):
    """Split command-line arguments.

    :param list argv: command-line arguments

    :returns: command-line arguments
    :rtype: list
    """
    return argv


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
    subcommands = {}
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
