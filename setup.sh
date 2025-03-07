#!/bin/sh

copy_to_config() {
    local ha_conf_dir="$1"

    if ! command -v git; then
        echo "You must have git installed!"
        exit -1
    fi

    if [ ! -d "$ha_conf_dir" ]; then
        echo "The path '$ha_conf_dir' is not a valid directory!"
        exit -1
    fi

    git clone git@github.com:erikkamph/pihole_ci_v6.git
    cd pihole_ci_v6/custom_components
    cp -R pihole "$ha_conf_dir/custom_components"
}

check_for_docker() {
    if command -v docker; then
        return 0
    fi
    return 1
}

check_for_container() {
    local container="$(echo "$1" | tr "[[:upper:]]" "[[:lower:]]")"
    local tmp_file="/tmp/$RANDOM.txt"

    if ! check_for_docker; then
        exit 1
    fi

    docker container ls > "$tmp_file"
    if grep -qc "$container" "$tmp_file"; then
        rm "$tmp_file"
        return 0
    fi
    rm "$tmp_file"

    exit 1
}

restart_container() {
    local container="$1"
    docker container restart "$container"
}

restart_inside_container() {
    local container="$1"
    docker exec "$container" hassio 1> /dev/null
    
    if [ "$?" -ne "0" ]; then
        echo "This only works if the hassio command exists!"
        exit 1
    fi

    docker exec "$container" hassio homeassistant restart
}

usage() {
    cat <<EOF
Usage: ./setup.sh [-h] [-c ha_config_dir] [-d container_name] [-r container_name]

Arguments:
-h                  Show this help text and exit
-c ha_config_dir    Point this argument to the HomeAssistant config dir
-d container_name   Restarts the docker container if you are running in docker
-r container_name   The same as "-d" but restarts HomeAssistant inside the container

Notes:
You can't supply "-d" if you supply "-r" and the other way around.
This is because "-r" restarts HomeAssistant inside the container,
while "-d" restarts the whole container. Both will check if the
container exists before restarting and if you actually have docker
installed on the computer or wherever you are running this script.
EOF
    exit -1
}

r_container=0
r_inside=0
container=""

while getopts "hc:d:r:" opt; do
    case ${opt} in
        c)
            copy_to_config "${OPTARG}"
            ;;
        d)
            r_container=1
            container="${OPTARG}"
            ;;
        r)
            r_inside=1
            container="${OPTARG}"
            ;;
        *)
            usage
            ;;
    esac
done

if [ "$r_inside" -eq "1" ] && [ "$r_container" -eq 1 ]; then
    usage
fi

if [ "$r_inside" -eq "1" ]; then
    check_for_container "$container"
    restart_inside_container "$container"
fi

if [ "$r_container" -eq "1" ]; then
    check_for_container "$container"
    restart_container "$container"
fi