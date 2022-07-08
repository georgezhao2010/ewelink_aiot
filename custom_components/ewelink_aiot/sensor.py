from .base_entities import EWeLinkEntity
from .device_config import SUPPORTED_DEVICES
from .const import DOMAIN, CLOUD
from homeassistant.const import CONF_DEVICE_ID
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    device_id = config_entry.data.get(CONF_DEVICE_ID)
    cloud = hass.data[DOMAIN][CLOUD]
    device = cloud.get_device(device_id)
    device_type = device.device_type
    _LOGGER.debug(f"Setting up entry, platform: sensor, device: {device.device_id}")
    if SUPPORTED_DEVICES.get(device_type) and SUPPORTED_DEVICES.get(device_type).get("sensor"):
        configs = SUPPORTED_DEVICES.get(device_type).get("sensor")
        sensors = []
        for config in configs:
            sensor = eval(f"{config.get('class')}(device, {config})")
            sensors.append(sensor)
        async_add_entities(sensors)
