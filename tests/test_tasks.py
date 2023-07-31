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
import datetime
import unittest

# third party imports

# library specific imports
import pusteblume.tasks


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
