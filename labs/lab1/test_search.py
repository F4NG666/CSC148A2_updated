"""CSC148 Lab 1: Introduction to CSC148!

=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module illustrates a simple unit test for our binary_search function.
"""
from search import binary_search

from search import binary_search
def test_search() -> None:
    """Simple test for binary_search."""
    assert binary_search([0, 5, 10, 15, 20, 25, 30, 35, 40], 5) == True


def test_search_first_item() -> None:
    """Test that binary_search finds an item at the first index."""
    assert binary_search([10, 20, 30, 40, 50], 10) == 0

def test_search_single_item_list_found() -> None:
    """Test binary_search on a single-item list where the item is present."""
    assert binary_search([5], 5) == 0

def test_search_single_item_list_not_found() -> None:
    """Test binary_search on a single-item list where the item is not present."""
    assert binary_search([3], 5) == -1

def test_search_item_not_at_start_or_end() -> None:
    """Test binary_search for an item not at the start or end of the list."""
    assert binary_search([2, 4, 6, 8], 6) == 2

def test_search_middle_item() -> None:
    """Test binary_search for an item in the exact middle of the list."""
    assert binary_search([1, 3, 5, 7, 9], 5) == 2

def test_search_last_item() -> None:
    """Test binary_search for an item at the last index."""
    assert binary_search([1, 3, 5, 7], 7) == 3

def test_search_not_first_last_mid() -> None:
    """Test binary_search for an item not at the start, end, or middle."""
    assert binary_search([10, 20, 30, 40, 50, 60], 40) == 3

def test_search_near_middle() -> None:
    """Test binary_search for an item near the middle of the list."""
    assert binary_search([10, 20, 30, 40, 50, 60, 70, 80], 40) == 3

def test_search_second_half() -> None:
    """Test binary_search for an item in the second half of the list."""
    assert binary_search([10, 20, 30, 40, 50, 60], 60) == 5

def test_search_first_half() -> None:
    """Test binary_search for an item in the first half of the list."""
    assert binary_search([10, 20, 30, 40, 50, 60], 20) == 1

def test_search_empty_list() -> None:
    """Test binary_search on an empty list."""
    assert binary_search([], 5) == -1

if __name__ == '__main__':
    import pytest
    pytest.main(['test_search.py'])


if __name__ == '__main__':
    import pytest
    pytest.main(['test_search.py'])
