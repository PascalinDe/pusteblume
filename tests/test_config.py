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
:synopsis: Configuration management test cases.
"""


# standard library imports
import unittest.mock
import configparser

# third party imports
# library specific imports
import pusteblume.config
import pusteblume.errors

from tests import BaseTestCase


@unittest.mock.patch(
    "pusteblume.config.CONFIG_FILE",
    BaseTestCase.DATA_DIR / "pusteblume.ini",
)
class ConfigTestCase(BaseTestCase):
    """Configuration management test case."""

    def setUp(self):
        """Set up configuration management test case."""
        self.expected = configparser.ConfigParser()
        self.expected.read_dict(
            {
                "database": {
                    "path": pusteblume.config._DATABASE_PATH,
                    "name": pusteblume.config._DATABASE_NAME,
                },
            },
        )

    def test_generate_default_config(self):
        """Test generating default config file.

        Trying: generate default config file
        Expecting: default config file
        """
        pusteblume.config.generate_default_config()
        actual = configparser.ConfigParser()
        with pusteblume.config.CONFIG_FILE.open() as fp:
            actual.read_file(fp)
        self.assertEqual(actual, self.expected)

    def test_validate_config_valid_config(self):
        """Test validating configuration file.

        Trying: valid configuration
        Expecting: InvalidConfig is not raised
        """
        pusteblume.config.validate_config(self.expected)

    def test_validate_config_invalid_config(self):
        """Test validating configuration file.

        Trying: invalid configuration
        Expecting: InvalidConfig is raised
        """
        # missing section
        config = configparser.ConfigParser()
        with self.assertRaises(pusteblume.errors.InvalidConfig):
            pusteblume.config.validate_config(config)
        # missing key
        config = configparser.ConfigParser()
        config.read_dict(
            {
                "database": {
                    "path": pusteblume.config._DATABASE_PATH,
                },
            },
        )
        with self.assertRaises(pusteblume.errors.InvalidConfig):
            pusteblume.config.validate_config(config)
