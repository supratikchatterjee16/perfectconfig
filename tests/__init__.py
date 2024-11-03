import unittest
from .test_store import StoreTestCases

def suite():
    suite = unittest.TestSuite()
    suite.addTest(StoreTestCases('test_single_config_creation'))
    suite.addTest(StoreTestCases('test_config_persistance'))
    # suite.addTest(StoreTestCases('test_cleanup'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())