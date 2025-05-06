import os
 import json
 import xmltodict
 import requests

 # === KONFIGURACJA ===
 INPUT_DIR = '/media/sf_Downloads/2025_TEOS_XML_01A'  # <-- Zmień na swój katalog z XML
 ELASTIC_URL = 'http://localhost:9200'
 INDEX_NAME = 'zad_forma_990'  # <-- Zmień nazwę indeksu
 FULL_INDEX_URL = f'{ELASTIC_URL}/{INDEX_NAME}'
 HEADERS = {'Content-Type': 'application/json'}

 # === Mapping indeksu (dopasuj do struktury danych) ===
 INDEX_MAPPING = {
     "settings": {
         "number_of_shards": 1,
         "number_of_replicas": 0,
         "index.mapping.total_fields.limit": 50000  # <-- kluczowa linia
     },
     "mappings": {
         "properties": {
           "Return": {
             "properties": {
               "ReturnHeader": {
                 "properties": {
                   "ReturnTs": { "type": "date" },
                   "TaxPeriodBeginDt": { "type": "date" },
                   "TaxPeriodEndDt": { "type": "date" },
                   "ReturnTypeCd": { "type": "keyword" },
                   "TaxYr": { "type": "integer" },
                   "Filer": {
                     "properties": {
                       "EIN": { "type": "keyword" },
                       "BusinessName": {
                         "properties": {
                           "BusinessNameLine1Txt": { "type": "text" }
                         }
                       },
                       "USAddress": {
                         "properties": {
                           "AddressLine1Txt": { "type": "text" },
                           "CityNm": { "type": "keyword" },
                           "StateAbbreviationCd": { "type": "keyword" },
                           "ZIPCd": { "type": "keyword" }
                         }
                       }
                     }
                   }
                 }
               },
               "ReturnData": {
                 "properties": {
                   "IRS990EZ": {
                     "properties": {
                       "GrossReceiptsAmt": { "type": "float" },
                       "TotalRevenueAmt": { "type": "float" },
                       "TotalExpensesAmt": { "type": "float" },
                       "NetAssetsOrFundBalancesEOYAmt": { "type": "float" },
                       "OfficerDirectorTrusteeEmplGrp": {
                         "type": "nested",
                         "properties": {
                           "PersonNm": { "type": "text" },
                           "TitleTxt": { "type": "keyword" },
                           "AverageHrsPerWkDevotedToPosRt": { "type": "float" },
                           "CompensationAmt": { "type": "float" }
                         }
                       },
                       "PrimaryExemptPurposeTxt": { "type": "text" }
                     }
                   }
                 }
               }
             }
           }
         }
       }
 }  
 def create_index_if_not_exists():
     response = requests.head(FULL_INDEX_URL)
     if response.status_code == 404:
         print(f"🔧 Tworzenie indeksu: {INDEX_NAME}")
         res = requests.put(FULL_INDEX_URL, headers=HEADERS, json=INDEX_MAPPING)
         if res.status_code == 200:
             print(f"✔ Indeks {INDEX_NAME} został utworzony.")
         else:
             print(f"❌ Błąd tworzenia indeksu: {res.status_code} - {res.text}")
     elif response.status_code == 200:
         print(f"ℹ️ Indeks {INDEX_NAME} już istnieje.")
     else:
         print(f"❌ Błąd sprawdzania indeksu: {response.status_code} - {response.text}")

 def flatten_and_extract_attributes(obj):
     """
     Zamienia {"#text": X, "@attr": Y} na:
     - pole: X
     - pole_attr: Y
     """
     if isinstance(obj, dict):
         if "#text" in obj:
             result = flatten_and_extract_attributes(obj["#text"])
             for k, v in obj.items():
                 if k.startswith("@"):
                     result_key = f"{k[1:]}"  # np. "referenceDocumentId"
                     return {**{"value": result}, **{f"{result_key}": v}}
             return result
         else:
             new_obj = {}
             for k, v in obj.items():
                 flattened = flatten_and_extract_attributes(v)
                 if isinstance(flattened, dict) and "value" in flattened:
                     # wypłaszcz obiekt {"value": X, "ref": Y} na dwa klucze
                     new_obj[k] = flattened["value"]
                     for attr_key, attr_val in flattened.items():
                         if attr_key != "value":
                             new_obj[f"{k}_{attr_key}"] = attr_val
                 else:
                     new_obj[k] = flattened
             return new_obj
     elif isinstance(obj, list):
         return [flatten_and_extract_attributes(item) for item in obj]
     else:
         return obj

 def convert_xml_to_json(xml_file_path):
     with open(xml_file_path, 'r', encoding='utf-8') as file:
         try:
             xml_data = xmltodict.parse(file.read())
             return flatten_and_extract_attributes(xml_data)
         except Exception as e:
             print(f"❌ Błąd konwersji pliku {xml_file_path}: {e}")
             return None

 def send_to_elasticsearch(json_data, source_file):
     try:
         response = requests.post(f"{FULL_INDEX_URL}/_doc", headers=HEADERS, json=json_data)
         if response.status_code in [200, 201]:
             print(f"✔ Wysłano dane z pliku {source_file} do Elasticsearch")
         else:
             print(f"❌ Błąd wysyłki z pliku {source_file}: {response.status_code} - {response.text}")
     except Exception as e:
         print(f"❌ Wyjątek przy wysyłce z pliku {source_file}: {e}")

 def process_contractor_documents(json_data, source_file):
    contractor_path = json_data.get("Return", {}).get("ReturnData", {}).get("IRS990", {}).get("ContractorCompensationGrp")

    if isinstance(contractor_path, list):
        print(f"📂 Rozdzielam {len(contractor_path)} wpisów ContractorCompensationGrp...")
        for i, contractor in enumerate(contractor_path):
            doc = {
                "source_file": source_file,
                "contractor_index": i,
                "ContractorCompensationGrp": contractor
            }
            send_to_elasticsearch(doc, f"{source_file} [{i}]")
    else:
        send_to_elasticsearch(json_data, source_file)

 def main():
     if not os.path.isdir(INPUT_DIR):
         print(f"❌ Katalog nie istnieje: {INPUT_DIR}")
         return

     create_index_if_not_exists()

     for filename in os.listdir(INPUT_DIR):
         if filename.endswith('.xml'):
             full_path = os.path.join(INPUT_DIR, filename)
             print(f"🔄 Przetwarzanie: {filename}")
             json_data = convert_xml_to_json(full_path)
             if json_data:
                 process_contractor_documents(json_data, filename)

 if __name__ == '__main__':
     main()
