#!/bin/bash

LOG_FILE="/tmp/neo4jsetup.log" 

export NEO4J_ACCEPT_LICENSE_AGREEMENT=eval

echo "Start running" >> $LOG_FILE

yum update -y >> $LOG_FILE

yum install -y java-11-amazon-corretto-headless >> $LOG_FILE

yum install -y neo4j-enterprise-5.6.0-1.noarch >> $LOG_FILE

sed -i 's/#dbms.default_listen_address=0.0.0.0/dbms.default_listen_address=0.0.0.0/g' /etc/neo4j/neo4j.conf
sed -i 's/#server.default_listen_address=0.0.0.0/server.default_listen_address=0.0.0.0/g' /etc/neo4j/neo4j.conf

sed -i 's/#server.http.enabled=true/server.http.enabled=true/g' /etc/neo4j/neo4j.conf
sed -i 's/#server.http.listen_address=:7474/server.http.listen_address=:7474/g' /etc/neo4j/neo4j.conf
sed -i 's/#server.http.advertised_address=:7474/server.http.advertised_address=:7474/g' /etc/neo4j/neo4j.conf

sed -i 's/#dbms.connector.bolt.enabled=true/dbms.connector.bolt.enabled=true/g' /etc/neo4j/neo4j.conf
sed -i 's/#dbms.connector.bolt.tls_level=DISABLED/dbms.connector.bolt.tls_level=DISABLED/g' /etc/neo4j/neo4j.conf
sed -i 's/#dbms.connector.bolt.listen_address=:7687/dbms.connector.bolt.listen_address=:7687/g' /etc/neo4j/neo4j.conf
sed -i 's/#dbms.connector.bolt.advertised_address=:7687/dbms.connector.bolt.advertised_address=:7687/g' /etc/neo4j/neo4j.conf

sed -i 's/#dbms.logs.http.enabled=true/dbms.logs.http.enabled=true/g' /etc/neo4j/neo4j.conf
sed -i 's/#dbms.security.allow_csv_import_from_file_urls=true/dbms.security.allow_csv_import_from_file_urls=true/g' /etc/neo4j/neo4j.conf

wget https://github.com/neo4j/graph-data-science/releases/download/2.3.2/neo4j-graph-data-science-2.3.2.jar  -P /var/lib/neo4j/plugins/

echo 'dbms.security.procedures.unrestricted=gds.*' | sudo tee -a /etc/neo4j/neo4j.conf
echo 'dbms.security.procedures.allowlist=gds.*' | sudo tee -a /etc/neo4j/neo4j.conf

wget https://neo4jdatacs4296.s3.amazonaws.com/neo4j.dump -P /var/lib/neo4j/import

neo4j-admin database load --from-path=/var/lib/neo4j/import neo4j --overwrite-destination=true

neo4j-admin database migrate neo4j --force-btree-indexes-to-range

chown -R neo4j:neo4j /var/lib/neo4j/data/

systemctl start neo4j >> $LOG_FILE

echo "Script completed successfully" >> $LOG_FILE