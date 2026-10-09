#!/bin/bash
# Setup script for the Claude Code cloud environment ("Proyecto New 3ds").
# Installs devkitPro (devkitARM, libctru, citro2d/3d) and the SDL 1.2
# portlibs for 3DS, so 3DS homebrew can be built inside the session.
# Needs these domains allowed in Network access: devkitpro.org,
# apt.devkitpro.org, pkg.devkitpro.org, downloads.devkitpro.org.
set -e

if [ ! -x /opt/devkitpro/pacman/bin/pacman ]; then
    install -d /usr/local/share/keyring
    wget -qO /usr/local/share/keyring/devkitpro-pub.gpg https://apt.devkitpro.org/devkitpro-pub.gpg
    echo "deb [signed-by=/usr/local/share/keyring/devkitpro-pub.gpg] https://apt.devkitpro.org stable main" \
        > /etc/apt/sources.list.d/devkitpro.list
    apt-get update -q
    apt-get install -y -q devkitpro-pacman
    [ -e /etc/mtab ] || ln -s /proc/self/mounts /etc/mtab
fi

export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
dkp-pacman -Sy --noconfirm --needed 3ds-dev \
    3ds-sdl 3ds-sdl_mixer 3ds-sdl_ttf 3ds-sdl_image 3ds-sdl_gfx \
    3ds-libvorbisidec 3ds-libmad 3ds-libogg 3ds-freetype \
    3ds-libpng 3ds-libjpeg-turbo 3ds-zlib || true
