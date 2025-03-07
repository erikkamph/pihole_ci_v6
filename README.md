# PiHole V6 Custom Integration
## Setup
### Setup with git and docker
1. `git clone git@github.com:erikkamph/pihole_ci_v6.git` if using ssh otherwise `git clone https://github.com/erikkamph/pihole_ci_v6.git`
2. `cd pihole_ci_v6/custom_components`
3. `docker cp ./pihole <container_name>:/config/custom_components/pihole`
4. Reload HomeAssistant with either `docker restart <container_name>` or by heading to settings and clicking the power icon in the upper right corner and then restart in the pop-up.
5. Enjoy!

### Setup with HACS
1. Copy the url `https://github.com/erikkamph/pihole_ci_v6.git`
2. Open HomeAssistant and go to HACS
3. Navigate to "Integrations" and click on "Add custom repository"
4. Search for `Pi-Hole V6` and install it
5. Restart HomeAssistant by heading to settings and clicking the power icon in the upper right corner and then restart in the pop-up. 
6. Enjoy!

### Setup using script
1. `curl -O setup.sh https://raw.githubusercontent.com/erikkamph/pihole_ci_v6/refs/heads/main/setup.sh`
2. `chmod +x setup.sh`
3. `./setup.sh -c <location_of_ha_config>`
    1. Add `-d <ha_container_name>` to restart the docker container
    2. Add `-r <ha_container_name>` to restat ha from inside the container
    3. Skip the two above and go to step 4
4. Go into HomeAssistant under settings, click the power icon in the upper right and then restart in the pop-up.
5. Enjoy!