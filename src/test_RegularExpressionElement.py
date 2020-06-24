#!/usr/bin/env python3
# coding: utf-8


import unittest
from RegularExpressionElement import RegularExpressionElement
from const import _


class TestRegularExpressionElement(unittest.TestCase):

    def test_RegularExpressionElement(self):

        ree = RegularExpressionElement(preamble="", strings=[""], postamble="", min=-1, max=-1)
        self.assertEqual( str(ree), _("INTERNAL ERROR the number of occurrences is missing"))

        ree = RegularExpressionElement(preamble="^", strings=[""], postamble="", min=-1, max=-1)
        self.assertEqual(str(ree), _("INTERNAL ERROR the number of occurrences is missing"))

        ree = RegularExpressionElement(preamble="", strings=[""], postamble="$", min=-1, max=-1)
        self.assertEqual(str(ree), _("INTERNAL ERROR the number of occurrences is missing"))


        ree = RegularExpressionElement(preamble="", strings=["ga bu"], postamble="", min=1, max=1)
        self.assertEqual(str(ree), _("1 occurrence exactly of \"ga bu\""))

        ree = RegularExpressionElement(preamble="", strings=["ga bu"], postamble="", min=0, max=1)
        self.assertEqual(str(ree), _("0 or 1 occurrence of \"ga bu\""))

        ree = RegularExpressionElement(preamble="", strings=["ga bu"], postamble="", min=0, max=-1)
        self.assertEqual(str(ree), _("Any number of occurrences of \"ga bu\""))

        ree = RegularExpressionElement(preamble="", strings=["ga bu"], postamble="", min=1, max=-1)
        self.assertEqual(str(ree), _("At least 1 occurrence of \"ga bu\""))

        ree = RegularExpressionElement(preamble="", strings=["ga bu"], postamble="", min=-1, max=-1)
        self.assertEqual(str(ree), _("INTERNAL ERROR the number of occurrences is missing"))

        ree = RegularExpressionElement(preamble="", strings=[], postamble="", min=1, max=-1)    # TODO: corriger
        self.assertEqual(str(ree), _("At least 1 occurrence"))

        ree = RegularExpressionElement(preamble="", strings=["ga", "bu", "zo", "meu"], postamble="", min=1, max=1)
        self.assertEqual(str(ree), _("1 occurrence exactly of \"ga\" ou \"bu\" ou \"zo\" ou \"meu\""))

        ree = RegularExpressionElement(preamble="", strings=["ga", "bu", "zo", "meu"], postamble="", min=0, max=-1)
        self.assertEqual(str(ree), _("Any number of occurrences of \"ga\" ou \"bu\" ou \"zo\" ou \"meu\""))

        ree = RegularExpressionElement(preamble="[", strings=["eéèêë"], postamble="]", min=1, max=-1)
        self.assertEqual(str(ree), _("At least 1 occurrence of a character among \"eéèêë\""))

        ree = RegularExpressionElement(preamble="[^", strings=["aàáäâ"], postamble="]", min=0, max=1)
        self.assertEqual(str(ree), _("0 ou 1 occurrence of one character other than \"aàáäâ\""))


if __name__ == '__main__':
    unittest.main()

# vim: tabstop=4:shiftwidth=4:expandtab
