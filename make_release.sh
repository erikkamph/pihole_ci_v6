#!/bin/bash

if [ ! -d "releases" ];
then
    mkdir "releases"
fi

cd custom_components

if [ -f "pihole_v6/.DS_Store" ];
then
    rm "pihole_v6/.DS_Store"
fi

zip -r ../releases/pihole_v6.zip pihole_v6/