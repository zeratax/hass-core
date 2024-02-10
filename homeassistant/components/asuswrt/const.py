"""AsusWrt component constants."""
from enum import Enum

DOMAIN = "asuswrt"

CONF_DNSMASQ = "dnsmasq"
CONF_INTERFACE = "interface"
CONF_REQUIRE_IP = "require_ip"
CONF_SSH_KEY = "ssh_key"
CONF_TRACK_UNKNOWN = "track_unknown"

DATA_ASUSWRT = DOMAIN

DEFAULT_DNSMASQ = "/var/lib/misc"
DEFAULT_INTERFACE = "eth0"
DEFAULT_TRACK_UNKNOWN = False

KEY_COORDINATOR = "coordinator"
KEY_METHOD = "method"
KEY_SENSORS = "sensors"

MODE_AP = "ap"
MODE_ROUTER = "router"

PROTOCOL_HTTP = "http"
PROTOCOL_HTTPS = "https"
PROTOCOL_SSH = "ssh"
PROTOCOL_TELNET = "telnet"

# Sensors
SENSORS_BYTES = ["sensor_rx_bytes", "sensor_tx_bytes"]
SENSORS_CONNECTED_DEVICE = ["sensor_connected_device"]
SENSORS_LOAD_AVG = ["sensor_load_avg1", "sensor_load_avg5", "sensor_load_avg15"]
SENSORS_RATES = ["sensor_rx_rates", "sensor_tx_rates"]
SENSORS_TEMPERATURES_LEGACY = ["2.4GHz", "5.0GHz", "CPU"]
SENSORS_TEMPERATURES = [*SENSORS_TEMPERATURES_LEGACY, "5.0GHz_2", "6.0GHz"]

# Vpn Clients
VPN_CLIENT_STATE_OFF = "off"
VPN_CLIENT_STATE_STARTING = "starting"
VPN_CLIENT_STATE_ON = "on"

class AsusWrtVpnState(str, Enum):
    """AsusWrt VPN Client States."""

    OFF = VPN_CLIENT_STATE_OFF
    STARTING = VPN_CLIENT_STATE_STARTING
    ON = VPN_CLIENT_STATE_ON
