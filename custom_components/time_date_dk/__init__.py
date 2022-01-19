"""Example Load Platform integration."""
from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER: logging.Logger = logging.getLogger(__package__)
_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:

  # Add sensors
	hass.async_create_task(
		hass.helpers.discovery.async_load_platform('sensor', DOMAIN, {}, config)
	)

	# Initialization was successful.
	return True
