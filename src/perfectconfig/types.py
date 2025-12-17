import inspect

class ConfigProperty:
    def __init__(
        self, datatype, name: str = None, default: any = None, prompt: str = None
    ):
        self.datatype = datatype
        self.name = name
        self.prompt = prompt
        self._val = default
    
    def __set__(self, instance, value):
        if not isinstance(value, self.datatype):
            raise TypeError(f"Expected {self.datatype} but received {type(value)}.")
        self._val = value

    def __get__(self, instance, objtype=None):
        return self._val

    def __eq__(self, other):
        if other is self.datatype:
            raise TypeError("Expected {}, received {}.".format(self.datatype, type(other)))
        return (self._val == other)


class GlobalConfig:
    __instance = None
    _name = "GlobalConfig"

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cls.__instance._initialized = False
        return cls.__instance

    def get_all(self) -> dict:
        config = {}
        for key in self.__dict__.keys():
            if isinstance(key, ConfigProperty):
                config[key.name] = self.__dict__[key]
        raise RuntimeError("Must be overridden.")

    def to_dict(self) -> dict:
        data = {}
        for name, value in self.__class__.__dict__.items():
            for obj_name, obj_value in inspect.getmembers(self):
                if obj_name == name and isinstance(value, ConfigProperty):
                    config_name = value.__dict__['name'] if value.__dict__['name'] is not None else obj_name
                    data[config_name] = obj_value
        return data

    def from_dict(self, buffer: dict):
        for name, value in self.__class__.__dict__.items():
            for obj_name, obj_value in inspect.getmembers(self):
                if obj_name == name and isinstance(value, ConfigProperty):
                    config_name = value.__dict__['name'] if value.__dict__['name'] is not None else obj_name
                    if hasattr(self, obj_name):
                        setattr(self, obj_name, buffer[config_name])

