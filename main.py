#/usr/bin/python
#-*- coding:utf-8 -*-

import yaml

configPath = "F:\\k8s\kubespray-2.8.1\\kubespray-2.8.1\\roles\download\defaults\\main.yml"



def parseYaml():
    version_map = []
    with open(configPath,"r") as f:
        data = yaml.load(f)
    # for key,value in data.items():


if __name__ == "__main__":
    parseYaml()
    pass