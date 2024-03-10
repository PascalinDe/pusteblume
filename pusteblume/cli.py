#    Pusteblume v1.2
#    Copyright (C) 2024  Carine Dengler
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
import pusteblume.errors
import pusteblume.messages

from pusteblume import METADATA


_RESERVED_CHARS = "[]"


def name(string):
    """Assert string matches 'name' pattern.

    :param str string: string

    :raises: argparse.ArgumentTypeError

    :returns: name
    :rtype: str
    """
    if matches := re.findall(rf"[{re.escape(_RESERVED_CHARS)}]", string):
        raise argparse.ArgumentTypeError(
            pusteblume.errors.ERRORS["cli"]["reserved_chars"].format(
                string=string,
                reserved_chars="".join(dict.fromkeys(matches)),
            ),
        )
    return string


def tag(string):
    """Assert string matches 'tag' pattern.

    :param str string: string

    :raises: argparse.ArgumentTypeError

    :returns: tag
    :rtype: str
    """
    if match := re.match(r"\[(.+?)\]", string):
        return name(match.group(1))
    raise argparse.ArgumentTypeError(
        pusteblume.errors.ERRORS["cli"]["invalid_tag"].format(string=string),
    )


def split(argv):
    """Split command-line arguments.

    :param list argv: command-line arguments

    :returns: command-line arguments
    :rtype: list
    """
    if len(argv) == 1:
        return argv
    args = [argv[0]]  # argumentless subcommand
    sep = ""
    for split in re.split(
        rf"([{re.escape(_RESERVED_CHARS)}])",
        " ".join(argv[1:]),
    ):
        split = split.strip()
        if not split:
            continue
        if split in _RESERVED_CHARS:
            if len(args) == 1:
                args.append(split)
                continue
            if split == "[":
                sep = split
            if split == "]":
                args[-1] += split
            continue
        args.append(sep + split)
        sep = ""
    return args


def parse_input(input_, type_, choices=()):
    """Parse input.

    :param str input_: input
    :param str type_: type
    :param list choices: choices

    :returns: parsed input
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        prog="",
        add_help=False,
    )
    if type_ == "name":
        parser.add_argument(
            type_,
            type=name,
        )
        input_ = [input_]
    if type_ == "tag":
        parser.add_argument(
            type_,
            nargs="*",
            type=tag,
        )
        input_ = [tag + "]" for tag in input_.split("]") if tag]
    if type_ == "choice":
        parser.add_argument(
            type_,
            choices=choices,
        )
        input_ = [input_]
    return parser.parse_args(input_)


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
        version=pusteblume.messages.MESSAGES["cli"]["version"].format(
            version=METADATA["version"],
        ),
        help=pusteblume.messages.MESSAGES["cli"]["help"]["version"],
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
            "func": pusteblume.tasks.list_,
        },
        "start": {
            "help": pusteblume.messages.MESSAGES["cli"]["help"]["start"],
            "arguments": {
                "name": {
                    "type": name,
                    "help": pusteblume.messages.MESSAGES["cli"]["help"]["name"],
                },
                "tags": {
                    "nargs": "*",
                    "type": tag,
                    "help": pusteblume.messages.MESSAGES["cli"]["help"]["tags"],
                },
            },
            "func": pusteblume.tasks.start,
        },
        "stop": {
            "help": pusteblume.messages.MESSAGES["cli"]["help"]["stop"],
            "arguments": {},
            "func": pusteblume.tasks.stop,
        },
        "status": {
            "help": pusteblume.messages.MESSAGES["cli"]["help"]["status"],
            "arguments": {},
            "func": pusteblume.tasks.status,
        },
        "edit": {
            "help": pusteblume.messages.MESSAGES["cli"]["help"]["edit"],
            "arguments": {
                "name": {
                    "type": name,
                    "help": pusteblume.messages.MESSAGES["cli"]["help"]["name"],
                },
                "tags": {
                    "nargs": "*",
                    "type": tag,
                    "help": pusteblume.messages.MESSAGES["cli"]["help"]["tags"],
                },
            },
            "func": pusteblume.tasks.edit,
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
