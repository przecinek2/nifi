import os
import json
import xmltodict

# Ścieżka do folderu z plikami XML
folder_path = "/media/sf_Downloads/2025_TEOS_XML_01A"  # ← zmień na nazwę swojego folderu

# Upewnij się, że folder istnieje
if not os.path.exists(folder_path):
    print(f"❌ Folder '{folder_path}' nie istnieje.")
    exit()

# Przechodzimy przez wszystkie pliki XML w folderze
for filename in os.listdir(folder_path):
    if filename.lower().endswith(".xml"):
        xml_file_path = os.path.join(folder_path, filename)
        json_file_path = os.path.join(folder_path, filename.replace(".xml", ".json"))

        try:
            with open(xml_file_path, "r", encoding="utf-8") as xml_file:
                xml_content = xml_file.read()
                data_dict = xmltodict.parse(xml_content)

            with open(json_file_path, "w", encoding="utf-8") as json_file:
                json.dump(data_dict, json_file, indent=2, ensure_ascii=False)

            print(f"✅ Skonwertowano: {filename} → {os.path.basename(json_file_path)}")

        except Exception as e:
            print(f"❌ Błąd przy pliku {filename}: {e}")
