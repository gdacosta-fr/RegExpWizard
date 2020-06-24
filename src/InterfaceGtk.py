#!/usr/bin/env python3
# coding: utf-8

import const
import gi
gi.require_version( 'Gtk', '3.0' )

from gi.repository import Gtk



class Environment:
    # Static data
    _GtkInterface = None

    def __init__(self):
        if Environment._GtkInterface is None:
            Environment._GtkInterface = Gtk.Builder()
            Environment._GtkInterface.set_translation_domain(const.GETTEXT_DOMAIN)



# vim: tabstop=4:shiftwidth=4:expandtab