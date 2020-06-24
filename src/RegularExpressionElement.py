#!/usr/bin/env python3
# coding: utf-8

from GrampsOrNotGramps import _

#
# Expressions rationelles = Regular Expressions = RegExp = Regex = RE
#
# The goal is not to use the full range of possibilities for Perl RE, but a small subset that should
# be enough for Gramps users.
#


#
# Ancillary class, intended to collect all the parameters necessary for the construction of a RE element
# An object can be built in several steps. The string in clear text and the quantizer can not be
# built before all elements are available.
#
class RegularExpressionElement:
    """
    min, max: number of occurrences. By convention, -1 = infinite. min == - 1: these parameters are not significant
     strings: list. 1 item for sets.
    """
    def __init__(self,  preamble="",  strings=[],  postamble="", min=-1, max=-1):
        self._Preamble = preamble
        self._Strings = strings
        self._Postamble = postamble
        self._Min = min
        self._Max = max
        # The following members are evaluated from the previous ones
        self._Quantifier = None
        self._ClearText = None
        self.EscapedRe = None  # Public (or get()/set()?)

    #
    # Clear representation of the RE
    #
    # This function has 2 side effects:
    # 1) check the consistency of the parameters
    # 2) evaluate the quantizer
    #
    def __str__(self):
        self.Evaluate()
        return self._ClearText

    def Evaluate(self):
        """
        Evaluates the computed members, based on the parameter members.
        The RE is escaped. The description in clear is constructed.
        Side effect: checks the consistency of the parameters.
        Possibly, the evaluation can take place several times, after changing the parameters
        """
        result=""
        occurrences=""  # singular or plural

        self._Quantifier = ""

        if self._Min == -1  and  self._Max == -1  and  self._Strings == []:
            # The number of occurrences is not significant
            if self._Preamble == "^"  and  self._Postamble == "":
                result = _("Start of string")
            elif self._Preamble == ""  and  self._Postamble == "$":
                result = _("End of string")
        else:
            # In all other cases, the number of occurrences must be specified
            if self._Min == -1:
                result = _("INTERNAL ERROR the number of occurrences is missing")
            else:
                if self._Max != -1  and  self._Max < self._Min:
                    result = _("INTERNAL ERROR max < min")
                else:
                    # a syntactically correct number of occurrences is specified

                    #
                    # Yes, I know: concatenating strings does not help translation.
                    # Maybe one day...
                    #

                    # plural begins at 2, up to infinity
                    if self._Max > 1  or  self._Max == -1:
                        occurrences = _("occurrences")    # plural
                    else:
                        occurrences = _("occurrence")     # singular

                    if self._Min == self._Max:
                        result = str(self._Min) + _(" ") + occurrences + _(" exactly")
                        if self._Min == 1:
                            self._Quantifier = ""
                        else:
                            self._Quantifier = "{" + str(self._Min) + "}"
                    else:
                        # min and max are different
                        if self._Min == 0  and  self._Max == -1:
                            result = _("Any number of occurrences")
                            self._Quantifier = "*"
                        elif self._Min == 1  and  self._Max == -1:
                            result = _("At least 1 occurrence")
                            self._Quantifier = "+"
                        elif self._Min == 0  and  self._Max == 1:
                            result = _("0 ou 1 occurrence")
                            self._Quantifier = "?"
                        else:
                            result = _("INTERNAL ERROR the number of occurrences {n,m} is not taken into account")

                    if len(self._Preamble) == 1  and  self._Preamble == "."  and  len(self._Postamble) == 0:
                        # trick: the "." is considered preamble not to be escaped
                        result += _(" of any character")
                    elif len(self._Preamble) >= 1  and  self._Preamble[0] == "["  and  self._Postamble == "]":
                        result += _(" of one character")
                        if len(self._Preamble) == 1:
                            result += _("among \"")
                        elif self._Preamble == "[^":
                            result += _("other than \"")
                        else:
                            result += _("INTERNAL ERROR set \"")
                        result += ( self._Strings[0] + _("\" "))   # TODO: s'assurer que Chaines comporte au moins 1 élément
                    else:
                        if len(self._Strings) >= 1:
                            result += _(" of \"") + _("\" or \"").join(self._Strings) + _("\" ")

        self._ClearText = result

        # Escaping
        escaped_string=""
        if (len(self._Preamble) >= 2) and (self._Preamble[0] == "[") and (self._Preamble[-1] == "]"):
            # it's a set of characters (range) of the form "[xyz]"
            escaped_string = RegularExpressionElement.__EscapeSet(self._Strings[0])
        else:
            # it's a list of strings
            escaped_list=[]
            for string in self._Strings:
                escaped_list.append(RegularExpressionElement.__EscapeString(string))
            escaped_string = "|".join(escaped_list)

        # Constitution of the compilable RE
        self.EscapedRe = self._Preamble + escaped_string + self._Postamble + self._Quantifier


    @staticmethod
    def __Escape(string, escape_these_characters):
        """
        From a raw regular expression, escape the special characters, and take care of other special cases.
        """
        result=string
        for to_be_escaped in escape_these_characters:
            result = result.replace(to_be_escaped, "\\"+to_be_escaped)

        return result

    @staticmethod
    def __EscapeString(string):
        """
        From a raw regular expression, escape special characters, and take care of other special cases.
        """
        return RegularExpressionElement.__Escape(string, "\\.[{()*+?^$|")    # SPECIAL_CHARS. ** WARNING **: "\" must be the first character to escape!



    @staticmethod
    def __EscapeSet(ensemble):
        """
        From a raw regular expression, escape special characters, and take care of other special cases.
        """
        # special case of [xyz], where special characters are no longer special
        return RegularExpressionElement.__Escape(ensemble, "\\^-]")  # ** WARNING **: "\" must be the first character to escape!



# vim: tabstop=4:shiftwidth=4:expandtab
