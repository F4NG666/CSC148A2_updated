"""CSC148 Prep 2: Object Oriented Programming

=== CSC148 Winter 2024 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: David Liu, Diane Horton, and Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 David Liu, Diane Horton, and Sophia Huynh

=== Module Description ===
This module contains sample tests for Prep 2.
Complete the TODO in this file.
There is also a task inside prep2.py.
Make sure to look at that file and complete the TODO there as well.

We suggest you also add your own tests to practice writing tests and
to be confident your code is correct.

When writing a test case, make sure you create a new function, with its
name starting with "test_". For example:

def test_my_test_case():
    # Your test here

All test cases must have different names (i.e. you cannot have two tests
named test_my_test_case).

NOTE: We will not be checking this file with PythonTA. So even though you
will submit both this file and prep2.py, only prep2.py will be checked
with PythonTA for grading purposes.
"""
from hypothesis import given
from hypothesis.strategies import integers
from datetime import date
from prep2 import Spinner
from prep2_coverage_example import coverage_example


################################################################################
# Part 3
# In this part, you will be writing tests such that you have full coverage of
# prep2_coverage_example.py
################################################################################
def test_coverage_provided():
    """Call coverage_example() on a single example.

    This call covers one branch of coverage_function
    """
    assert coverage_example(0) is True

def test_spinner_spin_overflow() -> None:
    """Test spinning the spinner by a number greater than the number of slots."""
    spinner = Spinner(5)
    spinner.spin(7)
    assert spinner.position == 2  # Assuming the spinner wraps around

# TODO: You should write additional tests and/or calls to coverage_example()
#       such that you have 100% coverage of prep2_coverage_example.py
#       To see the coverage you have, run prep2_coverage_example.py
#       See the comments in that file for more details.

# TODO: If you do not have coverage installed, please follow the instructions
#       on the following Quercus page to install it:
#       https://q.utoronto.ca/courses/336881/pages/installing-packages

################################################################################
# Sample test cases below
#
# Use the below test cases as an example for writing your own test cases,
# and as a start to testing your prep2.py code.
#
# The self-test on MarkUs runs the tests below, along with a few others.
# Make sure you run the self-test after submitting your code!
#
# WARNING: THIS IS CURRENTLY AN EXTREMELY INCOMPLETE SET OF TESTS!
# We will test your code on a much more thorough set of tests!
# We encourage you to add your own test cases to this file.
################################################################################
def test_doctest() -> None:
    """Test the given doctest in the Spinner class docstring."""
    spinner = Spinner(8)

    spinner.spin(4)
    assert spinner.position == 4

    spinner.spin(2)
    assert spinner.position == 6

    spinner.spin(2)
    assert spinner.position == 0

def test_spin_over_slots() -> None:
    """Test spinning over the number of slots."""
    spinner = Spinner(10)
    spinner.spin(15)
    assert spinner.position == 5


# This is a hypothesis test; it generates a random integer to use as input,
# so that we don't need to hard-code a specific number of slots in the test.
# For more information on hypothesis (one of the testing libraries we're using),
# please see
# https://www.teach.cs.toronto.edu/~csc148h/winter/notes/testing/hypothesis.html
@given(slots=integers(min_value=1))
def test_new_spinner_position(slots: int) -> None:
    """Test that the position of a new spinner is always 0."""
    spinner = Spinner(slots)
    assert spinner.position == 0


def test_unlike_doctest() -> None:
    """Test the given doctest in the unlike method of Tweet."""
    from prep2 import Tweet
    tweet = Tweet('Sophia', date(2021, 1, 1), 'Happy new year!')
    tweet.like(5)
    assert tweet.likes == 5
    tweet.unlike()
    assert tweet.likes == 4


if __name__ == '__main__':
    import pytest

    pytest.main(['prep2_starter_tests.py'])
