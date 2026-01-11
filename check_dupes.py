import json
from collections import Counter

print("Starting checks...")

def check_dupes(pairs):
    keys = [k for k, v in pairs]
    counts = Counter(keys)
    dupes = [k for k, c in counts.items() if c > 1]
    if dupes:
        print(f"Duplicate keys found: {dupes}")
    return dict(pairs)

try:
    with open('frontend/locales/uz.json', 'r') as f:
        json.load(f, object_pairs_hook=check_dupes)
    print("uz.json checked.")
except Exception as e:
    print(f"Error: {e}")
