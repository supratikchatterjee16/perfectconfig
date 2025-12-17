from perfectconfig import GlobalConfig, ConfigProperty, config_store

class TestConfig(GlobalConfig):
    _name='test-config'
    __test__ = False
    val = ConfigProperty(str, 'value', default="value")
    name = ConfigProperty(str, 'name', default="name")
    some_default = ConfigProperty(str, 'default', default="some_default")

class SecondTestConfig(GlobalConfig):
    _name = 'second-config'
    __test__ = False
    val = ConfigProperty(str, 'value', default="value")
    some_default = ConfigProperty(str, 'default', default="some_default")

config_store.track()

