from .const import DOMAIN, CLOUD, DEVICE, CONF_SERVER, CONF_DEVICE_TYPE
from .device_config import SUPPORTED_DEVICES
from .ewelinkcloud import EWeLinkCloud
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, CONF_TYPE, CONF_DEVICE_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.event import async_track_point_in_utc_time
from datetime import timedelta
import homeassistant.util.dt as dt_util
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry):
    config = config_entry.data
    server = config.get(CONF_SERVER)
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    conf_type = config.get(CONF_TYPE)
    device_id = config.get(CONF_DEVICE_ID)

    async def async_setup_entities(now):
        exist_cloud = None
        if DOMAIN in hass.data:
            exist_cloud = hass.data.get(DOMAIN).get(CLOUD)
        if exist_cloud:
            device = exist_cloud.get_device(device_id)
            device_type = device.device_type
            if SUPPORTED_DEVICES.get(device_type):
                for platform in SUPPORTED_DEVICES.get(device_type).keys():
                    hass.async_create_task(hass.config_entries.async_forward_entry_setup(
                        config_entry, platform))
            return
        else:
            _LOGGER.debug(f"Cloud is not prepared, retry after 10 seconds")
        async_track_point_in_utc_time(hass, async_setup_entities, dt_util.utcnow() + timedelta(seconds=10))

    if conf_type == CLOUD:
        session = async_create_clientsession(hass)
        cloud = EWeLinkCloud(session, server, username, password)
        if await cloud.async_login():
            await cloud.async_update_devices()
            cloud.open_websocket()
            hass.data[DOMAIN] = {}
            hass.data[DOMAIN][CLOUD] = cloud
            return True
        else:
            return False
    else:
        async_track_point_in_utc_time(hass, async_setup_entities, dt_util.utcnow())
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry):
    config = config_entry.data
    conf_type = config.get(CONF_TYPE)
    device_type = config.get(CONF_DEVICE_TYPE)
    if conf_type == CLOUD:
        if DOMAIN in hass.data:
            cloud = hass.data.get(DOMAIN).get(CLOUD)
            if cloud is not None:
                await cloud.async_close_websocket()
        hass.data[DOMAIN].pop(CLOUD)
        hass.data.pop(DOMAIN)
    elif conf_type == DEVICE:
        if SUPPORTED_DEVICES.get(device_type):
            for platform in SUPPORTED_DEVICES.get(device_type).keys():
                hass.config_entries.async_forward_entry_unload(config_entry, platform)
    return True
