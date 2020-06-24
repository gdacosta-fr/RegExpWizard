# -*- coding: utf-8 -*-
#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2018      Paul Culley
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#
# Gramplet Skeleton Gramplet.
#
# pylint: disable=attribute-defined-outside-init

#------------------------------------------------------------------------
#
# Python modules
#
#------------------------------------------------------------------------
import os
import ctypes
import locale

#------------------------------------------------------------------------
#
# GTK modules
#
#------------------------------------------------------------------------
import gi
gi.require_version( 'Gtk', '3.0' )
from gi.repository import Gtk

import re

#------------------------------------------------------------------------
#
# Gramps modules
#
#------------------------------------------------------------------------
from gramps.gen.plug import Gramplet

from InterfaceGtk import GtkInterface
from WidgetNode import WidgetNode
from RegExpStack import RegExpStack
from RegularExpressionElement import RegularExpressionElement

from i18n import _

from Configuration import Configuration



#
# Expressions rationelles = Regular Expressions = RegExp = Regex = RE
#
# The goal is not to use the full range of possibilities for Perl RE, but a small subset that should
# be enough for Gramps users.
#
# Initialization is done by overridden init() method, vs __init__().
# The reference is the French translation.

class RegExpWizardGramplet(Gramplet,GtkInterface):

    # Overrides Gramplet.init()
    def init(self):
        """
        Initialise the gramplet.
        """
        GtkInterface.__init__(self)

        GtkInterface.top.add_from_file(self.package_path + "RegExpWizard.glade")

        self._Strings = []      # list of "OR" strings
        self.__BuildWidgetsTree()

        GtkInterface.top.connect_signals(self)

        window = GtkInterface.top.get_object('main')
        window.connect( 'destroy', Gtk.main_quit )

        window.show_all()

        self.RegExpStack = RegExpStack(widget=GtkInterface.top.get_object("TxtRegExpClearText"))

        self.TxtRegExp = GtkInterface.top.get_object("TxtRegExp")

        # secondary widgets
        self.TxtTestString = GtkInterface.top.get_object("TxtTestString")
        self.CheckCase = GtkInterface.top.get_object("CheckCase")
        self.LblTestResult = GtkInterface.top.get_object("LblTestResult")

        # Outside of the main widgets tree
        self.BtnPaste = WidgetNode("BtnPaste")

        root = self.__create_gui()
        self.gui.get_container_widget().remove(self.gui.textview)
        self.gui.get_container_widget().add(root)
        root.show_all()

    def __create_gui(self):
        """
        Create and display the GUI components of the gramplet.
        """
        # the results screen items
        self.top.connect_signals({
            "on_main_destroy"   : self.on_main_destroy,
            "on_main_close" : self.on_main_close,
            "RadioButtonChanged": self.RadioButtonChanged,
            "on_BtnOr_clicked": self.on_BtnOr_clicked,
            "on_BtnAdd_clicked": self.on_BtnAdd_clicked,
            "on_BtlClearAll_clicked": self.on_BtlClearAll_clicked,
            "on_TxtTestString_changed": self.on_TxtTestString_changed,
            "on_CheckCase_toggled": self.on_CheckCase_toggled,
            "on_TxtRegExp_changed": self.on_TxtRegExp_changed
        })
        # main screen items
        self.mainwin = self.top.get_object("main")
        return self.mainwin

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

    #
    # Inspired by GrampletBar.all_gramplets()
    #
    def enumerate_siblings(self):
        """
        Enumerates all active TabGramplet objects, including the one associated to this Gramplet, in the current view.
        """
        tabgramplet = self.gui
        grampletbar = tabgramplet.pane
        if grampletbar.empty:
            return grampletbar.detached_gramplets
        else:
            return [gramplet for gramplet in grampletbar.get_children() +
                    grampletbar.detached_gramplets]

    def get_associated_filter_gramplet(self):
        """
        :return: The 1st Filter gramplet (class: TabGramplet) found in the current view (normally, at most 1)
        """
        result = None
        siblings = self.enumerate_siblings()
        for sibling in siblings:
            if  sibling.gname in Configuration.get_associated_gramplets_name():
                result = sibling
                # Stop on 1st occurrence
                break

        return result

    # ======================================================
    # gramplet event handlers
    # ======================================================

    def on_main_close(self, widget):
        Gtk.main_quit()

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
                    string = GtkInterface.top.get_object("TxtChar").get_text()
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
            GtkInterface.top.get_object(w).set_text("")
        self.RegExpStack.Clear()

    def on_BtlClearAll_clicked(self,  widget):
        self.__ClearEnteredData()
        self.__ClearResults()
        self.FrameReBuilding.Validate(True)

    def on_BtnPaste_clicked(self,  widget):
        """
        Paste regular expression, in "Filter" Gramplet
        """
        try:
            associated_tabgramplet = self.get_associated_filter_gramplet()
            if associated_tabgramplet:
                xxxfilter = associated_tabgramplet.pui # Plugin User Interface
                xxxsidebarfilter = xxxfilter.filter
                # Check the "Use regular expressions" box
                chkbtnregex = xxxsidebarfilter.filter_regex
                chkbtnregex.set_active(True)
                # Write the regexp in associated filter tab
                re_field = Configuration.get_re_field_from(associated_tabgramplet.gname)
                gtkentryre = getattr(xxxsidebarfilter, re_field, None)
                if gtkentryre:
                    gtkentryre.set_text(self.TxtRegExp.get_text())

                # Activate associated filter tab
                tabgramplet = self.gui
                grampletbar = tabgramplet.pane
                page_number = grampletbar.page_num(associated_tabgramplet)
                if page_number >= 0:
                    # Found the filter Gramplet page. Select it.
                    grampletbar.set_current_page(page_number)
        except:
            pass

    # Signal not found in documentation, but known by Glade
    def on_TxtTestString_changed(self, widget):
        self.__EvaluateTestRegExp()

    def on_CheckCase_toggled(self, widget):
        self.__EvaluateTestRegExp()

    def on_TxtRegExp_changed(self, widget):
        self.__EvaluateTestRegExp()

    def on_main_destroy(self, dummy):
        pass

# vim: tabstop=4:shiftwidth=4:expandtab
