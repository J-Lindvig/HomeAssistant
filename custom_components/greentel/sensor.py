from .const import DOMAIN
import logging

from datetime import datetime, timedelta

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
  """Setup sensor platform"""

  async def async_update_data():
    #try:
    greentelClient = hass.data[DOMAIN]["greentelClient"]
    await hass.async_add_executor_job(greentelClient.login)
    #except Exception as e:
    #    raise UpdateFailed(f"Error communicating with server: {e}")

  coordinator = DataUpdateCoordinator(
    hass,
    _LOGGER,
    name="sensor",
    update_method=async_update_data,
    update_interval=timedelta(minutes=5)
  )

  # Immediate refresh
  await coordinator.async_request_refresh()
  
  # entities = []
  # client = hass.data[DOMAIN]["greentelClient"]
  # for i, child in enumerate(client._children):
  #   if str(child["id"]) in client._daily_overview:
  #     entities.append(AulaChildSensor(hass, coordinator, child))

  # async_add_entities(entities)