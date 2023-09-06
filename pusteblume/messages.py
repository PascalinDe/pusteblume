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
:synopsis: Messages.
"""


# standard library imports
# third party imports
# library specific imports


MESSAGES = {
    "tasks": {
        "no_running_task": "no running task",
    },
    "config": {
        "default": "generated default configuration file {config_file}",
    },
    "cli": {
        "help": {
            "list": "list tasks",
            "start": "start task",
            "stop": "stop task",
            "status": "show currently running task if any",
            "name": "task name, e.g. 'debug command-line interface'",
            "tags": "tag(s), e.g. '[v1.2]'",
        },
    },
}
