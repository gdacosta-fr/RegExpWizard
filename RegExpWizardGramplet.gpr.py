#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2020      G.Da Costa
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
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

"""
Regular Expressions Wizard Gramplet.
"""



#
# Version identifiers, inspired by gramps/version.py
#

### The following values may be used/modified by an external program (Git,...) ######
GRAMPLET_VERSION_TUPLE = (2, 51, 1)
GRAMPLET_VERSION_QUALIFIER = ""
GRAMPS_TARGET_VERSION = "5.1"
# plus
GRAMPLET_NAVTYPES = [ "Person", "Family", "Event", "Place", "Source", "Citation", "Repository", "Media", "Note" ]
############################################################################# End ###

GRAMPLET_VERSION = '.'.join(map(str,GRAMPLET_VERSION_TUPLE)) + GRAMPLET_VERSION_QUALIFIER



#
# Reference: gramps/gen/plug/_pluginreg.py
#
register(
    GRAMPLET,
    id = "RegExpWizard",
    name = _("Regular Expressions Wizard"),
    description = _("Regular Expressions Wizard Gramplet assists you in building regular expressions, used for "
                        "searching database records"),
    authors = ["G.Da Costa"],
    authors_email = ["regexp-wizard@gdacosta.fr"],
    status = STABLE,
    version = GRAMPLET_VERSION,
    gramps_target_version = GRAMPS_TARGET_VERSION,
    fname = "RegExpWizardGramplet.py",
    gramplet = 'RegExpWizardGramplet',  # Class name
    navtypes = GRAMPLET_NAVTYPES,
    height = 375,
    detached_width = 510,
    detached_height = 480,
    expand = True,
    gramplet_title = _("Regular Expressions"),
    help_url= None, # TODO: URL @ gdacosta.fr
    include_in_listing = True,
    )
