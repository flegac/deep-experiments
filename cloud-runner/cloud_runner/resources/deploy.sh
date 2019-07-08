#!/usr/bin/env bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3 get-pip.py
sudo pip3 install setuptools
pip3 install --user /tmp/cloud-runner
