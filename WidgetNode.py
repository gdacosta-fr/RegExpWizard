#!/usr/bin/env python3
# coding: utf-8


import gi
gi.require_version( 'Gtk', '3.0' )

from gi.repository import Gtk

from InterfaceGtk import GtkInterface
from Node import Node


class WidgetNode(Node,GtkInterface):

    # Static dictionary of all nodes, indexed by widget
    Dictionary = {}

    def __init__(self,nom_widget,enfants_noeuds_widget=None):
        GtkInterface.__init__(self)
        Node.__init__(self, nom=nom_widget,children=enfants_noeuds_widget)

        self.Widget = GtkInterface.top.get_object(nom_widget)
        # Add object in the dictionary
        WidgetNode.Dictionary[id(self.Widget)] = self

    def __getattr__(self, attr):
        """
        All unknown attributes are delegated to the embedded widget object: get_active (), get_text (), ...
        A WidgetNode is virtually any widget.
        """
        return self.Widget.__getattribute__(attr)

    def IsSensitiveAndActive(self):
        return self.is_sensitive() and self.get_active()

    def SetActiveIfSensitive(self,active=True):
        if self.is_sensitive():
            self.set_active(active)



    #
    # Invalidation is unconditional
    # Validation is conditioned by the selection of the widget.
    # If the button is selectable (radio button, check box), children are validated only if the button is
    # selected.
    #
    # "set_sensitive" is a GtkWidget method: all widgets inherit it.
    #
    def Validate(self,validate=True):
        """
        Recursively (in)validate the widget
        """
        w = self.Widget
        w.set_sensitive(validate)    # current widget

        # children widgets
        # there is probably a more concise way to write, but not necessarily clearer
        if validate:
            if isinstance(w,Gtk.ToggleButton):
                if w.get_active():
                    self.ValidateChildren(True)
                else:
                    self.ValidateChildren(False)
            else:
                self.ValidateChildren(True)
        else:
            self.ValidateChildren(False)

    def ValidateChildren(self,validate=True):
        """
        (In)Valid recursively the children of the widget, but not the widget itself
        """
        for n in self.Children:
            n.Validate(validate)


# vim: tabstop=4:shiftwidth=4:expandtab
