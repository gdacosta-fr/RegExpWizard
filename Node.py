#!/usr/bin/env python3
# coding: utf-8



class Node:
    """
    Inspired by <https://stackoverflow.com/a/28015122>
    """
    def __init__(self, nom=None, children=None):
        self.Name = nom
        self.Children = []

        if children is not None:
            # children may be a list, a tuple, an object...
            self.Children = list(children)

    def AddChildren(self, children):
        self.Children.extend(list(children))

    def Walk(self,function=None):
        """
        Walk the tree from the current node, and execute "function" for each node.
        """
        function(self)
        for child in self.Children:
            child.Walk(function)



# vim: tabstop=4:shiftwidth=4:expandtab
