import logging

from .api import greentelClient
from .const import (
    DOMAIN,
    CONF_CLIENT,
    CONF_PASSWORD,
    CONF_PHONENUMBER,
    CONF_PLATFORM,
    CONF_SEPARATE_DATA_SENSORS,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)
_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    conf = config.get(DOMAIN)
    if conf is None:
        return True

    # Initialize the Client
    client  = greentelClient(conf.get(CONF_PHONENUMBER), conf.get(CONF_PASSWORD))
    hass.data[DOMAIN] = {
        CONF_CLIENT: client,
        CONF_SEPARATE_DATA_SENSORS: conf.get(CONF_SEPARATE_DATA_SENSORS)
    }

    # Add sensors
    hass.async_create_task(
        hass.helpers.discovery.async_load_platform(CONF_PLATFORM, DOMAIN, conf, config)
    )

    # Initialization was successful.
    return True