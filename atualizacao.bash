#!/bin/bash

# Atualiza o sistema
sudo apt-get update
sudo apt-get upgrade

# Atualiza os pacotes usados no programa
sudo apt-get install python3-pip

# Atualiza o pip
pip3 install --upgrade pip
pip3 install networkx
pip3 install matplotlib
pip3 install rich

echo "Atualização concluída!"