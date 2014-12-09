#!/usr/bin/env bash
echo "Installing Debian dependencies"

apt-get -y install git &> /dev/null
apt-get -y install mc vim &> /dev/null

