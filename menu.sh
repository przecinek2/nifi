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
            wget https://raw.githubusercontent.com/przecinek2/ansible/main/
            wget https://raw.githubusercontent.com/przecinek2/ansible/main/
            wget https://raw.githubusercontent.com/przecinek2/ansible/main/
            ;;
        "Elastisearch+Kibana")
            
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
