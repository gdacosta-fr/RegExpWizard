from collections import namedtuple

"""
Description of Gramplets where RegExpWizard is able to paste its results
view_type: type of the view where the Gramplet may be used.
gramplet_name: name of associated Gramplet.
re_field: name of the *SidebarFilter field, where the RegExp may be pasted.
          Must be a GtkEntry (BasicEntry).
"""

AssociatedGramplet = namedtuple( "AssociatedGramplet", "view_type gramplet_name re_field")



#
# This class may be extended in order to read and write configuration files.
#
# As of today, it's no more than a name space.
#
class Configuration:
    """
    Encapsulates RegExpWizard parameters
    """

    #
    # Class data
    #
    AssociatedGramplets = \
    [
        # View types: see "FILTER_TYPE" values
        # Filter names: see ???
        AssociatedGramplet("Person", "Person Filter", "filter_name"),
        AssociatedGramplet("Family", "Family Filter", "filter_father"),    # No sexism. Pragmatism!
        AssociatedGramplet("Event", "Event Filter", "filter_desc"),
        AssociatedGramplet("Place", "Place Filter", "filter_name"),
        AssociatedGramplet("Source", "Source Filter", "filter_title"),
        AssociatedGramplet("Citation", "Citation Filter", "filter_src_title"),
        AssociatedGramplet("Repository", "Repository Filter", "filter_title"),
        AssociatedGramplet("Media", "Media Filter", "filter_title"),
        AssociatedGramplet("Note", "Note Filter", "filter_text")
    ]

    def __init__(self):
        pass

    #
    # Class methods
    #
    def get_views():
        """
        :return: a list of view types, where the Gramplet can be launched.
        """
        return [ gramplet.view_type for gramplet in Configuration.AssociatedGramplets ]

    def get_associated_gramplets_name():
        return [ gramplet.gramplet_name for gramplet in Configuration.AssociatedGramplets ]

    def get_re_field_from(gramplet_name):
        result = None
        for associated_gramplet in Configuration.AssociatedGramplets:
            if associated_gramplet.gramplet_name == gramplet_name:
                result = associated_gramplet.re_field
                break

        return result
