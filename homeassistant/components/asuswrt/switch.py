"""Support for ASUSWRT routers."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DATA_ASUSWRT,
    DOMAIN,
)
from .router import AsusWrtRouter, AsusWrtVpnInfo


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the sensors."""
    router: AsusWrtRouter = hass.data[DOMAIN][entry.entry_id][DATA_ASUSWRT]
    tracked: set = set()

    @callback
    def update_router() -> None:
        """Update the values of the router."""
        add_entities(router, async_add_entities, tracked)

    router.async_on_close(
        async_dispatcher_connect(hass, router.signal_vpn_client_new, update_router)
    )

    update_router()


@callback
def add_entities(
    router: AsusWrtRouter, async_add_entities: AddEntitiesCallback, tracked: set[str]
) -> None:
    """Add new tracker entities from the router."""
    new_tracked = []

    for id, vpn_info in router.vpn_clients.items():
        if id in tracked:
            continue

        new_tracked.append(AsusWrtVpnSwitch(router, vpn_info))
        tracked.add(id)

    async_add_entities(new_tracked)


class AsusWrtVpnSwitch(SwitchEntity):
    """A switch to control a AsusWrt VPN Client."""

    def __init__(self, router: AsusWrtRouter, vpn_client: AsusWrtVpnInfo):
        """Initialize a AsusWrt VPN Switch."""
        self._router = router
        self._vpn_client = vpn_client

        id = vpn_client.id
        self._attr_name = f"VPN Client {id}"
        self._attr_device_info = router.device_info
        self._attr_unique_id = f"{router.unique_id}_vpn_client_{id}"

    @property
    def is_on(self) -> bool | None:
        """Return the state of the switch."""
        return self._vpn_client.is_on

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        """Return extra attributes."""
        return {
            "client_name": self._vpn_client.description,
        }

    async def async_turn_on(self, **_):
        """Turn the VPN client on."""
        await self._router.start_vpn_client(self._vpn_client.id)
        self._vpn_client.turn_on()
        self.async_write_ha_state()

    async def async_turn_off(self, **_):
        """Turn the VPN client off."""
        await self._router.stop_vpn_client(self._vpn_client.id)
        self._vpn_client.turn_off()
        self.async_write_ha_state()

    @callback
    def async_on_demand_update(self) -> None:
        """Update state."""
        self._vpn_client = self._router.vpn_clients[self._vpn_client.id]
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Register state update callback."""
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                self._router.signal_vpn_client_update,
                self.async_on_demand_update,
            )
        )
