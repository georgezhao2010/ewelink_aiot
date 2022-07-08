from homeassistant.const import (
    TEMP_CELSIUS,
    DEVICE_CLASS_TEMPERATURE,
    STATE_ON,
    STATE_OFF
)

SUPPORTED_DEVICES = {
    1: {
        "switch": [{
            "class": "EWeLinkSwitch",
            "state_param": "switch",
            "state": {
                STATE_ON: "on",
                STATE_OFF: "off",
            }
        }],
        "sensor": [{
            "class": "EWeLinkEntity",
            "state_param": "rssi",
            "icon": "mdi:signal",
            "unit": "dB",
            "suffix": "RSSI",
        }],
    },
    151: {
        "climate": [{
            "class": "EWeLinkClimate151",
            "state_param": "mode",
        }]
    },
    175: {
        "water_heater": [{
            "class": "EWeLinkClimate175",
            "state_param": "mode",
        }]
    }
}
