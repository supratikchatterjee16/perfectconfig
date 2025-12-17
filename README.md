# Perfect Config

Manage your deployment configuations in a mechanism similar to [SQLAlchemy](https://www.sqlalchemy.org/).

What does it provide?

- Single globally available configuration, via the `config_store`
- Automatic JSON and YAML config files, with options to create atomic, or a unified configuration file.
- Dictionary access to configurations
- Prompting users during initial setup of application.
- Active and Lazy loading of configurations
- Removes biolerplate codes for configuration management
- Usage of system agnostic logging locations

## Usage

Install using `pip install perfectconfig`.

Define your configuration classes :

```python
from perfectconfig import GlobalConfig, ConfigProperty, config_store

class SampleServerConfiguration(GlobalConfig):
    _name = "server_config"
    port = ConfigProperty(int, "port", default=8080)
    host = ConfigProperty(str, "host", default="localhost")
    name = ConfigProperty(str, "name", default="sample_server")

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
config_store.remove()
```

This is expected to help you manage your configurations, but in a human readable way, so offers no encryption options, at the moment.

There are no in-built mutex, or resource locking implemented, this is to provide flexibility to the implementor.

## Active and Lazy loading

The program is prepared to perform active and lazy loading as required. The developer need not bother about it, and work on the main logic itself. Just by following the aforementioned steps, the configuration store will automatically manage the loading.

Active loading is when the property definitions and values are required at the start of the program. When the file containing the property definitions are imported, it automatically triggers the `track` function, to add load the definitions and then load the values using initialize.

Lazy loading is when the property definitions are loaded at a later time. This works by holding the values on a buffer, and assigning the values to the defintions, when they're required to be used.

Everything happens under the hood without the explicit intervention of the user.

## Under the hood

Uses the in-built `json` library, and `pyyaml` and `appdirs`.

This is inspired from the property loading mechanism in `Spring Boot`, with the mechanism used in `SQLAlchemy`.

## Warnings

If the configurations objects are changed(such as during development), the objects aren't auto-managed yet. This will require a manual removal or updation of the configurations for them to operate as expected.

## Planned

Configurations segregation for automatic configuration on environments.

```python
from perfectconfig import config_store
config_store.load(yourpackage.env_configs.prod)
config_store.load(yourpackage.env_configs.dev)
...
```

Prompt prevention for automated deployments(prompts during initial setup may be undesirable, for remote nodes being deployed to via a CI/CD pipeline).

```python
from perfectconfig import config_store
config_store.initialize(org_name, app_name, prompt=False)
```

Automatic detection and backup, on config schema changes, with proper porting of existing configurations, allowing for backups for reverting deployments.

Creating a debug mode, that updates the application configuration from defaults every time(with options to prevent debug mode inside the configuration defintion: i.e. `GlobalConfig._no_debug : bool` and `config_store.initialize(org, product, format="json", single_file=True, user=True, debug=False)`).

Recreation of deleted configuration files from defaults/prompts.