# -*- coding: utf-8 -*-
"""
Defines the fixtures for running a scored evaluation.
"""

import json
from contextlib import contextmanager

import pytest
from fsc.export import export

from ._score import ScoreSheet
from ._serialize import encode, decode


@export
@pytest.fixture(scope='session')
def score_sheet(request):
    """
    Creates the score sheets and saves it after the test session.
    """
    with _store_score(save_file=_get_save_file(request)
                      ) as score_sheet_instance:
        request.session._score_sheet_instance = score_sheet_instance  # pylint: disable=protected-access
        score_sheet_instance.rotate()
        yield score_sheet_instance


@contextmanager
def _store_score(save_file):
    """
    Initializes the ScoreSheet instance on entering and saves it on exiting.
    """
    try:
        with open(save_file, 'r') as in_file:
            score_sheet_instance = json.load(in_file, object_hook=decode)
    except (IOError, json.decoder.JSONDecodeError):
        score_sheet_instance = ScoreSheet()
    if not isinstance(score_sheet_instance, ScoreSheet):
        score_sheet_instance = ScoreSheet()

    yield score_sheet_instance

    with open(save_file, 'w') as out_file:
        json.dump(score_sheet_instance, out_file, default=encode)


def _get_save_file(request):
    """
    Returns the path where the score file is stored.
    """
    return request.config.rootdir.join('.pytest-score')


@export
@pytest.fixture
def score(request, score_sheet):  # pylint: disable=redefined-outer-name
    """
    Fixture to store a scored test.
    """

    def inner(value, cutoff=None, tag=''):  # pylint: disable=missing-docstring
        score_sheet.add_score(
            value, test_name=_get_test_name(request), tag=tag
        )
        if cutoff is not None:
            assert value >= cutoff

    return inner


def _get_test_name(request):
    """
    Returns a unique identifier for a given test.
    """
    return request.module.__name__ + '/' + request._parent_request._pyfuncitem.name  # pylint: disable=protected-access