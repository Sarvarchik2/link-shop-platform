import json
import os

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def flatten_keys(data, parent_key='', sep='.'):
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_keys(v, new_key, sep=sep).items())
            items.append((new_key, "TYPE:OBJECT")) # Mark as object for type checking
        else:
            items.append((new_key, "TYPE:STRING"))
    return dict(items)

def compare_locales(base_path, target_path, base_name, target_name):
    print(f"\n--- Comparing {base_name} -> {target_name} ---")
    base_data = load_json(base_path)
    target_data = load_json(target_path)

    base_keys = flatten_keys(base_data)
    target_keys = flatten_keys(target_data)

    missing_keys = []
    type_mismatches = []

    for key, type_ in base_keys.items():
        if key not in target_keys:
            # Check if a parent key exists as a string in target (schema mismatch)
            # or if it's just missing
             missing_keys.append(key)
        else:
            if target_keys[key] != type_:
                type_mismatches.append(f"{key} (Base: {type_}, Target: {target_keys[key]})")
    
    if not missing_keys and not type_mismatches:
        print("No issues found!")
        return

    if missing_keys:
        print(f"\nMissing Keys ({len(missing_keys)}):")
        # heuristic: don't show children if parent is missing
        # actually, flatten_keys handles full paths, so we can see exactly what leaf is missing
        # But if a whole object is missing, we might see 100 missing keys. 
        # Let's just print them.
        for k in sorted(missing_keys):
            print(f"  [MISSING] {k}")

    if type_mismatches:
        print(f"\nType Mismatches ({len(type_mismatches)}):")
        for m in sorted(type_mismatches):
            print(f"  [MISMATCH] {m}")

def main():
    root_dir = '/Users/ula/Documents/link-shop-platform-1/frontend/locales'
    en_path = os.path.join(root_dir, 'en.json')
    uz_path = os.path.join(root_dir, 'uz.json')
    ru_path = os.path.join(root_dir, 'ru.json')

    if not os.path.exists(en_path):
        print("Error: en.json not found")
        return

    compare_locales(en_path, uz_path, 'English', 'Uzbek')
    compare_locales(en_path, ru_path, 'English', 'Russian')

if __name__ == "__main__":
    main()
