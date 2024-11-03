import inspect


class password(str):
    def __new__(cls, content):
        return super().__new__(cls, content)


class ConfigProperty:
    def __init__(
        self, datatype, name: str = None, default: any = None, prompt: str = None
    ):
        self.datatype = datatype
        self.name = name
        self.prompt = prompt
        if datatype != password:
            self._val = default
        else:
            self._val = password(default)
    
    def __set__(self, instance, value):
        if not isinstance(value, self.datatype):
            raise TypeError(f"Expected {self.datatype} but received {type(value)}")
        instance._val = value

    def __get__(self, instance, objtype=None):
        if instance is None:
            return self
        return instance._val

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
        for name, member in inspect.getmembers(self):
            if (
                not inspect.ismethod(member)
                and not inspect.isfunction(member)
                and isinstance(member, ConfigProperty)
            ):
                if member.name is None:
                    data[name] = member
                else:
                    data[member.name] = member
        return data

    def from_dict(self, buffer: dict):
        for name, member in inspect.getmembers(self):
            if (
                not inspect.ismethod(member)
                and not inspect.isfunction(member)
                and isinstance(member, ConfigProperty)
            ):
                if member.name is None:
                    member = buffer[name]
                else:
                    member = buffer[member.name]
