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
:synopsis: Main routine.
"""


# standard library imports
import sys
import logging

# third party imports
# library specific imports
import pusteblume.cli
import pusteblume.tasks
import pusteblume.output

from pusteblume.config import load_config


def main():
    """Main routine."""
    logging.basicConfig(level=logging.DEBUG)
    config = load_config()
    pusteblume.tasks.init_database(config)
    argument_parser = pusteblume.cli.init_argument_parser()
    args = argument_parser.parse_args(pusteblume.cli.split(sys.argv[1:]))
    try:
        if output := args.func(
            config,
            **{k: v for k, v in vars(args).items() if k != "func"},
        ):
            print(output)
    except Exception as exception:
        logging.getLogger(main.__name__).exception(exception)
        print(f"subcommand '{sys.argv[1]}' failed")
        raise SystemExit
