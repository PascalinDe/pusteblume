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
:synopsis: Shared objects.
"""


# standard library imports
import os
import pathlib
import configparser

# third party imports
# library specific imports


CONFIG_FILE = (
    pathlib.Path(os.environ["HOME"])
    / ".config"
    / "pusteblume.ini"
)
CONFIG = {
    "database": ["path", "name"],
}
METADATA = {
    "name": "pusteblume",
    "version": "v1.0",
    "description": "Light-weight time tracking tool.",
    "author": "Carine Dengler",
    "author_email": "pusteblume@pascalin.de",
    "url": "https://github.com/PascalinDe/pusteblume",
    "classifiers": [
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.11",
    ],
}


def generate_default_config():
    """Generate default configuration file."""
    config = configparser.ConfigParser()
    config["database"] = {
        "path": str(pathlib.Path(os.environ["HOME"]) / ".local" / "share"),
        "name": "pusteblume.db",
    }
    with CONFIG_FILE.open("w") as fp:
        config.write(fp)
    print(f"generated default configuration file '{CONFIG_FILE}'")


def load_config():
    """Load configuration file.

    :raises: SystemExit if configuration file is invalid

    :returns: configuration
    :rtype: configparser.ConfigParser
    """
    if not CONFIG_FILE.exists():
        generate_default_config()
    config = configparser.ConfigParser()
    with CONFIG_FILE.open() as fp:
        config.read_file(fp)
    errors = []
    for section in CONFIG:
        if section not in config.sections():
            errors.append(f"required section '{section}' missing")
        else:
            for key in CONFIG[section]:
                if key not in config[section]:
                    errors.append(
                        f"required key '{key}' in section '{section}' missing"
                    )
    if errors:
        raise SystemExit(
            os.linesep.join(
                (f"configuration file '{CONFIG_FILE}' contains errors", *errors)
            )
        )
    config.add_section("evaluated")
    config.set(
        "evaluated",
        "database",
        str(
            pathlib.Path(config["database"]["path"])
            / config["database"]["name"]
        ),
    )
    return config
