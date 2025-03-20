# PiHole V6 Custom Integration
This is a Pi-Hole Custom Integration for version 6 of Pi-Hole which introduced sessions and moved the api from `/admin/api` to `/api`. The integration has a checklist besides the stuff that is implemented or to be implemented and it can be found at [/CHECKLIST.md](/CHECKLIST.md). If you want a feature to be implemented, visit the [issues](https://github.com/erikkamph/pihole_ci_v6/issues) page. If accepted, the issue will be linked in the [/TODO.md](/TODO.md) to track.

## Navigation
This is basic navigation for the [README.md](/README.md) until full docs are in place for the custom integration.
- [Semantic Versioning](#semantic-versioning)
- [Dependencies](#dependencies)
- [Translations](#translations)
- [Installation](#setup)
    - [Installation with docker](#setup-with-git-and-docker)
    - [Installation via HACS](#setup-with-hacs)
    - [Installation with script](#setup-using-script)
- [Uninstallation](#removal-of-pihole_v6)
- [Configuration](#configuring-the-integration-in-home-assistant)
- [Actions](#actions)
    - [Toggle Pi-Hole](#pi-hole-toggle)
    - [Update Gravity](#update-gravity)
    - [Flush Arp/Logs](#flush-arplogs)
    - [Restart DNS](#restart-dns)
- [Development](#development)
    - [Notes](#note)

## Semantic Versioning
This repository uses semantic versioning, more information can be found at [https://semver.org/](https://semver.org/).
A short summary can be read below:
```
Given a version number MAJOR.MINOR.PATCH, increment the:

MAJOR version when you make incompatible API changes
MINOR version when you add functionality in a backward compatible manner
PATCH version when you make backward compatible bug fixes
Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.
```

## Dependencies
Python package dependencies:
- `pydantic==2.10.6`
- `validators==0.34.0`
- `aiofiles==24.1.0`
- `pandas==2.2.3`

## Translations
Currently available for following languages:
- Japanese
- Swedish
- English

Please verify translation, and if you have a suggestion, open an issue and I will fix it.
If you want a translation for your language, open a PR in a separate branch and I will check it.

## Setup
### Setup with git and docker
1. `git clone git@github.com:erikkamph/pihole_ci_v6.git` if using ssh otherwise `git clone https://github.com/erikkamph/pihole_ci_v6.git`
2. `cd pihole_ci_v6/custom_components`
3. `docker cp ./pihole <container_name>:/config/custom_components/pihole`
4. Reload Home Assistant with either `docker restart <container_name>` or by heading to settings and clicking the power icon in the upper right corner and then restart in the pop-up.
5. Enjoy!

### Setup with HACS
1. Copy the url `https://github.com/erikkamph/pihole_ci_v6.git`
2. Open Home Assistant and go to HACS
3. Navigate to "Integrations" and click on "Add custom repository"
4. Search for `Pi-Hole V6` and install it
5. Restart Home Assistant by heading to settings and clicking the power icon in the upper right corner and then restart in the pop-up. 
6. Enjoy!

### Setup using script
1. `curl -O setup.sh https://raw.githubusercontent.com/erikkamph/pihole_ci_v6/refs/heads/main/setup.sh`
2. `chmod +x setup.sh`
3. `./setup.sh -c <location_of_ha_config>`
    1. Add `-d <ha_container_name>` to restart the docker container
    2. Add `-r <ha_container_name>` to restat ha from inside the container
    3. Skip the two above and go to step 4
4. Go into Home Assistant under settings, click the power icon in the upper right and then restart in the pop-up.
5. Enjoy!

## Removal of pihole_v6
1. Remove all configurations under `Settings -> Devices & Services -> Pi-Hole V6 (Dev)`
2. Remove the folder `pihole_v6` from `custom_components` in the Home Assistant configuration folder
3. Reload Home Assistant from `Settings -> Three dots upper right corner -> Restart Home Assistant`
4. The integration should now be successfully removed from Home Assistant

## Configuring the integration in Home Assistant
Steps to configure the integration after installing using [#setup](#setup).
1. Visit `Devices & services` under `Settings`.
2. Click `Add integration` in the bottom right corner
3. Search for and select `Pi-Hole V6`
4. In the dialogue `Step 1` enter a configuration name, this will also be the name of the device. The preferred name is in lowercase without spaces.
5. In the dialogue `Step 2`
    1. Enter the location of the pihole instance without `http(s)` and without `/api`
    2. Select `https` or `http`
    3. Enter `api` if the api is located at `/api`.
    4. Enter the relevant port that pihole is running at, `80` and `443` are standard for https and doesn't get included in the url.
    5. Select `Verify SSL` if it should verify the http/https certificate
6. In the dialogue `Step 3`, enter the API key, if you don't have one you can create one using following steps:
    1. Open your pihole instance and login
    2. Under `System` click `Settings`
    3. Go to `Web interface / API`
    4. Switch from `Basic` to `Advanced` mode in the upper right corner
    5. Click on `Configure app password`
    6. Copy the password under the text `Your new app password is:` which is hidden behind black stripes for security.
    7. Go back to Home Assistant and enter the app password you copied from the previous step in the input.
7. Enjoy your newly configured `Pi-Hole V6` integration

## Actions
### Pi-Hole Toggle
Toggles Pi-Hole on or off for a period of 5 minues.

### Update Gravity
Sends a POST request to Pi-Hole telling it to update the ad block lists for Gravity.

### Flush Arp/Logs
Clears the logs or ARP tables.

### Restart DNS
Restarts the DNS of the Pi-Hole instance.

## Development
The `compose.yaml` file can be found [/development/compose.yaml](/development/compose.yaml) and contains
two images, the official Home Assistant image and the official pihole image. Both of the images mentioned and their settings can be found at following locations:
- [https://hub.docker.com/r/pihole/pihole](https://hub.docker.com/r/pihole/pihole)
- [https://www.home-assistant.io/installation/linux#docker-compose](https://www.home-assistant.io/installation/linux#docker-compose)

The passwords in the [/development/compose.yaml](/development/compose.yaml) are just generic passwords and can be replaced with environment variables in a `.env`-file like so:
```.env
PIHOLE_FTL_PASSWORD=
TZ=
```
`TZ` replaces the `TZ` standard setting in the `compose.yaml` file with the timezone you have. While `PIHOLE_FTL_PASSWORD` replaces the generic password in the same file, the password you set is the password you'll login with and for use with the integration unless you create an API specific password, in which case you'll use that instead. Once you have set all variables to your liking, start the environment with
```sh
docker compose -f development/compose.yaml up -d
```
or
```sh
(cd development && docker compose up -d)
```
The last step to do when developing on the integration is to run the following command:
```sh
sudo cp -r custom_components/ ./development/ha/custom_components
```
And also reload Home Assistant once that is done for it to discover the custom integration. This command also needs to be executed each time you've done some change in the integration for Home Assistant to pick it up.

### Note
The `.env`-file must be in the same directory as the compose file.