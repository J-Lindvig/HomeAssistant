from homeassistant.const import CONF_PHONE_NO, CONF_PASSWORD

from .greentel import GreentelClient
from .const import DOMAIN

async def async_setup(hass, config):
    conf = config.get(DOMAIN)
    if conf is None:
        return True

    greentelClient  = GreentelClient(conf.get(CONF_PHONE_NO), conf.get(CONF_PASSWORD))
    hass.data[DOMAIN] = {
        "greentelClient": greentelClient
    }

    # Add sensors
    hass.async_create_task(
        hass.helpers.discovery.async_load_platform('sensor', DOMAIN, conf, config)
    )

    # Initialization was successful.
    return True