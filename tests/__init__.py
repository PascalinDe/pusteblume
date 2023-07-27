#    Pusteblume v1.2
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
:synopsis: Shared objects.
"""


# standard library imports
import pathlib
import unittest
import configparser
# third party imports
# library specific imports


class BaseTestCase(unittest.TestCase):
    """Base test case."""

    def __init__(self, *args, **kwargs):
        """Initialise base test case."""
        self.data_dir = pathlib.Path(__file__).parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.database = self.data_dir / "temp.db"
        self.config = configparser.ConfigParser()
        self.config.read_dict({"evaluated": {"database": str(self.database)}})
        super().__init__(*args, **kwargs)
