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
:synopsis: Configuration management.
"""


# standard library imports
import os
import pathlib
import configparser

# third party imports
# library specific imports
import pusteblume.errors
import pusteblume.messages


_HOME_PATH = pathlib.Path(os.environ["HOME"])
_DATABASE_NAME = "pusteblume.db"
_DATABASE_PATH = _HOME_PATH / ".local" / "share"
CONFIG_FILE = _HOME_PATH / ".config" / "pusteblume.ini"


CONFIG_SECTIONS = {
    "database": ["path", "name"],
}


def generate_default_config():
    """Generate default configuration file."""
    ((section, keys),) = CONFIG_SECTIONS.items()
    default_config = configparser.ConfigParser()
    default_config[section] = {
        keys[0]: str(_DATABASE_PATH),
        keys[1]: _DATABASE_NAME,
    }
    with CONFIG_FILE.open("w") as fp:
        default_config.write(fp)
    print(
        pusteblume.messages.MESSAGES["config"]["default"].format(
            config_file=CONFIG_FILE,
        )
    )


def validate_config(config):
    """Validate configuration file.

    :param configparser.ConfigParser config: configuration

    :raises: InvalidConfig if configuration file is invalid
    """
    errors = []
    for section in CONFIG_SECTIONS:
        if section not in config.sections():
            errors.append(
                pusteblume.errors.ERRORS["config"]["missing_section"].format(
                    section=section,
                )
            )
        else:
            for key in CONFIG_SECTIONS[section]:
                if key not in config[section]:
                    errors.append(
                        pusteblume.errors.ERRORS["config"]["missing_key"].format(
                            key=key,
                            section=section,
                        ),
                    )
    if errors:
        raise pusteblume.errors.InvalidConfig(
            os.linesep.join(
                (
                    pusteblume.errors.ERRORS["config"]["errors"].format(
                        config_file=CONFIG_FILE,
                    ),
                    *errors,
                ),
            ),
        )


def load_config():
    """Load configuration file.

    :raises: InvalidConfig if configuration file is invalid

    :returns: configuration
    :rtype: configparser.ConfigParser
    """
    if not CONFIG_FILE.exists():
        generate_default_config()
    config = configparser.ConfigParser()
    with CONFIG_FILE.open() as fp:
        config.read_file(fp)
    validate_config(config)
    config.add_section("evaluated")
    config.set(
        "evaluated",
        "database",
        str(pathlib.Path(config["database"]["path"]) / config["database"]["name"]),
    )
    return config
