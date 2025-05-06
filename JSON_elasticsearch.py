import os
import json
from elasticsearch import Elasticsearch

# Ustawienia
folder = "/media/sf_Downloads/2025_TEOS_XML_01A"
indeks = "teos-2025"

# Połączenie z Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Tworzenie indeksu jeśli nie istnieje
if not es.indices.exists(index=indeks):
    es.indices.create(index=indeks)
    print(f"Utworzono indeks: {indeks}")
# Iteracja po plikach JSON w folderze
for plik in os.listdir(folder):
    if plik.endswith(".json"):
        sciezka = os.path.join(folder, plik)
        try:
            with open(sciezka, "r", encoding="utf-8") as f:
                dokument = json.load(f)
                es.index(index=indeks, document=dokument)
                print(f"Załadowano: {plik}")
        except Exception as e:
            print(f"Błąd przy {plik}: {e}")

print("Import zakończony.")
