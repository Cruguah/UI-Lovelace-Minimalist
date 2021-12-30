import logging

from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.core import Config
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.components import frontend

from custom_components.lovelace_minimalist_ui.enums import ConfigurationType

from .base import LmuBase
from .const import DOMAIN, NAME, STARTUP_MESSAGE
from .load_dashboard import load_dashboard
from .load_plugins import load_plugins
from .process_yaml import process_yaml

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_initialize_integration(
    hass: HomeAssistant,
    *,
    config_entry: ConfigEntry | None = None,
    config: dict[str, Any] | None = None,
) -> bool:
    """Initialize the integration"""
    hass.data[DOMAIN] = lmu = LmuBase()

    if config is not None:
        if DOMAIN not in config:
            return True
        if lmu.configuration.config_type == ConfigurationType.CONFIG_ENTRY:
            return True
        lmu.configuration.update_from_dict(
            {
                "config_type": ConfigurationType.YAML,
                **config[DOMAIN],
                "config": config[DOMAIN],
            }
        )

    if config_entry is not None:
        if config_entry.source == SOURCE_IMPORT:
            # not sure about this one
            hass.async_create_task(hass.config_entries.async_remove(config_entry.entyr_id))
            return False

        lmu.configuration.update_from_dict(
            {
                "config_entry": config_entry,
                "config_type": ConfigurationType.CONFIG_ENTRY,
                **config_entry.data,
                **config_entry.options,
            }
        )

    _LOGGER.debug("Configuration type: %s", lmu.configuration.config_type)
    return True
    # Process  yaml
    # Load plugins
    # Load dashboards




async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using UI."""
    return await async_initialize_integration(hass=hass, config=config)

    # load_plugins(hass, DOMAIN)

    # return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""

    config_entry.add_update_listener(async_reload_entry)
    return await async_initialize_integration(hass=hass, config_entry=config_entry)



    # if not DOMAIN in hass.data:
    #     hass.data[DOMAIN] = {}

    # _LOGGER.debug(config_entry.options)
    # if config_entry.options:
    #     data = config_entry.options.copy()
    # else:
    #     if DOMAIN in hass.data:
    #         data = hass.data[DOMAIN]
    #     else:
    #         data = {}
    #         await hass.config_entries.async_remove(config_entry.entry_id)

    # _LOGGER.debug(hass.data[DOMAIN])

    # process_yaml(hass, config_entry)

    # load_dashboard(hass, config_entry)

    # config_entry.add_update_listener(_update_listener)

    # return True

async def async_remove_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Remove Integration"""
    _LOGGER.debug("{} is now uninstalled".format(NAME))

    #TODO cleanup:
    #  - themes
    #  - blueprints
    frontend.async_remove_panel(hass, "lovelace-minimalist-ui")

async def async_reload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    _LOGGER.debug('Reload the config entry')

    await async_setup_entry(hass, config_entry)

    # process_yaml(hass, config_entry)

    # hass.bus.async_fire("lovelace_minimalist_ui_reload")

    # #register_modules(hass, config_entry.options)
    # #load_dashboard(hass, config_entry)

    # return True