#!/usr/bin/env python3
# coding: utf-8



class RegExpStack:
    def __init__(self, widget=None):
        """
        widget: object (vs name), with a "set_text()" method, where the stack content is written.
        """
        self._Stack = []
        self._Widget = widget

        self.Print()

    def Push(self, re):
        self._Stack.append(re)
        self.Print()

    def Clear(self):
        self._Stack.clear()
        self.Print()

    def GetText(self):
        """Get the content of the stack, in clear text"""
        lsct=[]    # List of Strings in Clear Text
        for re in self._Stack:
            lsct += str(re)
            lsct += "\n"

        return "".join(lsct)

    def GetRegExp(self):
        """
        Return concatened regular expressions
        """
        re=[]
        for element in self._Stack:
            re.append(element.EscapedRe)

        return "".join(re)

    def Print(self):
        """
        Display the RE description in clear text, in the widget
        """
        if self._Widget is not None:
            self._Widget.set_text(self.GetText())

    def IsEmpty(self):
        return len(self._Stack) == 0



# vim: tabstop=4:shiftwidth=4:expandtab