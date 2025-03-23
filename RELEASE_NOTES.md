## What's changed
- Sensors do now have `units_of_measurement` connected to them e.g. `Total clients` has `clients` as `unit_of_measurement`
- Sensors have gotten updated icons e.g. `Unique domains` has `mdi:domain` as icon instead of the default `mdi:eye`
- The coordinator downloads release notes from github
- System health checks api quota against github
- Sensors now have `has_entity_name` set to `True`

## Breaking changes
**None**

## Bug fixes
**None**

## Known bugs
- API Limits might be reached when trying to fetch release information from `GitHub`
- Devices does not get properly removed, e.g. when reloading Home Assistant it creates a new device with the same entities and the old is left without entities.
- Release information for different Pi-Hole components gets cut-off.
