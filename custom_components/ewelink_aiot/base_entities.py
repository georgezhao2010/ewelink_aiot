from homeassistant.helpers.entity import Entity, ToggleEntity
from homeassistant.const import STATE_ON, STATE_OFF
from .const import DOMAIN
from typing import Any


class EWeLinkEntity(Entity):
    def __init__(self, ewelink_device, config):
        self._device = ewelink_device
        self._device.register_update(self.update_state)
        self._config = config
        self._device_info = {
            "manufacturer": self._device.brand,
            "model": self._device.model,
            "identifiers": {(DOMAIN, self._device.device_id)},
            "name": self._device.name
        }
        self._unique_id = f"{DOMAIN}.{DOMAIN}_{self._device.device_id}_{self._config.get('state_param')}"
        self.entity_id = self._unique_id

    @property
    def device_info(self):
        return self._device_info

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def state(self):
        return self._device.get_param(self._config.get("state_param"))

    @property
    def device_class(self):
        return self._config.get("device_class")

    @property
    def name(self):
        if self._config.get("suffix"):
            return f"{self._device.name} {self._config.get('suffix')}"
        else:
            return self._device.name

    @property
    def available(self):
        return self._device.available

    @property
    def unit_of_measurement(self):
        return self._config.get("unit")

    @property
    def icon(self):
        return self._config.get("icon")

    @property
    def should_poll(self):
        return False

    def _update_state(self, status):
        result = False
        for key, state in status.items():
            if key == "online":
                result = True
            elif key == self._config.get("state_param"):
                result = True
        return result

    def update_state(self, status):
        if self._update_state(status):
            self.schedule_update_ha_state()


class EWeLinkSwitch(EWeLinkEntity, ToggleEntity):
    def __init__(self, ewelink_device, config):
        super().__init__(ewelink_device, config)

    @property
    def state(self):
        state = self._device.get_param(self._config.get("state_param"))
        return STATE_ON if state == self._config.get("state").get(STATE_ON) else STATE_OFF

    @property
    def is_on(self) -> bool:
        return self._state == STATE_ON

    async def async_turn_on(self, **kwargs: Any):
        await self._device.set_param(
            self._config.get("state_param"),
            self._config.get("state").get(STATE_ON)
        )

    async def async_turn_off(self, **kwargs: Any):
        await self._device.set_param(
            self._config.get("state_param"),
            self._config.get("state").get(STATE_OFF)
        )