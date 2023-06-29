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
:synopsis: Main routine.
"""


# standard library imports
import sys

# third party imports
# library specific imports
import pusteblume.cli
import pusteblume.tasks

from pusteblume import load_config


def main():
    """Main routine."""
    config = load_config()
    pusteblume.tasks.init_database(config)
    argument_parser = pusteblume.cli.init_argument_parser()
    args = argument_parser.parse_args(pusteblume.cli.split(sys.argv[1:]))
    try:
        print(
            args.func(
                config,
                **{k: v for k, v in vars(args).items() if k != "func"},
            )
        )
    except Exception:
        print(f"subcommand '{sys.argv[1]}' failed")
        raise SystemExit
