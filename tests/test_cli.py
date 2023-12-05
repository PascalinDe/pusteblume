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
:synopsis: Command-line interface tests.
"""


# standard library imports
import argparse
import unittest

# third party imports
# library specific imports
import pusteblume.cli
import pusteblume.errors


class ArgumentTypeTestCase(unittest.TestCase):
    """Argument type test case."""

    def test_valid_name(self):
        """Test 'name' argument type.

        Trying: valid name
        Expecting: name
        """
        name = "write test cases"
        self.assertEqual(pusteblume.cli.name(name), name)

    def test_invalid_name(self):
        """Test 'name' argument type.

        Trying: invalid name
        Expecting: ArgumentTypeError
        """
        with self.assertRaises(argparse.ArgumentTypeError) as exception:
            pusteblume.cli.name(pusteblume.cli._RESERVED_CHARS)
            self.assertEqual(
                str(exception),
                pusteblume.errors.ERRORS["cli"]["reserved_chars"].format(
                    string=pusteblume.cli._RESERVED_CHARS,
                    reserved_chars=pusteblume.cli._RESERVED_CHARS,
                ),
            )

    def test_valid_tag(self):
        """Test 'tag' argument type.

        Trying: valid tag
        Expecting: tag
        """
        tag = "pusteblume"
        self.assertEqual(pusteblume.cli.tag(f"[{tag}]"), tag)

    def test_invalid_tag(self):
        """Test 'tag' argument type.

        Trying: invalid tag
        Expecting: ArgumentTypeError
        """
        with self.assertRaises(argparse.ArgumentTypeError) as exception:
            string = "pusteblume"
            pusteblume.cli.tag(string)
            self.assertEqual(
                str(exception),
                pusteblume.errors.ERRORS["cli"]["invalid_tag"].format(
                    string=string,
                ),
            )
        with self.assertRaises(argparse.ArgumentTypeError) as exception:
            pusteblume.cli.tag(f"[{pusteblume.cli._RESERVED_CHARS}]")
            self.assertEqual(
                str(exception),
                pusteblume.errors.ERRORS["cli"]["reserved_chars"].format(
                    string=pusteblume.cli._RESERVED_CHARS,
                    reserved_chars=pusteblume.cli._RESERVED_CHARS,
                )
            )


class SplitTestCase(unittest.TestCase):
    """Command-line arguments splitting test case."""

    def test_start(self):
        """Test splitting 'start' subcommand and its command-line arguments.

        Trying: split 'start' subcommand and its command-line arguments
        Expecting: 'start' subcommand and its command-line arguments
        """
        args = ["start", "write test cases"]
        # name
        self.assertListEqual(pusteblume.cli.split(args), args)
        # name and tags
        args = [*args, "[pusteblume]", "[v1.2]"]
        self.assertListEqual(pusteblume.cli.split(args), args)

    def test_stop(self):
        """Test splitting 'stop' subcommand.

        Trying: split 'stop' subcommand
        Expecting: 'stop' subcommand
        """
        args = ["stop"]
        self.assertListEqual(pusteblume.cli.split(args), args)

    def test_list(self):
        """Test splitting 'list' subcommand.

        Trying: split 'list' subcommand
        Expecting: 'list' subcommand
        """
        args = ["list"]
        self.assertListEqual(pusteblume.cli.split(args), args)

    def test_status(self):
        """Test splitting 'status' subcommand.

        Trying: split 'status' subcommand
        Expecting: 'status' subcommand
        """
        args = ["status"]
        self.assertListEqual(pusteblume.cli.split(args), args)

    def test_edit(self):
        """Test splitting 'edit' subcommand.

        Trying: split 'edit' subcommand
        Expecting: 'edit' subcommand and its command-line arguments
        """
        args = ["edit", "write test cases"]
        # name
        self.assertListEqual(pusteblume.cli.split(args), args)
        # name and tags
        args = [*args, "[pusteblume]", "[v1.2]"]
        self.assertListEqual(pusteblume.cli.split(args), args)
