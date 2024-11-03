# Perfect Config

Manage your configuations in a mechanism similar to `SQLAlchemy`.

## Usage

Install using `pip install perfectconfig`.

Define your configuration classes :

```python
from perfectconfig import GlobalConfig, ConfigProperty, config_store

class SampleServerConfiguration(GlobalConfig):
    _name = "server_config"
    port = ConfigProperty("port", default=8080)
    host = ConfigProperty("host", default="localhost")
    name = ConfigProperty("name", default="sample_server")

config_store.track() # Tracks the configuration defined in the file
```

Initialize your store(once initialized this is accessible everywhere):

```python
from perfectconfig import config_store
config_store.initialize("my-org", "my-product", format="yaml", single_file=False)
```

`format` can be `json` or `yaml`. Default is `json`.

`single_file` allows you to control, whether all individual configurations will be stored as separate files, or if they'd be maintained in the same file. In some cases format errors in the configuration file might impact the whole file, so you may want to separate it out. By default, it is set to `True`.

`config_store.initialize` can be called anywhere, but it is recommended to have it at the entrance point of the program.

Use anywhere:

```python
from perfectconfig import config_store

# Use it
server_config = config_store["server_config"]
print(server_config.port)

# Modify it
server_config.port = 9090
config_store.save(server_config)
```

What about deletions?

This library does not provide a mechanism to delete configurations, or rename them on specific environments. Kindly ensure that when deployed everything is as-intended.

What we do provide is a clean-up mechanism:

```python
from perfectconfig import config_store
config_store.initialize("my-org", "my-product", type="yaml")
config_store.purge()
```

This is expected to help you manage your configurations, but in a human readable way, so offers no encryption options, at the moment.

There are no in-built mutex, or resource locking implemented, this is to provide flexibility to the implementor.

## Active and Lazy loading

The program is prepared to perform active and lazy loading as required. The developer need not bother about it, and work on the main logic itself. Just by following the aforementioned steps, the configuration store will automatically manage the loading.

Active loading is when the property definitions and values are required at the start of the program. When the file containing the property definitions are imported, it automatically triggers the `track` function, to add load the definitions and then load the values using initialize.

Lazy loading is when the property definitions are loaded at a later time. This works by holding the values on a buffer, and assigning the values to the defintions, when they're required to be used.

Everything happens under the hood without the explicit intervention of the user.

## Under the hood

Uses the in-built `json` library, and `pyyaml` and `appdirs` to provide the functionality in a structured way.

This is inspired from the property loading mechanism in `Spring Boot`, with the mechanism used in `SQLAlchemy`.

## Warnings

If the configurations objects are changed(such as during development), the objects aren't automanaged yet. This will require a manual removal or updation of the configurations for them to operate as expected.

## Planned

```python
from perfectconfig import config_store
config_store.load(yourpackage.env_configs.prod)
config_store.load(yourpackage.env_configs.dev)
...
```