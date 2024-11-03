import os
import appdirs
import unittest
from pathlib import Path
from perfectconfig import config_store, GlobalConfig, ConfigProperty
from .mocks import TestConfig

class StoreTestCases(unittest.TestCase):
    def test_single_config_creation(self):
        config_store.initialize('conceivilize', 'perfectconfig-test')
        config_path = Path(appdirs.user_config_dir('perfectconfig-test', 'conceivilize'))
        self.assertTrue(os.path.exists(config_path))
        files = []
        for path in config_path.iterdir():
            files.append(path)
        self.assertEqual(len(files), 1)

        test_config :TestConfig = config_store['test-config']

        # Assert test_config is subclass of GlobalConfig, 
        # some_default is instance of ConfigProperty,
        # and value is set
        self.assertTrue(issubclass(test_config, GlobalConfig))
        self.assertIsInstance(test_config.some_default, ConfigProperty)
        self.assertEqual(test_config.some_default, "some_default")
    
    def test_config_persistance(self):
        config_store.initialize('conceivilize', 'perfectconfig-test')
        test_config = config_store['test-config']
        self.assertIsInstance(test_config.some_default, ConfigProperty)
        self.assertEqual(test_config.some_default, "some_default")
    