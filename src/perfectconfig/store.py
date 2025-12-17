import inspect
import os
import appdirs
import json
import yaml

from pathlib import Path
from typing import Optional
import logging

from .types import GlobalConfig, ConfigProperty
from .exceptions import GlobalConfigError, PerfectConfigRuntimeException

logger = logging.getLogger('perfect-config')
class ConfigStore(dict):
    _config_loc: Optional[Path] = None
    _single_file: bool = True
    _format: str = "json"
    _buffer: dict = {}

    def _save(self, key=None):
        dump, name_template = (json.dump, "{}.json") if self._format == "json" else (yaml.safe_dump, "{}.yml")

        if self._single_file:
            with open(
                os.path.join(self._config_loc, name_template.format("config")), "w"
            ) as config_file:
                dump(self._buffer, config_file)
        else:
            if key is not None:
                with open(
                    os.path.join(self._config_loc, name_template.format(key)), "w"
                ) as config_file:
                    dump(self._buffer[key], config_file)
            else:
                for entry in self._buffer.keys():
                    with open(
                        os.path.join(self._config_loc, name_template.format(entry)), "w"
                    ) as config_file:
                        dump(self._buffer[entry], config_file)
        self._buffer.clear()
    
    def _load(self, config: Optional[GlobalConfig] = None):
        load, name_template = (json.loads, "{}.json") if self._format == "json" else (yaml.safe_load, "{}.yml")

        if self._single_file:
            with open(
                os.path.join(self._config_loc, name_template.format("config")), "r"
            ) as config_file:
                self._buffer = load(os.path.expandvars(config_file.read()))
        else:
            if config is None:
                for key in self.keys():
                    with open(
                        os.path.join(self._config_loc, name_template.format(key)), "r"
                    ) as config_file:
                        self._buffer[key] = load(os.path.expandvars(config_file.read()))
            else:
                with open(
                    os.path.join(self._config_loc, name_template.format(config._name)),
                    "r",
                ) as config_file:
                    self._buffer.update(load(os.path.expandvars(config_file.read())))
    
    def save(self, config: GlobalConfig):
        self._load(config)

        self._buffer[config._name] = config.to_dict()

        self._save(config._name)
    
    def _save_unchecked(self):
        if self._format in ["json", "yaml"]:
                self._save()
        else:
            raise PerfectConfigRuntimeException("Unsupported file format")

    def track(self):
        # Pre-intialization, and post initialization value injection
        current_module = inspect.getmodule(inspect.stack()[1][0])
        for name, obj in inspect.getmembers(current_module, inspect.isclass):
            if issubclass(obj, GlobalConfig) and obj is not GlobalConfig:
                logging.info("Loading configuration for " + name)
                self[obj._name] = obj()
                if self._config_loc is not None:
                    self._from_file(obj)

    def _prompt(self, member) -> str:
        return input("{}: ".format(member.prompt))

    def _load_members(self, cls) -> dict:
        defaults = {}
        current_cls = self[cls].__class__
        for name, value in current_cls.__dict__.items():
            for obj_name, obj_value in inspect.getmembers(self[cls]):
                if name == obj_name and isinstance(value, ConfigProperty):
                    config_name = value.__dict__['name'] if value.__dict__['name'] else obj_name
                    if value.__dict__['prompt']:
                        defaults[config_name] = self._prompt(value)
                    elif value.__dict__['_val'] is not None:
                        defaults[config_name] = value._val
                    else:
                        raise GlobalConfigError(f'No default value or prompt specified, for creating initial configurations for {current_cls.__name__}.{obj_name}')
        return defaults

    def _load_defaults(self, obj: Optional[GlobalConfig]=None):
        if obj is None:
            for prop_class in self.keys():
                prop_class_defaults = self._load_members(prop_class)
                self._buffer[self[prop_class]._name] = prop_class_defaults
        else:
            obj_defaults = self._load_members(obj)
            self._buffer[obj._name] = obj_defaults
            

    def _from_file(self, config: Optional[GlobalConfig] = None):
        try:
            self._load(config)
        except FileNotFoundError:
            logging.error("Configurations could not be loaded. Was it deleted/relocated perhaps?")
            raise PerfectConfigRuntimeException("Configurations not found")
        if config is not None:
            try:
                self[config._name].from_dict(self._buffer)
            except TypeError as e:
                raise PerfectConfigRuntimeException(str(e) + f' Reading configuration \"{config._name}\".')
        else:
            try:
                for key in self.keys():
                    self[key].from_dict(self._buffer[key])
            except TypeError as e:
                raise PerfectConfigRuntimeException(str(e) + f' Reading configuration \"{key}\".')
               
        self._buffer.clear()

    def initialize(self, org, product, format="json", single_file=True, user=True):
        """Configure the config store. This checks if config file is present and"""
        self._single_file = single_file
        self._format = format
        if user:
            self._config_loc = Path(appdirs.user_config_dir(product, org))
        else:
            self._config_loc = Path(appdirs.site_config_dir(product, org))
        if not os.path.exists(self._config_loc.absolute()):
            try:
                os.makedirs(self._config_loc.absolute())
                logger.info("Created configurations location: " + str(self._config_loc.absolute()))
            except OSError:
                logger.warning("The folders already exist.")
            self._load_defaults()
            self._save_unchecked()
        else:
            logger.info("Loading configurations at: " + str(self._config_loc.absolute()))
            self._from_file()

    def remove(self):
        """A managed function to remove all related configuration files and configurations from the object."""
        if self._config_loc is not None and os.path.exists(self._config_loc):
            for path in self._config_loc.iterdir():
                os.remove(path)
            os.rmdir(self._config_loc)
        # self.clear()


config_store: ConfigStore = ConfigStore()
