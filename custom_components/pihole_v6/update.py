from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.components.update import UpdateEntity, UpdateEntityDescription, UpdateEntityFeature
from .entity import PiHoleEntity
from .coordinator import PiHoleUpdateCoordinator
from .hole import PiHole
import asyncio, os, shutil, zipfile, io
from .models.const import DOMAIN


async def async_setup_entry(hass: HomeAssistant,
                            config: ConfigEntry,
                            async_add_entities: AddEntitiesCallback):
    updates = {
        'core': {
            'name': "Update available (Core)",
            'key': "core_update_available",
            'translation_key': "core_update_available"
        },
        'ftl': {
            'name': "Update available (FTL)",
            'key': "ftl_update_available",
            'translation_key': "ftl_update_available"
        },
        'web': {
            'name': "Update available (Web)",
            'key': "web_update_available",
            'translation_key': "web_update_available"
        },
    }

    update_entities = []
    for key in updates.keys():
        description = UpdateEntityDescription(**updates[key])
        update_entities.append(
            PiHoleComponentUpdate(
                config.runtime_data.coordinator,
                config.entry_id,
                config,
                hass,
                description,
                key,
                0
            )
        )

    integration_description = UpdateEntityDescription(
        name="Pi-Hole V6",
        key="integration_update_available",
        translation_key="integration_update_available"
    )
    update_entities.append(
        IntegrationUpdate(
            config.runtime_data.coordinator,
            config.entry_id,
            config,
            hass,
            integration_description,
            0
        )
    )
    config.runtime_data.entities = update_entities
    async_add_entities(update_entities)


class IntegrationUpdate(PiHoleEntity, UpdateEntity):
    def __init__(self,
                 coordinator: PiHoleUpdateCoordinator,
                 server_unique_id: str,
                 config_entry: ConfigEntry,
                 hass: HomeAssistant,
                 description: UpdateEntityDescription,
                 context = None):
        super().__init__(coordinator, description.name, server_unique_id, config_entry, hass, context)
        self._key = 'integration_updates'
        self._manifest_data = config_entry.runtime_data.manifest
        self._attr_installed_version = f"v{self._manifest_data['version']}"
        self._attr_unique_id = f"{server_unique_id}/{self._key}"
        self._attr_latest_version = ""
        self._attr_release_url = ""
        self._attr_available = False
        self._attr_supported_features = (UpdateEntityFeature.RELEASE_NOTES | UpdateEntityFeature.INSTALL | UpdateEntityFeature.PROGRESS)
        self._api = PiHole(hass, config_entry)
        self._attr_zip_url = ""
        self._attr_icon = "mdi:pi-hole"

    def version_is_newer(self, latest_version: str | None, installed_version: str | None):
        return asyncio.run_coroutine_threadsafe(self._api.version_is_newer(latest_version, installed_version), self.hass.loop)

    @callback
    def _handle_coordinator_update(self):
        if self._key in self.coordinator.data:
            data = self.coordinator.data[self._key]
            self._attr_latest_version = data['latest_version']
            self._attr_release_url = data['release_url']
            self._attr_zip_url = data['zip_file']
            self._attr_available = True
            self.async_write_ha_state()
    
    @property
    def icon(self):
        return self._attr_icon

    @property
    def name(self):
        return self._name
    
    @property
    def latest_version(self):
        return self._attr_latest_version
    
    @property
    def installed_version(self):
        return self._attr_installed_version
    
    @property
    def release_url(self):
        return self._attr_release_url
    
    async def async_release_notes(self):
        if self._key in self.coordinator.data:
            data = self.coordinator.data[self._key]
            release_notes = data['release_notes']
            return release_notes
        return None
    
    @property
    def update_percentage(self):
        return self._attr_update_percentage
    
    async def backup_integration(self):
        integration = self.hass.config.path(f'custom_components/{DOMAIN}')
        integration_backup = f"{integration}.bak"
        shutil.move(integration, integration_backup)

    async def update_integration(self, version: str | None):
        integration = self.hass.config.path(f'custom_components/{DOMAIN}')
        session = async_get_clientsession(self.hass)
        async with session.get(self._attr_zip_url) as r:
            zip_data = await r.read()
        self._attr_update_percentage = 50
        self.async_write_ha_state()
        
        file = zipfile.ZipFile(io.BytesIO(zip_data))
        file.extractall(integration)
        self._attr_update_percentage = 100
        self.async_write_ha_state()

    async def async_install_with_progress(self, version: str | None, backup: bool):
        self._attr_in_progress = True
        self.async_write_ha_state()

        try:
            if self._attr_zip_url != "":
                if backup:
                    await self.backup_integration()
                    self._attr_update_percentage = 30
                    self.async_write_ha_state()

                await self.update_integration(version)
        finally:
            self._attr_in_progress = False
            self.async_write_ha_state()



class PiHoleComponentUpdate(PiHoleEntity, UpdateEntity):
    def __init__(self, coordinator: PiHoleUpdateCoordinator,
                 server_unique_id: str,
                 config_entry: ConfigEntry,
                 hass: HomeAssistant,
                 entity_description: UpdateEntityDescription,
                 key: str,
                 context = None):
        super().__init__(coordinator,
                         entity_description.name,
                         server_unique_id,
                         config_entry,
                         hass,
                         context)
        self._attr_available = False
        self._attr_unique_id = f"{self._server_unique_id}/{entity_description.key}"
        self._attr_latest_version = None
        self._attr_installed_version = None
        self._key = key
        self._api = PiHole(hass, config_entry)
        self._attr_icon = "mdi:pi-hole"

        self._repo = "https://github.com/pi-hole/"
        self._release = "/releases/tag"
        
        match self._key:
            case 'core':
                self._release_url_base = f"{self._repo}pi-hole{self._release}"
            case 'ftl':
                self._release_url_base = f"{self._repo}FTL{self._release}"
            case 'web':
                self._release_url_base = f"{self._repo}web{self._release}"
    
    @property
    def icon(self):
        return self._attr_icon
    
    @callback
    def _handle_coordinator_update(self):
        if 'versions' in self.coordinator.data:
            versions = self.coordinator.data['versions']
            match self._key:
                case 'core':
                    self._attr_installed_version = versions.version.core.local.version
                    self._attr_latest_version = versions.version.core.remote.version
                case 'web':
                    self._attr_installed_version = versions.version.web.local.version
                    self._attr_latest_version = versions.version.web.remote.version
                case 'ftl':
                    self._attr_installed_version = versions.version.ftl.local.version
                    self._attr_latest_version = versions.version.ftl.remote.version
            self.async_write_ha_state()
    
    def version_is_newer(self, latest_version: str | None, installed_version: str | None):
        return asyncio.run_coroutine_threadsafe(self._api.version_is_newer(latest_version, installed_version), self.hass.loop)

    @property
    def name(self):
        return self._name

    @property
    def latest_version(self):
        return self._attr_latest_version
    
    @property
    def installed_version(self):
        return self._attr_installed_version
    
    @property
    def release_url(self):
        try:
            if not self.version_is_newer(self._attr_latest_version, self._attr_installed_version):
                version = self._attr_installed_version
            else:
                version = self._attr_latest_version
            return f"{self._release_url_base}/{version}"
        except Exception:
            return f"{self._release_url_base}/{self._attr_installed_version}"