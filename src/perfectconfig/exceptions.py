class PerfectConfigException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class PerfectConfigRuntimeException(RuntimeError):
    def __init__(self, msg):
        super().__init__(msg)

class GlobalConfigError(ValueError):
    def __init__(self, msg):
        super().__init__(msg)