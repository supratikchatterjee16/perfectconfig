import os
from perfectconfig import config_store
import pytest
from tests.helpers.mocks import TestConfig

PROFILE_MAPPING = {
    "single-json": (True, "json"),
    "multi-json": (False, "json"),
    "single-yaml": (True, "yaml"),
    "multi-yaml": (False, "yaml"),
}

def pytest_addoption(parser):
    parser.addoption(
        "--profile",
        action="store",
        choices=PROFILE_MAPPING.keys(),
        required=False,
        help="Execution profile",
    )

def pytest_generate_tests(metafunc):
    if "profile" not in metafunc.fixturenames:
        return

    selected = metafunc.config.getoption("--profile")
    profiles = [selected] if selected else list(PROFILE_MAPPING)

    metafunc.parametrize("profile", profiles, scope="class")

@pytest.fixture(scope="class")
def profile_data(request, profile):
    is_single, type_name = PROFILE_MAPPING[profile]
    request.cls.is_single = is_single
    request.cls.type_name = type_name
    return (is_single, type_name)

@pytest.fixture(scope="function", autouse=True)
def setup_per_test(profile_data):
    config_store.initialize('conceivilize', 'perfectconfig-test', single_file=profile_data[0], format=profile_data[1])
    test_config :TestConfig = config_store['test-config']
    test_config.val = "value"
    yield


@pytest.fixture(scope="class", autouse=True)
def class_setup_teardown(profile_data):
    # setUpClass
    os.environ['PERFECTCONFIG_PROFILE'] = 'perfectconfig-test'
    yield

    # tearDownClass
    config_store.remove()
    del os.environ['PERFECTCONFIG_PROFILE']
