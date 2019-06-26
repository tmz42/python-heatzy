# Custom Component for heatzy (Put it in <config>/custom_components/climate)
import logging

import voluptuous as vol

from homeassistant.components.climate import (ClimateDevice, PLATFORM_SCHEMA,
    SUPPORT_OPERATION_MODE)
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD

import homeassistant.helpers.config_validation as cv

# Home Assistant depends on 3rd party packages for API specific code.
REQUIREMENTS = ['heatzy==0.0.10']

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Heatzy platform."""
    import heatzy

    # Assign configuration variables. The configuration check takes care they are
    # present.
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)

    # Setup connection with devices/cloud
    _LOGGER.info("Trying to add Heatzy devices with "+username+","+password)

    try:
        heatzyHandler = heatzy.HeatzyHandler(username, password)
        heatzyHandler.getHeatzyDevices()
    except Exception as identifier:
        _LOGGER.error("Login error : "+str(identifier))

    add_devices(HeatzyPilote(heatzy_device) for heatzy_device in heatzyHandler.devices())

class HeatzyPilote(ClimateDevice):
    def __init__(self, heatzy_device):
        self.heatzy = heatzy_device
        self._name = heatzy_device.name
        self._operation_list = ['CONFORT', 'ECO', 'HGEL', 'OFF']
        self._support_flags = SUPPORT_OPERATION_MODE
        self._current_operation = heatzy_device.status()

    @property
    def name(self):
        """Return the name of the climate device."""
        return self._name

    @property
    def current_operation(self):
        """Return current operation ie. heat, cool, idle."""
        return self._current_operation
    
    @property
    def operation_list(self):
        """Return the list of available operation modes."""
        return self._operation_list

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return '°C'

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return self._support_flags

    def set_operation_mode(self, operation_mode):
        self.heatzy.setMode(operation_mode)
        self._current_operation = operation_mode
        self.schedule_update_ha_state()

    def update(self):
        self.heatzy.update()
        self._current_operation = self.heatzy.mode