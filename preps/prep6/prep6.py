"""CSC148 Prep 6: Linked Lists

=== CSC148 Winter 2024 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Sophia Huynh

=== Module Description ===
This module contains the code for a linked list implementation with two classes,
LinkedList and _Node.
"""
from __future__ import annotations
from typing import Any
from python_ta.contracts import check_contracts


@check_contracts
class _Node:
    """A node in a linked list.

    Note that this is considered a "private class", one which is only meant
    to be used in this module by the LinkedList class, but not by client code.

    Attributes:
    - item:
        The data stored in this node.
    - next:
        The next node in the list, or None if there are no more nodes.
    """
    item: Any
    next: _Node | None

    def __init__(self, item: Any) -> None:
        """Initialize a new node storing <item>, with no next node.
        """
        self.item = item
        self.next = None  # Initially pointing to nothing


@check_contracts
class LinkedList:
    """A linked list implementation of the List ADT.

    Private Attributes:
    - _first:
        The first node in the linked list, or None if the list is empty.
    """
    _first: _Node | None

    def __init__(self, items: list) -> None:
        """Initialize an empty linked list.
        """
        if not items:  # No items, and an empty list!
            self._first = None
        else:
            self._first = _Node(items[0])
            curr = self._first
            for item in items[1:]:
                curr.next = _Node(item)
                curr = curr.next

    def __str__(self) -> str:
        """Return a string representation of this list in the form
        '[item1 -> item2 -> ... -> item-n]'.

        >>> str(LinkedList([1, 2, 3]))
        '[1 -> 2 -> 3]'
        >>> str(LinkedList([]))
        '[]'
        """
        items = []
        curr = self._first
        while curr is not None:
            items.append(str(curr.item))
            curr = curr.next
        return '[' + ' -> '.join(items) + ']'

    ##########################################################################
    # Read the docstring and complete the following LinkedList method.
    #
    # You should use the provided *linked list traversal* code template
    # as your starting point, but of course you should modify it as necessary!
    ##########################################################################

    def remove_between(self, low: Any, high: Any) -> None:
        """
        Remove all nodes in this linked list that have an item
        between low and high (inclusive).

        Preconditions:
        - the nodes in self are in sorted order
          i.e. for all nodes in this LinkedList:
          node is None or node.next is None or (node.item <= node.next.item)
        - low < high

        >>> lnk = LinkedList([0, 1, 2, 2, 2, 3, 4, 5])
        >>> lnk.remove_between(1, 2)
        >>> print(lnk)
        [0 -> 3 -> 4 -> 5]
        >>> lnk = LinkedList([0, 1])
        >>> lnk.remove_between(0, 0)
        >>> print(lnk)
        [1]
        """
        while self._first and low <= self._first.item <= high:
            self._first = self._first.next

        prev = None
        current = self._first
        while current:
            if low <= current.item <= high:
                prev.next = current.next
            else:
                prev = current
            current = current.next


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        "max-line-length": 100
    })
