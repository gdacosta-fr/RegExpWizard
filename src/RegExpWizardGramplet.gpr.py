#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2019      G.Da Costa
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


import version


register(
    GRAMPLET,
    id = "RegExpWizard",
    name = _("Regular Expressions Wizard"),
    description = _("Regular Expressions Wizard Gramplet assists you in building regular expressions, used for "
                        "searching database records"),
    authors = ["G.Da Costa"],
    authors_email = ["regexp-wizard@gdacosta.fr"],  # TODO: Créer cette adresse
    status = STABLE,
    version = version.VERSION,
    gramps_target_version = '5.1',
    fname = "RegExpWizardGramplet.py",
    gramplet = 'RegExpWizardGramplet',  # Class name
    navtypes=["Person", "Place"],       # TODO: compléter
    height = 375,
    detached_width = 510,
    detached_height = 480,
    expand = True,
    gramplet_title = _("Regular Expressions Wizard"),
    help_url= None, # TODO: URL @ gdacosta.fr
    include_in_listing = True,
    )
