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
:synopsis: Task tracking and management tools.
"""


# standard library imports
import sqlite3
import collections

# third party imports
# library specific imports


def _connect(config):
    """Connect to SQLite3 database.

    :returns: SQLite3 database connection
    :rtype: sqlite3.Connection
    """
    return sqlite3.connect(
        config["evaluated"]["database"],
        detect_types=sqlite3.PARSE_DECLTYPES,
    )


def _execute(config, statement, *parameters):
    """Execute SQLite statement.

    :param configparser.ConfigParser config: configuration
    :param str statement: SQLite statement
    :param tuple parameters: parameters

    :returns: rows
    :rtype: list
    """
    try:
        connection = _connect(config)
        if len(parameters) > 1:
            rows = connection.executemany(statement, parameters).fetchall()
        else:
            rows = connection.execute(statement, *parameters).fetchall()
    except sqlite3.Error:
        connection.rollback()
        raise
    connection.commit()
    return rows


def init_database(config):
    """Initialize SQLite database.

    :param configparser.ConfigParser config: configuration
    """
    for table, columns in (
        (
            "task",
            (
                "id INTEGER PRIMARY KEY",
                "name TEXT",
                "start_time TIMESTAMP",
                "end_time TIMESTAMP CHECK (end_time > start_time)",
            ),
        ),
        (
            "tag",
            (
                "id INTEGER PRIMARY KEY",
                "name TEXT UNIQUE",
            ),
        ),
        (
            "added_to",
            (
                "tag_id INTEGER",
                "task_id INTEGER",
                "FOREIGN KEY(tag_id) REFERENCES tag(id)",
                "FOREIGN KEY(task_id) REFERENCES task(id)",
            ),
        ),
    ):
        _execute(
            config,
            f"CREATE TABLE IF NOT EXISTS {table} ({','.join(columns)})",
        )
