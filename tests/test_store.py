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
        # self.assertTrue(os.path.exists(config_path))
        files = []
        for path in config_path.iterdir():
            files.append(path)
        
        # Test if only one config file is created
        # self.assertEqual(len(files), 1 if self.is_single else 2)
        assert len(files) == (1 if self.is_single else 2)

        test_config :TestConfig = config_store['test-config']

        # Test if test_config is not None
        # self.assertIsNotNone(test_config)
        assert test_config is not None

        # self.assertTrue(issubclass(test_config.__class__, GlobalConfig))
        assert issubclass(test_config.__class__, GlobalConfig)

        # self.assertEqual(test_config.some_default, "some_default")
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

        # self.assertNotEqual(reloaded_config.val, original_value)
        # self.assertEqual(reloaded_config.val, new_value)
        assert reloaded_config.val != original_value
        assert reloaded_config.val == new_value

    def test_for_multiple_configs(self):
        from .helpers.mocks import SecondTestConfig
        second_config :SecondTestConfig = config_store['second-config']
        # self.assertIsNotNone(second_config)
        # self.assertTrue(issubclass(second_config.__class__, GlobalConfig))
        # self.assertEqual(second_config.some_default, "some_default")
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
        # self.assertEqual(config_dict, expected_dict)
        assert config_dict == expected_dict
