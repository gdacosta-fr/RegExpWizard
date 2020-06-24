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
from gi.repository import Gtk

#------------------------------------------------------------------------
#
# Gramps modules
#
#------------------------------------------------------------------------
from gramps.gen.plug import Gramplet
from gramps.gen.config import config
from gramps.gen.constfunc import win
from gramps.gen.display.place import displayer as _pd


#------------------------------------------------------------------------
#
# Internationalisation
#
#------------------------------------------------------------------------
from gramps.gen.const import GRAMPS_LOCALE as glocale
try:
    _trans = glocale.get_addon_translator(__file__)
except ValueError:
    _trans = glocale.translation
_ = _trans.gettext

from RegExpWizard import RegExpWizard

#-------------------------------------------------------------------------
#
# configuration
#
#-------------------------------------------------------------------------

GRAMPLET_CONFIG_NAME = "regexp_wizard_gramplet"
CONFIG = config.register_manager(GRAMPLET_CONFIG_NAME)
CONFIG.register("preferences.text", '')
CONFIG.register("preferences.boolean", True)
CONFIG.load()


#------------------------------------------------------------------------
#
# GrampletSkeleton class
#
#------------------------------------------------------------------------
class RegExpWizardGramplet(Gramplet,RegExpWizard):
    # Overrides Gramplet.init()
    def init(self):
        """
        Initialise the gramplet.
        """
        self.text_parameter = CONFIG.get("preferences.text")
        self.boolean_parameter = CONFIG.get("preferences.boolean")

        RegExpWizard.__init__(self)

        root = self.__create_gui()
        self.gui.get_container_widget().remove(self.gui.textview)
        self.gui.get_container_widget().add(root)
        root.show_all()

    def __create_gui(self):
        """
        Create and display the GUI components of the gramplet.
        """
        if False:
            self.top = Gtk.Builder()  # IGNORE:W0201
            # Found out that Glade does not support translations for plugins, so
            # have to do it manually.
            base = os.path.dirname(__file__)
            glade_file = base + os.sep + "RegExpWizard.glade"
            # This is needed to make gtk.Builder work by specifying the
            # translations directory in a separate 'domain'
            try:
                localedomain = "addon"
                localepath = base + os.sep + "locale"
                if hasattr(locale, 'bindtextdomain'):
                    libintl = locale
                elif win():  # apparently wants strings in bytes
                    localedomain = localedomain.encode('utf-8')
                    localepath = localepath.encode('utf-8')
                    libintl = ctypes.cdll.LoadLibrary('libintl-8.dll')
                else:  # mac, No way for author to test this
                    libintl = ctypes.cdll.LoadLibrary('libintl.dylib')

                libintl.bindtextdomain(localedomain, localepath)
                libintl.textdomain(localedomain)
                libintl.bind_textdomain_codeset(localedomain, "UTF-8")
                # and finally, tell Gtk Builder to use that domain
                self.top.set_translation_domain("addon")
            except (OSError, AttributeError):
                # Will leave it in English
                print("Localization of RegExpWizard failed!")

            self.top.add_from_file(glade_file)

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

    # ======================================================
    # gramplet event handlers
    # ======================================================
    def on_help_clicked(self, dummy):
    	pass

    # Overrides Gramplet.on_save()
    def on_save(self, *args, **kwargs):
        CONFIG.set("preferences.text", self.text_parameter)
        CONFIG.set("preferences.boolean", self.boolean_parameter)
        CONFIG.save()

    # Overrides Gramplet.db_changed()
    def db_changed(self):
    	pass

    # Overrides Gramplet.main()
    def main(self):
        active_handle = self.get_active('Place')    # TODO: active window
        if active_handle:
            self.place = self.dbstate.db.get_place_from_handle(active_handle)
            self.mainwin.hide()
            if self.place:
                self.set_has_data(True)
                title = _pd.display(self.dbstate.db, self.place)
            else:
                self.set_has_data(False)
            self.mainwin.show()
        else:
            self.set_has_data(False)

    def on_find_clicked(self, dummy):
    	pass


# Preferences dialog items

    def on_prefs_clicked(self, dummy):
        pass

    def on_pref_help_clicked(self, dummy):
    	pass

    def on_main_destroy(self, dummy):
        pass

# vim: tabstop=4:shiftwidth=4:expandtab
