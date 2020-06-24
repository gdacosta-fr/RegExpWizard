#!/usr/bin/env python3
# coding: utf-8


from const import _, GETTEXT_DOMAIN, REW_LOCALE_PATH
import locale
import gettext
# On Windows, "locale" does not export "bindtextdomain"
locale.bindtextdomain(GETTEXT_DOMAIN, REW_LOCALE_PATH)  # For Gtk. See https://stackoverflow.com/a/10540744
gettext.bindtextdomain(GETTEXT_DOMAIN, REW_LOCALE_PATH)
gettext.textdomain(GETTEXT_DOMAIN)

import gi
gi.require_version( 'Gtk', '3.0' )

from gi.repository import Gtk
import re
from InterfaceGtk import Environment
from WidgetNode import WidgetNode
from RegExpStack import RegExpStack
from RegularExpressionElement import RegularExpressionElement
import version


#
# Expressions rationelles = Regular Expressions = RegExp = Regex = RE
#
# The goal is not to use the full range of possibilities for Perl RE, but a small subset that should
# be enough for Gramps users.
#
# The reference is the French translation.
#

class RegExpWizard(Environment):
    def __init__(self):
        Environment.__init__(self)

        Environment._GtkInterface.add_from_file('RegExpWizard.glade')

        self._Strings = []      # list of "OR" strings
        self.__BuildWidgetsTree()

        Environment._GtkInterface.connect_signals(self)

        window = Environment._GtkInterface.get_object('RegExpWizardMainWindow')
        window.connect( 'destroy', Gtk.main_quit )

        # Version identification
        window.set_title(window.get_title() + " (" + version.VERSION + ")")

        window.show_all()

        self.RegExpStack = RegExpStack(widget=Environment._GtkInterface.get_object("TxtRegExpClearText"))

        self.TxtRegExp = Environment._GtkInterface.get_object("TxtRegExp")

        # secondary widgets
        self.TxtTestString = Environment._GtkInterface.get_object("TxtTestString")
        self.CheckCase = Environment._GtkInterface.get_object("CheckCase")
        self.LblTestResult = Environment._GtkInterface.get_object("LblTestResult")


    def __BuildWidgetsTree(self):
        # Next step: build this tree from the Glade file...
        # tree is built from the leaves up.
        self.RadioElemEnd = WidgetNode("RadioElemEnd")

        self.TxtChar = WidgetNode("TxtChar")
        self.RadioElemOneCharExcept = WidgetNode("RadioElemOneCharExcept")
        self.RadioElemOneCharAmong = WidgetNode("RadioElemOneCharAmong")
        self.RadioElemOneCharInSet = WidgetNode("RadioElemOneCharInSet", [  self.RadioElemOneCharExcept,
                                                                            self.RadioElemOneCharAmong,
                                                                            self.TxtChar])

        self.RadioElemOneCharAny = WidgetNode("RadioElemOneCharAny")
        self.RadioElemOneChar = WidgetNode("RadioElemOneChar", [    self.RadioElemOneCharAny,
                                                                    self.RadioElemOneCharInSet])

        self.TxtStrings = WidgetNode("TxtStrings")
        self.BtnOr = WidgetNode("BtnOr")
        self.TxtElementaryString = WidgetNode("TxtElementaryString")
        self.RadioElemString = WidgetNode("RadioElemString", [  self.TxtElementaryString,
                                                                self.BtnOr,
                                                                self.TxtStrings])

        self.FrameOccurencesOf = WidgetNode("FrameOccurencesOf", [  self.RadioElemString,
                                                                    self.RadioElemOneChar])

        self.RadioNbOccurrencesAny = WidgetNode("RadioNbOccurrencesAny")

        self.RadioNbOccurrences1orMore = WidgetNode("RadioNbOccurrences1orMore")
        self.RadioNbOccurrences1 = WidgetNode("RadioNbOccurrences1")
        self.RadioNbOccurrences0or1 = WidgetNode("RadioNbOccurrences0or1")
        self.RadioElementNbOccurrences = WidgetNode("RadioElementNbOccurrences", [  self.RadioNbOccurrences0or1,
                                                                                    self.RadioNbOccurrences1,
                                                                                    self.RadioNbOccurrences1orMore,
                                                                                    self.RadioNbOccurrencesAny,
                                                                                    self.FrameOccurencesOf])

        self.RadioElemBeginning = WidgetNode("RadioElemBeginning")

        self.FrameReBuilding = WidgetNode("FrameReBuilding", [  self.RadioElemBeginning,
                                                                self.RadioElementNbOccurrences,
                                                                self.RadioElemEnd])

    def __EvaluateTestRegExp(self):
        result = "" # default, if RE is empty
        retxt = self.TxtRegExp.get_text()
        test_string = self.TxtTestString.get_text()
        if len(retxt) > 0 and len(test_string) > 0:
            ignore_case = not self.CheckCase.get_active()
            if ignore_case:
                reflag = re.IGNORECASE
            else:
                reflag = 0
            rebin = re.compile(retxt, reflag)

            if rebin.search(test_string):
                result = _("Matches")           # TODO: green foreground color
            else:
                result = _("DOES NOT MATCH")    # TODO: red foreground color

        self.LblTestResult.set_text(result)

    def __LockNbOccurences(self, lock=True):
        """
        Lock, or unlock, radio-buttons of the "Number of occurrences" group.
        """
        for rb in self.RadioNbOccurrences1.get_group():
            if not rb.get_active():
                rb.set_sensitive(not lock)

    def RadioButtonChanged(self,widget):
        # Common to all RE building radio buttons
        try:
            # 1) Widgets under the selected button are validated (made sensitive)
            # 2) Widgets under unselected buttons are invalidated
            node = WidgetNode.Dictionary[id(widget)]
            node.ValidateChildren(widget.get_active())
        except:
            # No dictionary. Just ignore.
            pass



    def on_RegExpWizardMainWindow_close(self, widget):
        Gtk.main_quit()

    def on_BtnOr_clicked(self, widget):
        s = self.TxtElementaryString.get_text()
        if len(s) > 0:
            self._Strings.append(s)

            # Display in GtkEntry. Alternative: multiline in a GtkTextView
            if len(self._Strings) > 1:
                # Kludge: as Python 3.5 has no pgettext() function, we need some means for distinguishing opening and
                # closing quotes.
                # "context|string" is a Gramps extension.
                opening_quote = _(" \"")
                closing_quote = _("\" ")
            else:
                opening_quote = ""
                closing_quote = ""

            self.TxtStrings.set_text(   opening_quote
                                        + (closing_quote + _(" or ") + opening_quote).join(self._Strings)
                                        + closing_quote)
            self.TxtElementaryString.set_text("")

            self.__LockNbOccurences()

    def on_BtnAdd_clicked(self,  widget):
        re = None   # current regular expression element
        min = -1
        max = -1


        if self.RadioElemBeginning.get_active():
            re = RegularExpressionElement(preamble="^")
        elif self.RadioElementNbOccurrences.get_active():
            # N occurrences of...
            if self.RadioNbOccurrences0or1.get_active():
                min = 0
                max = 1
            elif self.RadioNbOccurrences1.get_active():
                min = 1
                max = 1
            elif self.RadioNbOccurrences1orMore.get_active():
                min = 1
                max = -1
            elif self.RadioNbOccurrencesAny.get_active():
                min = 0
                max = -1

            if self.RadioElemString.get_active():
                # If user has not clicked a last time on "OR" button, do it for him.
                self.on_BtnOr_clicked(None)  # widget inutilisé
                re = RegularExpressionElement(preamble="(", strings=self._Strings, postamble=")", min=min, max=max)
            elif self.RadioElemOneChar.get_active():
                # One character in a set
                if self.RadioElemOneCharAny.get_active():
                    # we're cheating: it's not really a preambule. This way, it will not be escaped.
                    re = RegularExpressionElement(preamble=".", min=min, max=max)
                elif self.RadioElemOneCharInSet.get_active():
                    if self.RadioElemOneCharExcept.get_active():
                        except_char="^"
                    else:
                        except_char=""
                    string = Environment._GtkInterface.get_object("TxtChar").get_text()
                    re = RegularExpressionElement(preamble="[" + except_char, strings=[string], postamble="]", min=min, max=max)
        elif self.RadioElemEnd.IsSensitiveAndActive():
            re = RegularExpressionElement( postamble="$")
            # "end of string" is selected, so it's not possible anymore to add something to the RE
            self.FrameReBuilding.Validate(False)

        if re is not None:
            self.RegExpStack.Push(re)
            # Display the RE
            retxt = self.RegExpStack.GetRegExp()
            self.TxtRegExp.set_text(retxt)


        if not self.RegExpStack.IsEmpty():
            # Beginning of line is significant... at the beginning.
            # set_active(False) does not work on a radio button.
            if  self.RadioElemBeginning.IsSensitiveAndActive():
                self.RadioElementNbOccurrences.set_active(True)
            self.RadioElemBeginning.set_sensitive(False)

        self.__ClearEnteredData()
        self.__LockNbOccurences(False)


    def __ClearEnteredData(self):
        for w in [ self.TxtElementaryString, self.TxtStrings, self.TxtChar ]:
            w.set_text("")
        self._Strings = []

    def __ClearResults(self):
        for w in ("TxtRegExpClearText",  "TxtRegExp"):
            Environment._GtkInterface.get_object(w).set_text("")
        self.RegExpStack.Clear()

    def on_BtlClearAll_clicked(self,  widget):
        self.__ClearEnteredData()
        self.__ClearResults()
        self.FrameReBuilding.Validate(True)

    # Signal not found in documentation, but known by Glade
    def on_TxtTestString_changed(self,  widget):
        self.__EvaluateTestRegExp()

    def on_CheckCase_toggled(self, widget):
        self.__EvaluateTestRegExp()

    def on_TxtRegExp_changed(self, widget):
        self.__EvaluateTestRegExp()

def main():
    rew = RegExpWizard()    # useless variable, but make debug easy
    Gtk.main()

if __name__ == "__main__":
    main()


# vim: tabstop=4:shiftwidth=4:expandtab
