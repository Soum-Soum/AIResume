from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    environments=True,
    env_switcher="ENV_SWITCH",
    settings_files=["conf/settings.toml", "conf/.secrets.toml"],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
