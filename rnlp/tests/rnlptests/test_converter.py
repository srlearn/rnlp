# Copyright (C) 2017-2018 StARLinG Lab
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (at the base of this repository). If not,
# see <http://www.gnu.org/licenses/>

import sys
import unittest

sys.path.append('./')

import rnlp

class converterTest(unittest.TestCase):
    """
    This performs a similar test to test_parse.py, but uses rnlp.convert.
    """

    def test_converter_1(self):

        example = "Hello there. How are you? I am fine."
        rnlp.converter(example)
