#! /bin/bash


# NB: all'interno di questo file e' preferibile non eseguire comandi bloccanti o lanciare
# applicazioni in background sino a quando non si risolve il problema del riavvio dei nodi.

echo "Installazione di: finger"
sudo apt-get install -y finger

echo "Installazione di: Java JRE e JDK"
sudo apt-get install -y default-jre
sudo apt-get install -y default-jdk

echo "Installazione di: librerie varie di Python"
sudo apt-get install -y build-essential python-dev
sudo apt-get install -y python-setuptools
sudo easy_install pip

echo "Installazione di: Django"
sudo pip install django
sudo pip install requests

echo "Installazione di: RabbitMQ, Celery e Flower"
echo "deb http://www.rabbitmq.com/debian/ testing main" | sudo tee -a /etc/apt/sources.list
sudo apt-get update
sudo apt-get install -y --force-yes rabbitmq-server
sudo pip install Celery
sudo pip install flower

echo "Installazione di: OpenCV"
sudo apt-get install -y --force-yes python-numpy python-opencv


