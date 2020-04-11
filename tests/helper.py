from contextlib import contextmanager
from django.test import TestCase
from expects import *

from classic_tetris_project.models import *
from classic_tetris_project.util.memo import memoize
from .factories import *



@contextmanager
def describe(description):
    """
    noop, just used to provide structure to test classes
    """
    yield
