from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.update import UpdateEntity, UpdateEntityDescription
from .entity import PiHoleEntity
from .coordinator import PiHoleUpdateCoordinator


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
        name="Update available (Integration)",
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
        self._attr_installed_version = self._manifest_data['version']
        self._attr_unique_id = f"{server_unique_id}/{self._key}"
        self._attr_latest_version = ""
        self._attr_release_url = ""
        self._attr_available = False

    def version_is_newer(self, latest_version, installed_version):
        if not latest_version or latest_version == '':
            return False
        
        if not installed_version or installed_version == '':
            raise ValueError("Unknown version installed")
        
        latest = latest_version.replace("v", "").split(".")
        installed = latest_version.replace("v", "").split("")

        for i, v in enumerate(latest):
            if int(v) > int(installed[i]):
                return True
        return False

    @callback
    def _handle_coordinator_update(self):
        if self._key in self.coordinator.data:
            data = self.coordinator.data[self._key]
            self._attr_latest_version = data['latest_version']
            self._attr_release_url = data['release_url']
            self._attr_available = True
            self.async_write_ha_state()

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

        self._repo = "https://github.com/pi-hole/"
        self._release = "/releases/tag"
        
        match self._key:
            case 'core':
                self._release_url_base = f"{self._repo}pi-hole{self._release}"
            case 'ftl':
                self._release_url_base = f"{self._repo}FTL{self._release}"
            case 'web':
                self._release_url_base = f"{self._repo}web{self._release}"
    
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
        if latest_version is None or latest_version == '':
            return False
        
        if installed_version is None or installed_version == '':
            raise ValueError("Unknown version installed")

        latest = latest_version.replace("v", "").split(".")
        installed = installed_version.replace("v", "").split(".")

        for i, v in enumerate(latest):
            if int(installed[i]) < int(v):
                return True
        return False

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