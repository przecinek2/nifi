#!/bin/bash

echo "Wybierz opcję:"
select opcja in "NiFi" "Elastisearch" "Elastisearch+Kibana" "NiFi+Elastisearch+Kibana" "Wyjście"; do
    case $opcja in
        "NiFi")
            wget https://raw.githubusercontent.com/przecinek2/ansible/main/NiFi/docker-compose.yml
            wget https://raw.githubusercontent.com/przecinek2/ansible/main/NiFi/docker_nifi.yml
            wget https://raw.githubusercontent.com/przecinek2/ansible/main/NiFi/inventory
            ;;
        "Elastisearch")
            
            ;;
        "Elastisearch+Kibana")
            wget https://raw.githubusercontent.com/przecinek2/ansible/main/elasticsearch%2Bkibana/docker-compose.yml
            wget https://raw.githubusercontent.com/przecinek2/ansible/main/elasticsearch%2Bkibana/docker-_elastisearch_kibana.yml
            wget https://raw.githubusercontent.com/przecinek2/ansible/main/elasticsearch%2Bkibana/inventoy
            ;;
        "NiFi+Elastisearch+Kibana")
            
            ;;
        "Wyjście")
            echo "Kończę skrypt."
            break
            ;;
        *)
            echo "Nieprawidłowa opcja."
            ;;
    esac
done
