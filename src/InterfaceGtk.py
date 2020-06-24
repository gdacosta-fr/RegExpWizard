#!/usr/bin/env python3
# coding: utf-8

import const
import locale
import os
import ctypes
import gi
gi.require_version( 'Gtk', '3.0' )

from gi.repository import Gtk



class GtkInterface:
    # Static data
    top = None  # Not my better idea: class data named "top"
                # and instance data also named "top"...
    package_path = None

    def __init__(self):
        if GtkInterface.top is None:
            GtkInterface.top = Gtk.Builder()
        self.top = GtkInterface.top   # make compatible with PlaceCleanup gramplet code

        # following code, including comments, is borrowed from PlaceCleanup.__create_gui()

        # Found out that Glade does not support translations for plugins, so
        # have to do it manually.
        GtkInterface.package_path = os.path.dirname(__file__) + os.sep   # Terminated by "/"
        # This is needed to make gtk.Builder work by specifying the
        # translations directory in a separate 'domain'
        try:
            localedomain = const.GETTEXT_DOMAIN
            localepath = GtkInterface.package_path + "locale"
            if hasattr(locale, 'bindtextdomain'):
                libintl = locale
            elif win():  # apparently wants strings in bytes
                localedomain = localedomain.encode('utf-8')
                localepath = localepath.encode('utf-8')
                libintl = ctypes.cdll.LoadLibrary('libintl-8.dll')
            else:   # mac, No way for author to test this (PC)
                    # Neither do I (GdC)
                libintl = ctypes.cdll.LoadLibrary('libintl.dylib')

            libintl.bindtextdomain(localedomain, localepath)
            libintl.textdomain(localedomain)
            libintl.bind_textdomain_codeset(localedomain, "UTF-8")
            # and finally, tell Gtk Builder to use that domain
            self.top.set_translation_domain(const.GETTEXT_DOMAIN)
        except (OSError, AttributeError):
            # Will leave it in English
            print("Localization of RegExpWizard failed!")





# vim: tabstop=4:shiftwidth=4:expandtab