# -*- coding: utf-8 -*-

# © 2015-2018, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the function to serialize and deserialize pytest-score objects to JSON.
"""

import numbers
from functools import singledispatch

import numpy as np

from ._score import ScoreSheet, ScoreResult, Evaluator

SCORE_SHEET_KEY = '_score_sheet'
SCORE_RESULT_KEY = '_score_result'
EVALUATOR_KEY = '_evaluator'


@singledispatch
def encode(obj):
    """
    Serializes pytest-score objects to JSON-compatible format.
    """
    raise TypeError('cannot JSONify {} object {}'.format(type(obj), obj))


@encode.register(np.bool_)
def _(obj):
    return bool(obj)


@encode.register(numbers.Integral)
def _(obj):
    return int(obj)


@encode.register(numbers.Real)
def _(obj):
    return float(obj)


@encode.register(ScoreSheet)
def _(obj):
    return {SCORE_SHEET_KEY: obj.to_dict()}


@encode.register(ScoreResult)
def _(obj):
    return {SCORE_RESULT_KEY: obj.to_dict()}


@encode.register(Evaluator)
def _(obj):
    return {EVALUATOR_KEY: obj.to_dict()}


def _decode_score_sheet(obj):
    return ScoreSheet.from_dict(obj)


def _decode_score_result(obj):
    return ScoreResult.from_dict(obj)


def _decode_evaluator(obj):
    return Evaluator.from_dict(obj)


_DECODE_LOOKUP = {
    SCORE_SHEET_KEY: _decode_score_sheet,
    SCORE_RESULT_KEY: _decode_score_result,
    EVALUATOR_KEY: _decode_evaluator,
}


def decode(obj):
    """
    Create a pytest-score object from the JSON-compatible format.
    """
    if isinstance(obj, dict):
        for key, decode_func in _DECODE_LOOKUP.items():
            if key in obj:
                return decode_func(obj[key])
    return obj
