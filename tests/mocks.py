from perfectconfig import GlobalConfig, ConfigProperty, password, config_store

class TestConfig(GlobalConfig):
    _name='test-config'
    val = ConfigProperty(str, 'value', prompt="Enter a value")
    name = ConfigProperty(str, 'name', prompt="Enter a name")
    password = ConfigProperty(password, 'passkey', prompt="Enter a password")
    some_default = ConfigProperty(str, 'default', default="some_default")

class SecondTestConfig(GlobalConfig):
    _name = 'second-config'
    val = ConfigProperty(str, 'value', default="Enter a value")
    some_default = ConfigProperty(str, 'default', default="some_default")

config_store.track()

