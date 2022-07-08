from homeassistant.const import (
    TEMP_CELSIUS,
    DEVICE_CLASS_TEMPERATURE
)

ENTITIES = {
    1: {
        "switch": [{
            "class": "switch",
            "sub_class": "EWeLinkSwitch1",
            "state_param": "switch",
        }],
        "sensor": [{
            "class": "sensor",
            "sub_class": "EWeLinkEntity",
            "state_param": "rssi",
            "icon": "mdi-signal-variant",
            "unit": "dB",
            "suffix": "RSSI"
        }],
    },
    151: {
        "climate": [{
            "class": "climate",
            "sub_class": "EWeLinkClimate151",
            "state_param": "mode",
        }]
    },
    175: {
        "climate": [{
            "class": "climate",
            "sub_class": "EWeLinkClimate171",
            "state_param": "mode",
        }]
    }
}
