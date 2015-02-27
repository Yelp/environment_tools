# -*- coding: utf-8 -*-

import mock

from environment_tools.type_utils import available_location_types
from environment_tools.type_utils import convert_location_type
from environment_tools.type_utils import get_current_location

from types import ListType
from types import StringType


def test_available_location_types():
    location_types = available_location_types()
    assert type(location_types) is ListType
    assert len(location_types) > 0


def test_convert_location_type():
    down_convert = convert_location_type('prod', 'habitat')
    assert type(down_convert) is ListType
    for result in down_convert:
        assert type(result) is StringType


def test_get_current_location():
    mock_open = mock.mock_open(read_data='test   ')

    with mock.patch('__builtin__.open', mock_open):
        assert get_current_location('habitat') == 'test'
