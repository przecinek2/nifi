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
            wget https://raw.githubusercontent.com/przecinek2/ansible/main/Elasticsearch
            wget https://raw.githubusercontent.com/przecinek2/ansible/main/Elasticsearch
            wget https://raw.githubusercontent.com/przecinek2/ansible/main/Elasticsearch
            ;;
        "Elastisearch+Kibana")
            wget https://raw.githubusercontent.com/przecinek2/ansible/main/Elasticsearch%2BKibana/docker-compose.yml
            wget https://raw.githubusercontent.com/przecinek2/ansible/main/Elasticsearch%2BKibana/docker_elastisearch_kibana.yml
            wget https://raw.githubusercontent.com/przecinek2/ansible/main/Elasticsearch%2BKibana/inventory
            ;;
        "NiFi+Elastisearch+Kibana")
            wget https://raw.githubusercontent.com/przecinek2/ansible/main/NiFi%2BElasticsearch%2BKibana/docker_nifi_elastcsearch_kibana.yml
            wget https://raw.githubusercontent.com/przecinek2/ansible/main/NiFi%2BElasticsearch%2BKibana/invetnory
            wget https://raw.githubusercontent.com/przecinek2/ansible/main/NiFi%2BElasticsearch%2BKibana/docker-compose.yml
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
