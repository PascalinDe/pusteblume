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


PROMPT = "> "
OUTPUT = {
    "cli": {
        "messages": {
            "help": {
                "version": "output version information",
                "list": "list tasks",
                "start": "start task",
                "stop": "stop task",
                "status": "output running task",
                "edit": "edit task",
                "arguments": {
                    "name": "name, e.g. 'debug user interface'",
                    "tags": "tags, e.g. '[pusteblume][v1.3]'",
                },
            },
            "version": "%(prog)s {version}",
        },
        "errors": {
            "reserved_chars": "'{string}' contains reserved characters '{reserved_chars}'",
            "invalid_tag": "'{string}' is not a valid tag",
        },
    },
    "main": {
        "messages": {},
        "errors": {
            "failed_subcommand": "subcommand '{subcommand}' failed",
        },
    },
    "tasks": {
        "messages": {
            "stop": {
                "no_task": "no running task",
            },
            "edit": {
                "single_matching_task": "editing '{task}' …",
                "multiple_matching_tasks": "choose task to edit: …",
                "no_matching_task": "no task '{task}'",
                "attribute": "choose attribute to edit: …",
                "value": "new value of {attribute}: …",
            },
        },
        "errors": {},
    },
}
MESSAGES = {
    "config": {
        "generate_default_config": "generated default configuration file {config_file}",
    },
}
ERRORS = {
    "config": {
        "missing_section": "required section '{section}' missing",
        "missing_key": "required key '{key}' in section '{section}' missing",
        "errors": "configuration file {config_file} contains errors",
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
    return f"\033[{';'.join(str(escape_code) for escape_code in (STYLES.get(style, ''), COLOURS['fg'].get(fg, ''), COLOURS['bg'].get(bg, '')) if escape_code)}m{string}\033[m"  # noqa: E501
