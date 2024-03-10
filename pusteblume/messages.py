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
:synopsis: Messages.
"""


# standard library imports
# third party imports
# library specific imports


MESSAGES = {
    "tasks": {
        "no_running_task": "no running task",
        "edit": {
            "task": "Editing task '{task}'...",
            "tasks": "Which task do you want to edit?",
            "no_task": "'{task}' does not exist",
            "attribute": "Which attribute do you want to edit?",
            "new_attr": "What is the new value of {attribute}?",
            "new_value": "The new value of {attribute} is {value}",
        },
    },
    "config": {
        "default": "generated default configuration file {config_file}",
    },
    "cli": {
        "help": {
            "version": "print %(prog)s version",
            "list": "list tasks",
            "start": "start task",
            "stop": "stop task",
            "status": "show currently running task if any",
            "edit": "edit task",
            "name": "task name, e.g. 'debug command-line interface'",
            "tags": "tag(s), e.g. '[v1.2]'",
        },
        "version": "%(prog)s {version}",
    },
}
COLOURS = {
    "fg": {
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
    },
    "bg": {},
}
for k, v in list(COLOURS["fg"].items()):
    COLOURS["fg"][f"bright_{k}"] = v + 60
for k, v in list(COLOURS["fg"].items()):
    COLOURS["bg"][k] = v + 10
COLOURS["fg"]["default"] = 0
COLOURS["bg"]["default"] = 0
STYLES = {
    "normal": 0,
    "bold": 1,
    "faint": 2,
    "italic": 3,
    "underline": 4,
}


def colour_string(string, style=None, fg=None, bg=None):
    """Colour string.

    :param str string: string
    :param str style: style
    :param str fg: foreground colour
    :param str bg: background colour

    :returns: coloured string
    :rtype: str
    """
    style = STYLES.get(style, "")
    fg = COLOURS["fg"].get(fg, "")
    bg = COLOURS["bg"].get(bg, "")
    ansi_escape_codes = ";".join(
        str(escape_code) for escape_code in (style, fg, bg) if escape_code
    )
    return f"\033[{ansi_escape_codes}m{string}\033[m"
