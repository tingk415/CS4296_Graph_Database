#!/bin/bash

sudo yum update -y
sudo amazon-linux-extras install epel -y
sudo yum install -y java-11-amazon-corretto-headless neo4j-enterprise-5.6.0-1.noarch

sudo sed -i 's/#dbms.default_listen_address=0.0.0.0/dbms.default_listen_address=0.0.0.0/g' /etc/neo4j/neo4j.conf
sudo sed -i 's/#server.default_listen_address=0.0.0.0/server.default_listen_address=0.0.0.0/g' /etc/neo4j/neo4j.conf

sudo sed -i 's/#server.http.enabled=true/server.http.enabled=true/g' /etc/neo4j/neo4j.conf
sudo sed -i 's/#server.http.listen_address=0.0.0.0:7474/server.http.listen_address=:7474/g' /etc/neo4j/neo4j.conf
sudo sed -i 's/#server.http.advertised_address=/server.http.advertised_address=:7474/g' /etc/neo4j/neo4j.conf

sudo sed -i 's/#dbms.connector.bolt.enabled=true/dbms.connector.bolt.enabled=true/g' /etc/neo4j/neo4j.conf
sudo sed -i 's/#dbms.connector.bolt.tls_level=DISABLED/dbms.connector.bolt.tls_level=DISABLED/g' /etc/neo4j/neo4j.conf
sudo sed -i 's/#dbms.connector.bolt.listen_address=:7687/dbms.connector.bolt.listen_address=:7687/g' /etc/neo4j/neo4j.conf
sudo sed -i 's/#dbms.connector.bolt.advertised_address=:7687/dbms.connector.bolt.advertised_address=:7687/g' /etc/neo4j/neo4j.conf

sudo sed -i 's/#dbms.logs.http.enabled=true/dbms.logs.http.enabled=true/g' /etc/neo4j/neo4j.conf
sudo sed -i 's/#dbms.security.allow_csv_import_from_file_urls=true/dbms.security.allow_csv_import_from_file_urls=true/g' /etc/neo4j/neo4j.conf

sudo systemctl start neo4j