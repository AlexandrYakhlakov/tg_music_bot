#!/bin/bash
artist_name=$1
song_name=$2
path="PATH/tg_music_bot/utils/"
time=$3
timeout "$time"m parec --device=alsa_output.pci-0000_00_14.2.analog-stereo.monitor --volume=65536 --raw|lame -r -s -V 0 -b 320 - "$path""$artist_name"-"$song_name"
