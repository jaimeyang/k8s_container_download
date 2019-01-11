#/usr/bin/python
#-*- coding:utf-8 -*-

import common
import subprocess

username = "node0"
pwd = "123456"
def registry():
    comand = "mkdir registry"
    subprocess.call(comand,shell=True)
    comand1 = "cd registry & openssl genrsa -out \"root-ca.key\" 4096 "
    subprocess.call(comand1,shell=True)
    comand2 = "cd registry & openssl req -new -key \"root-ca.key\" -out \"root-ca.csr\" -sha256 -subj '/C=CN/ST=Guangdong/L=sz/O=docker.domain/CN=docker.domain Docker Registry CA' "
    subprocess.call(comand2,shell=True)
    rootfile = "registry/root-ca.cnf"
    rootline = "basicConstraints = critical,CA:TRUE,pathlen:1 \n" \
                + "keyUsage = critical, nonRepudiation, cRLSign, keyCertSign \n" \
                + "subjectKeyIdentifier=hash \n"
    rootf = open(rootfile,"w+")
    rootf.writelines(rootline)
    rootf.close()
    comand3 = "cd registry & openssl x509 -req  -days 3650  -in \"root-ca.csr\ "  \
               + "-signkey \"root-ca.key\" -sha256 -out \"root-ca.crt " \
               + "-extfile \"root-ca.cnf\" -extensions " \
               + "root_ca"
    subprocess.call(comand3,shell=True)
    comand4 = "cd registry & openssl genrsa -out \"docker.domain.com.key\" 4096"
    subprocess.call(comand4,shell=True)
    comand5 = "cd registry & openssl req -new -key \"docker.domain.com.key\" -out \"site.csr\" -sha256 " \
              + "-subj '/C=CN/ST=Shanxi/L=Datong/O=Your Company Name/CN=docker.domain.com'"
    subprocess.call(comand5,shell=True)
    sitefile = "registry/site.cnf"
    siteline = "authorityKeyIdentifier=keyid,issuer \n" + "basicConstraints = critical,CA:FALSE \n" \
               + "extendedKeyUsage=serverAuth \n" + "keyUsage = critical, digitalSignature, keyEncipherment \n" \
               + "subjectAltName = DNS:docker.domain.com, IP:" + common.getLocalIp() + " \n" \
               + "subjectKeyIdentifier=hash"
    sitef = open(sitefile,"w+")
    sitef.writelines(siteline)
    sitef.close()
    comand6 = "cd registry & openssl x509 -req -days 750 -in \"site.csr\" -sha256 "  \
            + "-CA \"root-ca.crt\" -CAkey \"root-ca.key\"  -CAcreateserial " \
            + "-out \"docker.domain.com.crt\" -extfile \"site.cnf\" -extensions server"
    subprocess.call(comand6,shell=True)
    comand7 = "mkdir registry & mkdir auth"
    subprocess.call(comand7,shell=True)
    command8 = "cp ./config.xml registry/"
    subprocess.call(command8,shell=True)
    comand9 = "cd registry & docker run --rm " \
              +" --entrypoint htpasswd " \
              + "registry " \
              + "-Bbn " + username + pwd + " > auth/nginx.htpasswd"
    subprocess.call(comand9,shell=True)
    hosts = "/etc/hosts"
    hostsfr = open(hosts,"r+")
    linesr = hostsfr.readlines()
    hostsfr.close()
    hostsfw = open(hosts,"w+")
    linesw = ""
    for line in linesr :
        linesw += line
    linesw += "\n" + common.getLocalIp() + "        " + "docker.domain.com"
    hostsfw.writelines(linesw)
    hostsfw.close()
    command10 = "cd registry & mkdir ssl"
    subprocess.call(command10,shell=True)
    comand11 = "cd registry & cp docker.domain.com.key ./ssl & cp docker.domain.crt ./ssl & cp root-ca.crt ./ssl"
    subprocess.call(comand11,shell=True)
    comand12 = "sudo mkdir -p /etc/docker/certs.d/docker.domain.com"
    subprocess.call(comand12,shell=True)
    comand13 = "sudo cp ./registry/ssl/root-ca.crt /etc/docker/certs.d/docker.domain.com/ca.crt"
    subprocess.call(comand13,shell=True)
    comand14 = "sudo docker run -d \
                 -p 5000:5000 \
                -p 443:443 \
                -v ./docker:/var/lib/registry \
                -v ./registry:/etc/docker/registry \
                registry.docker-cn.com/library/registry:2"
    subprocess.call(comand14,shell=True)






