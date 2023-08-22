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
:synopsis: Task tracking and management tools test cases.
"""


# standard library imports
import os
import datetime
import unittest

# third party imports

# library specific imports
import pusteblume.tasks
import pusteblume.messages

from tests import BaseTestCase


class TaskTestCase(unittest.TestCase):
    """Task test case."""

    def setUp(self):
        """Set up task test case."""
        name = "write test cases"
        tags = ("pusteblume", "v1.2")
        start_time = datetime.datetime.now()
        self.running_task = pusteblume.tasks.Task(
            name,
            tags,
            (start_time, None),
        )
        self.stopped_task = pusteblume.tasks.Task(
            name,
            tags,
            (start_time, start_time + datetime.timedelta(minutes=5)),
        )

    def test_running_task_runtime(self):
        """Test runtime.

        Trying: running task runtime
        Expecting: runtime of < 1 second
        """
        self.assertTrue(self.running_task.runtime < 1)

    def test_stopped_task_runtime(self):
        """Test runtime.

        Trying: stopped task runtime
        Expecting: runtime of >= 300 seconds
        """
        self.assertTrue(self.stopped_task.runtime >= 300)


class TasksTestCase(BaseTestCase):
    """Task tracking and management tools test case."""

    def setUp(self):
        """Set up task tracking and management tools test case."""
        self.name = "write test cases"
        self.tags = ("pusteblume", "v1.2")
        self.start_time = datetime.datetime.now()
        pusteblume.tasks.init_database(self.config)

    def tearDown(self):
        """Tear down task tracking and management tools test case."""
        self.database.unlink()

    def _insert_task(self, name, tags, start_time, end_time):
        """Insert task.

        :param str name: task name
        :param tuple tags: tags
        :param datetime.datetime start_time: start time
        :param datetime.datetime end_time: end time

        :returns: task ID
        :rtype: int
        """
        ((task_id,),) = pusteblume.tasks._execute(
            self.config,
            "INSERT INTO task(name,start_time,end_time) VALUES(?,?,?) RETURNING id",
            (name, start_time, end_time),
        )
        for tag in tags:
            rows = pusteblume.tasks._execute(
                self.config,
                "SELECT id FROM tag WHERE name = ?",
                (tag,),
            )
            if not rows:
                ((tag_id,),) = pusteblume.tasks._execute(
                    self.config,
                    "INSERT INTO tag(name) VALUES(?) RETURNING id",
                    (tag,),
                )
            else:
                ((tag_id,),) = rows
            pusteblume.tasks._execute(
                self.config,
                "INSERT INTO added_to(task_id,tag_id) VALUES(?,?)",
                (task_id, tag_id),
            )
        return task_id

    def test_init_database(self):
        """Test initialise SQLite database.

        Trying: initialise SQLite database
        Expecting: 'task', 'tag' and 'added_to' tables have been initialised
        """
        self.assertListEqual(
            pusteblume.tasks._execute(
                self.config,
                "SELECT name FROM sqlite_master WHERE type = 'table'",
            ),
            [
                ("task",),
                ("tag",),
                ("added_to",),
            ],
        )

    def test_query_related_tags(self):
        """Test querying related tags.

        Trying: query related tags of task without tags
        Expecting: related tags or empty list if there are none
        """
        for tags in ((), self.tags):
            task_id = self._insert_task(self.name, tags, self.start_time, None)
            self.assertListEqual(
                pusteblume.tasks._query_related_tags(self.config, task_id),
                list(tags),
            )

    def test_query_currently_running_task_no_running_task(self):
        """Test querying currently running task.


        Trying: no running task
        Expecting: empty tuple
        """
        self._insert_task(
            self.name,
            (),
            self.start_time,
            datetime.datetime.now(),
        )
        self.assertFalse(pusteblume.tasks._query_currently_running_task(self.config))

    def test_query_currently_running_task_running_task(self):
        """Test querying currently running task.

        Trying: running task
        Expecting: running task
        """
        task_id = self._insert_task(
            self.name,
            (),
            self.start_time,
            None,
        )
        self.assertEqual(
            pusteblume.tasks._query_currently_running_task(self.config)[0][0],
            task_id,
        )

    def test_start_task_without_tags(self):
        """Test starting task.

        Trying: start task without tags
        Expecting: 'task' table has been updated, 'added_to' and 'tag' tables
            have not been updated
        """
        pusteblume.tasks.start(
            self.config,
            self.name,
            (),
        )
        self.assertTrue(
            pusteblume.tasks._execute(
                self.config,
                "SELECT 1 FROM task WHERE name = ?",
                (self.name,),
            ),
        )
        for table in ("tag", "added_to"):
            self.assertFalse(
                pusteblume.tasks._execute(
                    self.config,
                    f"SELECT 1 FROM {table}",
                ),
            )

    def test_start_task_with_tags(self):
        """Test starting task.

        Trying: start task with tags
        Expecting: 'task', 'added_to' and 'tag' tables have been updated
        """
        pusteblume.tasks.start(
            self.config,
            self.name,
            self.tags,
        )
        self.assertTrue(
            pusteblume.tasks._execute(
                self.config,
                "SELECT 1 FROM task WHERE name = ?",
                (self.name,),
            ),
        )
        ((task_id,),) = pusteblume.tasks._execute(
            self.config,
            "SELECT id FROM task WHERE name = ?",
            (self.name,),
        )
        self.assertTrue(
            pusteblume.tasks._execute(
                self.config,
                "SELECT 1 FROM tag WHERE name IN (?,?)",
                self.tags,
            ),
        )
        for row in pusteblume.tasks._execute(
            self.config,
            "SELECT 1 FROM tag WHERE name IN (?,?)",
            self.tags,
        ):
            self.assertTrue(
                pusteblume.tasks._execute(
                    self.config,
                    "SELECT 1 FROM added_to WHERE task_id = ? and tag_id = ?",
                    (task_id, row[0]),
                ),
            )

    def test_stop_stopped_task(self):
        """Test stopping task.

        Trying: stop stopped task
        Expecting: 'task' table has not been updated
        """
        pusteblume.tasks.start(
            self.config,
            self.name,
        )
        end_time = datetime.datetime.now()
        pusteblume.tasks._execute(
            self.config,
            "UPDATE task SET end_time = ? WHERE name = ?",
            (end_time, self.name),
        )
        pusteblume.tasks.stop(self.config)
        self.assertTrue(
            pusteblume.tasks._execute(
                self.config,
                "SELECT 1 FROM task WHERE name = ? AND end_time = ?",
                (self.name, end_time),
            )
        )

    def test_stop_running_task(self):
        """Test stopping task.

        Trying: stop running task
        Expecting: 'task' table has been updated
        """
        pusteblume.tasks.start(
            self.config,
            self.name,
        )
        pusteblume.tasks.stop(self.config)
        self.assertFalse(
            pusteblume.tasks._execute(
                self.config,
                "SELECT 1 FROM task WHERE name = ? AND end_time IS NULL",
                (self.name,),
            ),
        )

    def test_list(self):
        """Test listing tasks.

        Trying: 1 stopped and 1 running task
        Expecting: 1 stopped and 1 running task
        """
        running_task = pusteblume.tasks.Task(
            self.name,
            self.tags,
            (
                self.start_time + datetime.timedelta(minutes=5),
                None,
            ),
        )
        stopped_task = pusteblume.tasks.Task(
            self.name,
            self.tags,
            (
                self.start_time,
                datetime.datetime.now(),
            ),
        )
        for task in (running_task, stopped_task):
            self._insert_task(task.name, task.tags, *task.time_range)
        self.assertEqual(
            pusteblume.tasks.list(self.config),
            os.linesep.join(
                task.pprinted_long for task in (running_task, stopped_task)
            ),
        )

    def test_status_no_running_task(self):
        """Test showing currently running task.


        Trying: no running task
        Expecting: 'no running task' message
        """
        self.assertEqual(
            pusteblume.tasks.status(self.config),
            pusteblume.messages.MESSAGES["no_running_task"],
        )

    def test_status_running_task(self):
        """Test showing currently running task.

        Trying: running task
        Expecting: message w/ running task
        """
        pusteblume.tasks.start(
            self.config,
            self.name,
            self.tags,
        )
        ((start_time,),) = pusteblume.tasks._execute(
            self.config,
            "SELECT start_time FROM task WHERE name = ?",
            (self.name,),
        )
        task = pusteblume.tasks.Task(self.name, self.tags, (start_time, None))
        self.assertEqual(
            pusteblume.tasks.status(self.config),
            task.pprinted_short,
        )