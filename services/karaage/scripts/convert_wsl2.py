#!/usr/bin/env python
import sys
import os
import shutil
import docker
import subprocess

shutil.copyfile('/mnt/c/Users/karaage/GitHub/stable-diffusion-webui-docker/scripts/input.png', '/home/karaage/stable-diffusion-webui-docker/cache/input.png')
# shutil.copyfile('/mnt/c/Users/karaage/GitHub/stable-diffusion-webui-docker/scripts/info.txt', './info.txt')

client = docker.from_env()
container_name = client.containers.list()[0].name

cmd = 'docker exec ' + container_name + ' python scripts/ai_zoo.py --prompt "kawaii bear" --seed -1 --init-img /cache/input.png --strength 0.5 --skip_grid'
# print(cmd)
# subprocess.run(cmd, shell=True)