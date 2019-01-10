#/usr/bin/python
#-*- coding:utf-8 -*-

import yaml
import os
import sys
import socket
import zipfile
# path of download config yaml
configPath = "./kubespray-2.8.1/roles/download/defaults/main.yml"
# binary file name
kubeadm_download_url = ""
hyperkube_download_url = ""
etcd_download_url = ""
cni_download_url = ""
# registry config
# /var/lib/registry
var_lib = ""
docker_reg = ""
# temp registry addr
registry = ""
# ansible 配置
ansibleConf = "inventory/netcluster/hosts.ini"


def getLocalIp():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip


def downLoadServer():
    # command = "apt-get install nginx"
    # os.system(command)
    # os.mkdir("/var/www/package")
    # ln = "ln -s ./package /var/www/package"
    # os.system(ln)
    addr = "http://" + getLocalIp() + "/package"
    return addr

def registryDocker():
    comamnd = "docker run -d \
    -p 5000:5000 \
    -p 443:443 \
    -v " + var_lib + ":/var/lib/registry \
    -v " + docker_reg + ":/etc/docker/registry \
    registry.docker-cn.com/library/registry:2"
    os.system(comamnd)


def parseYaml(url):
    # version_map = []
    # with open(configPath,"r") as f:
    #     data = yaml.load(f)
    #     version_map = data.items()
    # version_map["registry"] = registry
    # version_map["kubeadm_download_url"] = kubeadm_download_url
    # version_map["hyperkube_download_url"] = hyperkube_download_url
    # version_map["etcd_download_url"] = etcd_download_url
    # version_map["cni_download_url"] = cni_download_url
    fr = open(configPath,"r+")
    rlines = fr.readlines()
    wlines = ''
    for line in rlines:
        if line.find("registry:") == 0 :
            line = "registry: " + registry
        elif line.find("downloadurl:") == 0 :
            line = "downloadurl: " + url
        wlines += line
    fw = open(configPath,"w+")
    fw.writelines(wlines)

def pushImage():
    zipPath = "./k8s_offline.zip"
    zfile = zipfile.ZipFile(zipPath)
    temp = "./temp"
    os.mkdir(temp)
    for names in zfile.namelist():
        zfile.extract(names,temp)
    zfile.close()
    files = os.listdir(temp)
    for file in files:
        imageName = file.replace("#","/")
        imageName = registry + "/" + imageName
        comand = "docker load " + file + " > " + " " + imageName
        p = os.popen(comand)
        print( p.read() )
        pushCommand = "docker push " + imageName
        p1 = os.popen(pushCommand)
        print( p1.read() )

def runAnsible():
    command = "ansible-playbook -i " + ansibleConf + " " + " cluster.yml -b -v --private-key=~/.ssh/id_rsa"
    p = os.popen(command)
    print(p.read())

if __name__ == "__main__":
    addr = downLoadServer()
    parseYaml(addr)
    # pushImage()
    # runAnsible()
    pass