

"""
This module provides some resources, either from the Gramps environment if
available, or from some defaults and fallbacks.
Exports:
    RunningUnderGramps: False, if script is running autonomously, True if running as a Gramplet.
    win(): return True if OS is Windows
    _: string translation
"""

import sys

RunningUnderGramps = False

if "gramps" in sys.modules:
    RunningUnderGramps = True

    #------------------------------------------------------------------------
    #
    # Gramps modules
    #
    #------------------------------------------------------------------------
####    from gramps.gui.dialog import ErrorDialog, WarningDialog
    ####    from gramps.gen.plug import Gramplet
    ####    from gramps.gen.lib import StyledText, StyledTextTag, StyledTextTagType
    ####    from gramps.gen.config import config
    from gramps.gen.constfunc import win
    ####    from gramps.gui.display import display_url
    ####    from gramps.gen.display.place import displayer as _pd


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
else:
    #
    # Fallbacks
    #

    # Extracted from "gramps/gen/constfunc.py"

    import platform

    WINDOWS = ["Windows", "win32"]

    def win():
        """
        Return True if a windows system
        """
        if platform.system() in WINDOWS:
            return True
        return False

    # ---------------------------------------

    import gettext

    _ = gettext.gettext

