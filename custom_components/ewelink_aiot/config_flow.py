from .const import DOMAIN, CLOUD, DEVICE, CONF_SERVER, CONF_DEVICE_TYPE
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, CONF_TYPE, CONF_DEVICE_ID
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from .ewelinkcloud import EWeLinkCloud
import voluptuous as vol

SERVERS = {
    "China": "China",
    "Asian": "Asian",
    "America": "America",
    "Europe": "Europe"
}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    cloud = None
    dev_list = {}

    def _already_configured(self, device_id):
        for entry in self._async_current_entries():
            if device_id == entry.data.get(CONF_DEVICE_ID):
                return True
        return False

    async def async_step_user(self, user_input=None, error=None):
        if DOMAIN in self.hass.data:
            self.cloud = self.hass.data.get(DOMAIN).get(CLOUD)
        if self.cloud:
            return await self.async_step_device()
        elif user_input is not None:
            session = async_create_clientsession(self.hass)
            cloud = EWeLinkCloud(
                session,
                user_input[CONF_SERVER],
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD]
            )
            if await cloud.async_login():
                user_input[CONF_TYPE] = CLOUD

                return self.async_create_entry(
                    title=user_input[CONF_USERNAME],
                    data=user_input)
            else:
                return await self.async_step_user(error="cant_login")

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(CONF_SERVER, default=["China"]): vol.In(SERVERS)
            }),
            errors={"base": error} if error else None
        )

    async def async_step_device(self, user_input=None, error=None):
        if user_input is not None:
            device = self.cloud.get_device(user_input[CONF_DEVICE_ID])
            user_input[CONF_TYPE] = DEVICE
            user_input[CONF_DEVICE_TYPE] = device.device_type
            return self.async_create_entry(
                title=self.dev_list[user_input[CONF_DEVICE_ID]],
                data=user_input)

        if error is None:
            await self.cloud.async_update_devices()
            devices = self.cloud.devices
            self.dev_list = {}
            for device in devices.values():
                if not self._already_configured(device.device_id):
                    self.dev_list[device.device_id] = f"{device.name}({device.device_id})"
            if len(self.dev_list) == 0:
                return await self.async_step_device(error="no_devices")
        return self.async_show_form(
            step_id="device",
            data_schema=vol.Schema({
                vol.Required(CONF_DEVICE_ID): vol.In(self.dev_list)
            }),
            errors={"base": error} if error else None
        )
