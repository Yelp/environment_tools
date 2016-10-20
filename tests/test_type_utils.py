# -*- coding: utf-8 -*-

import contextlib
import mock

from environment_tools.config import _convert_mapping_to_graph
import environment_tools.type_utils
from environment_tools.type_utils import available_location_types
from environment_tools.type_utils import convert_location_type
from environment_tools.type_utils import compare_types
from environment_tools.type_utils import get_current_location
from environment_tools.type_utils import location_graph

from types import ListType
from types import StringType

from pytest import yield_fixture


class TestTypeUtils:
    @yield_fixture
    def mock_data(self):
        fake_data = {
            'location_types.json': ['environment', 'region', 'az'],
            'location_mapping.json': {
                'prod_environment': {
                    'usnorth1-prod_region': {
                        'usnorth1aprod_az': {},
                        'usnorth1bprod_az': {},
                    },
                    'usnorth2-prod_region': {
                        'usnorth2aprod_az': {},
                        'usnorth2bprod_az': {},
                        'usnorth2cprod_az': {},
                    },
                },
                'dev_environment': {
                    'usnorth1-dev_region': {
                        'usnorth1adev_az': {},
                        'usnorth1bdev_az': {},
                    },
                },
            },
        }
        with mock.patch('environment_tools.type_utils._read_data_json',
                        side_effect=fake_data.get) as mock_fake_data:
            empty_graph = environment_tools.type_utils.GraphCache(None, None)
            environment_tools.type_utils._location_graph_cache = empty_graph
            yield mock_fake_data
            environment_tools.type_utils._location_graph_cache = empty_graph

    def test_location_graph_cache(self, mock_data):
        mock_convert = mock.Mock(spec=_convert_mapping_to_graph)
        mock_convert.return_value = 'fake_graph'
        with mock.patch(
                'environment_tools.type_utils._convert_mapping_to_graph',
                mock_convert):
            for i in range(5):
                assert location_graph() == 'fake_graph'
            assert mock_convert.call_count == 1
            assert location_graph(use_cache=False) == 'fake_graph'
            assert mock_convert.call_count == 2

    def test_available_location_types(self, mock_data):
        location_types = available_location_types()
        assert type(location_types) is ListType
        assert len(location_types) > 0

    def test_compare_types(self, mock_data):
        assert compare_types('environment', 'az') < 0
        assert compare_types('az', 'az') == 0
        assert compare_types('az', 'region') > 0

    def test_down_convert(self, mock_data):
        down_convert = convert_location_type('prod', 'environment', 'az')
        assert type(down_convert) is ListType
        assert len(down_convert) > 1
        for result in down_convert:
            assert type(result) is StringType

    def test_up_convert(self, mock_data):
        up = convert_location_type('usnorth1bprod', 'az', 'environment')
        assert up == ['prod']

        up = convert_location_type('usnorth1aprod', 'az', 'region')
        assert up == ['usnorth1-prod']

    def test_same_convert(self, mock_data):
        same = convert_location_type('usnorth2cprod', 'az', 'az')
        assert same == ['usnorth2cprod']

    def test_get_current_location(self, mock_data):
        mock_open = mock.mock_open(read_data='test   ')

        with contextlib.nested(
            mock.patch('__builtin__.open', mock_open),
        ):
            assert get_current_location('az') == 'test'
