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
:synopsis: Error messages and exceptions.
"""


# standard library imports
# third party imports
# library specific imports


ERRORS = {
    "main": {
        "failed_subcommand": "subcommand '{subcommand}' failed",
    },
    "config": {
        "missing_section": "required section '{section}' missing",
        "missing_key": "required key '{key}' in section '{section}' missing",
        "errors": "configuration file {config_file} contains errors",
    },
    "cli": {
        "reserved_chars": "'{string}' contains reserved characters '{reserved_chars}'",
        "invalid_tag": "'{string}' is not a valid tag",
    },
}


class InvalidConfig(Exception):
    """Raised when configuration file is invalid."""

    pass
