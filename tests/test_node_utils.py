# -*- coding: utf-8 -*-
import mock
import pytest

from environment_tools import node_utils
from environment_tools import type_utils


@pytest.yield_fixture
def mock_data():
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
    with mock.patch(
        'environment_tools.type_utils._read_data_json',
        side_effect=fake_data.get
    ) as mock_fake_data:
        empty_graph = type_utils.GraphCache(None, None)
        type_utils._location_graph_cache = empty_graph
        yield mock_fake_data
        type_utils._location_graph_cache = empty_graph


def test_get_node_location():
    node_hostname = 'my-hostname-usnorth1'
    assert node_utils.get_node_location(node_hostname) == 'usnorth1'


def test_get_node_location_none():
    node_hostname = 'notahostname'
    assert node_utils.get_node_location(node_hostname) is None


def test_get_node_location_type_az(mock_data):
    node_location = 'usnorth1adev'
    assert node_utils.get_node_location_type(node_location) == 'az'


def test_get_node_location_type_region(mock_data):
    node_location = 'usnorth2-prod'
    assert node_utils.get_node_location_type(node_location) == 'region'


def test_get_node_location_type_invalid(mock_data):
    node_location = 'nananana'
    with pytest.raises(ValueError):
        node_utils.get_node_location_type(node_location)


def test_node_location_inequaliy_az(mock_data):
    node_1 = 'usnorth2aprod'
    node_2 = 'usnorth2bprod'
    assert node_utils.node_location_equality(node_1, node_2, 'az') is False


def test_node_location_equaliy_region(mock_data):
    node_1 = 'usnorth2aprod'
    node_2 = 'usnorth2bprod'
    assert node_utils.node_location_equality(node_1, node_2, 'region') is True


def test_node_location_inequaliy_region(mock_data):
    node_1 = 'usnorth1aprod'
    node_2 = 'usnorth2bprod'
    assert node_utils.node_location_equality(node_1, node_2, 'region') is False
