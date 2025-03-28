## What's changed
- Data for the github poll which requires update will now only update once every 7 days
- Polling for github data for pihole components has been removed
- Statistics has changed structure, we are talking about total clients and active clients not seen clients and unique clients. This is beause the data and description is about the total number of clients and the number of active clients last 24 hours.

## Breaking changes
**None**

## Bug fixes
**None**

## Known bugs
- Devices does not get properly removed, e.g. when reloading Home Assistant it creates a new device with the same entities and the old is left without entities.
