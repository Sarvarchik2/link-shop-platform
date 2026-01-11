import json
import glob

files = ['frontend/locales/ru.json', 'frontend/locales/uz.json', 'frontend/locales/en.json']

for file_path in files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"Fixed encoding for {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
