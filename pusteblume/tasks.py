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
:synopsis: Task tracking and management tools.
"""


# standard library imports
import os
import sqlite3
import datetime
import collections

# third party imports
# library specific imports
import pusteblume.messages


_Task = collections.namedtuple("Task", ("name", "tags", "time_range"))


class Task(_Task):
    """Task."""

    __slots__ = ()

    @property
    def runtime(self):
        """Runtime (in seconds).

        :returns: runtime
        :rtype: int
        """
        end_time = self.time_range[1] or datetime.datetime.now()
        delta = end_time - self.time_range[0]
        if delta.days >= 1:
            return delta.seconds + delta.days * (24 * 60 * 60)
        return delta.seconds

    @property
    def pprinted_tags(self):
        """Pretty-printed tags.

        :returns: pretty-printed tags
        :rtype: str
        """
        return pusteblume.messages.colour_string(
            "".join(f"[{tag}]" for tag in self.tags),
            fg="bright_black",
        )

    @property
    def pprinted_short(self):
        """Pretty-printed short form.

        :returns: pretty-printed short form
        :rtype: str
        """
        return f"{pusteblume.messages.colour_string(self.name, fg='green')} {self.pprinted_tags}"  # noqa: E501

    @property
    def pprinted_time_range(self):
        """Pretty-printed time range.

        :returns: pretty-printed time range
        :rtype: str
        """
        start_time, end_time = self.time_range
        if not end_time:
            pprinted_end_time = "…"
        else:
            pprinted_end_time = end_time.strftime("%H:%M %Y-%m-%d")
        if end_time and end_time.date == start_time.date:
            pprinted_start_time = start_time.strftime("%H:%M")
        else:
            pprinted_start_time = start_time.strftime("%H:%M %Y-%m-%d")
        return pusteblume.messages.colour_string(
            f"{pprinted_start_time}-{pprinted_end_time}",
            fg="magenta",
        )

    @property
    def pprinted_time_range_parentheses(self):
        """Pretty-printed time range in parentheses.

        :returns: pretty-printed time range in parentheses
        :rtype: str
        """
        return (
            pusteblume.messages.colour_string("(", fg="magenta")
            + self.pprinted_time_range
            + pusteblume.messages.colour_string(")", fg="magenta")
        )

    @property
    def pprinted_medium(self):
        """Pretty-printed medium form.

        :returns: pretty-printed medium form
        :rtype: str
        """
        return f"{self.pprinted_short} {self.pprinted_time_range_parentheses}"

    @property
    def pprinted_runtime(self):
        """Pretty-printed runtime.

        :returns: pretty-printed runtime
        :rtype: str
        """
        hours, minutes = divmod(divmod(self.runtime, 60)[0], 60)
        return pusteblume.messages.colour_string(f"({hours}h{minutes}m)", fg="yellow")

    @property
    def pprinted_long(self):
        """Pretty-printed long form.

        :returns: pretty-printed long form
        :rtype: str
        """
        return f"{self.pprinted_time_range}{self.pprinted_runtime} {self.pprinted_short}"  # noqa: E501


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


def _get_related_tags(config, task_id):
    """Get related tags.

    :param configparser.ConfigParser config: configuration
    :param int task_id: task ID

    :returns: related tags
    :rtype: list
    """
    return [
        name
        for (name,) in _execute(
            config,
            """SELECT tag.name
            FROM tag JOIN added_to ON tag.id = added_to.tag_id
            WHERE added_to.task_id = ?""",
            (task_id,),
        )
    ]


def _get_currently_running_task(config):
    """Get currently running task.

    :param configparser.ConfigParser config: configuration

    :returns: currently running task
    :rtype: tuple
    """
    return _execute(
        config,
        "SELECT id,name,start_time FROM task WHERE end_time IS NULL",
    )


def start(config, name=None, tags=tuple()):
    """Start task.

    :param configparser.ConfigParser config: configuration
    :param str name: task name
    :param tuple tags: tag(s)

    :returns: output
    :rtype: str
    """
    start_time = datetime.datetime.now()
    output = stop(config)
    ((task_id,),) = _execute(
        config,
        "INSERT INTO task(name,start_time) VALUES(?,?) RETURNING id",
        (name, start_time),
    )
    for tag in tags:
        rows = _execute(
            config,
            "SELECT id FROM tag WHERE name = ?",
            (tag,),
        )
        if not rows:
            ((tag_id,),) = _execute(
                config,
                "INSERT INTO tag(name) VALUES(?) RETURNING id",
                (tag,),
            )
        else:
            ((tag_id,),) = rows
        _execute(
            config,
            "INSERT INTO added_to(task_id,tag_id) VALUES(?,?)",
            (task_id, tag_id),
        )
    return os.linesep.join(
        (output, Task(name, tags, (start_time, None)).pprinted_short)
    )


def stop(config):
    """Stop task.

    :param configparser.ConfigParser config: configuration

    :returns: output
    :rtype: str
    """
    rows = _get_currently_running_task(config)
    if not rows:
        return pusteblume.messages.MESSAGES["tasks"]["no_running_task"]
    end_time = datetime.datetime.now()
    _execute(config, "UPDATE task SET end_time = ? WHERE end_time IS NULL", (end_time,))
    return os.linesep.join(
        [
            Task(
                name,
                _get_related_tags(config, task_id),
                (start_time, end_time),
            ).pprinted_medium
            for (task_id, name, start_time) in rows
        ]
    )


def list_(config):
    """List tasks.

    :param configparser.ConfigParser config: configuration

    :returns: output
    :rtype: str
    """
    rows = _execute(
        config,
        "SELECT id,name,start_time,end_time FROM task",
    )
    if not rows:
        return ""
    tasks = []
    for task_id, name, start_time, end_time in rows:
        tasks.append(
            Task(
                name,
                _get_related_tags(config, task_id),
                (start_time, end_time),
            ),
        )
    return os.linesep.join(task.pprinted_long for task in tasks)


def status(config):
    """Show currently running task if any.

    :param configparser.ConfigParser config: configuration

    :returns: output
    :rtype: str
    """
    rows = _get_currently_running_task(config)
    if not rows:
        return pusteblume.messages.MESSAGES["tasks"]["no_running_task"]
    (task_id, name, start_time) = rows[0]
    return Task(
        name,
        _get_related_tags(config, task_id),
        (start_time, None),
    ).pprinted_short
