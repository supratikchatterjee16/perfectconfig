import os
import copy
import appdirs
import pytest

from pathlib import Path
from perfectconfig import config_store, GlobalConfig
from .helpers.mocks import TestConfig

@pytest.mark.usefixtures("profile_data")
class TestStore:
    # def setUp(self):
    #     self.is_single = self.__class__.is_single
    #     self.type_name = self.__class__.type_name
    #     config_store.initialize('conceivilize', 'perfectconfig-test', single_file=self.is_single, format=self.type_name)
    
    # @classmethod
    # def tearDownClass(self):
    #     config_store.remove()
        # pass
    
    def test_config_creation(self):
        config_path = Path(appdirs.user_config_dir('perfectconfig-test', 'conceivilize'))

        assert os.path.exists(config_path)
        files = []
        for path in config_path.iterdir():
            files.append(path)
        
        # Test if only one config file is created
        assert len(files) == (1 if self.is_single else 2)

        test_config :TestConfig = config_store['test-config']

        # Test if test_config is not None
        assert test_config is not None

        assert issubclass(test_config.__class__, GlobalConfig)

        assert test_config.some_default == "some_default"
    
    def test_config_modification_persistence(self):
        test_config :TestConfig = config_store['test-config']
        original_value = copy.deepcopy(test_config.val)
        new_value = "new_value"
        test_config.val = new_value
        config_store.save(test_config)
        # Reload the config store to ensure persistence
        config_store.initialize('conceivilize', 'perfectconfig-test', single_file=self.is_single, format=self.type_name)
        reloaded_config :TestConfig = config_store['test-config']
        assert reloaded_config.val != original_value
        assert reloaded_config.val == new_value

    def test_for_multiple_configs(self):
        from .helpers.mocks import SecondTestConfig
        second_config :SecondTestConfig = config_store['second-config']
        assert second_config is not None
        assert issubclass(second_config.__class__, GlobalConfig)
        assert second_config.some_default == "some_default"
    
    def test_to_dict_method(self):
        test_config :TestConfig = config_store['test-config']
        config_dict = test_config.to_dict()
        expected_dict = {
            'value': test_config.val,
            'name': test_config.name,
            'default': test_config.some_default
        }
        assert config_dict == expected_dict

    def test_env_variable_expansion(self):
        from .helpers.mocks import SecondTestConfig
        second_config :SecondTestConfig = config_store['second-config']
        expected_value = os.getenv('PERFECTCONFIG_PROFILE', '')
        assert expected_value is not None
        assert expected_value != ''
        assert second_config.env == expected_value