import gzip
import json

def find_related_products(path, compressed=True, limit=20):
    open_fn = gzip.open if compressed else open

    count = 0
    with open_fn(path, 'rt', encoding='utf-8') as f:
        for line_num, line in enumerate(f, start=1):
            try:
                item = json.loads(line)

                if 'related' in item:
                    print(f"✅ FOUND on line {line_num} | ASIN:", item.get("asin"))
                    print("Related keys:", list(item["related"].keys()))
                    print("Sample related ASINs:", item["related"])
                    print("-" * 60)
                    count += 1
                    if count >= limit:
                        break
                else:
                    print(f"⛔ NO 'related' on line {line_num}")

            except json.JSONDecodeError:
                print(f"❌ JSON error on line {line_num}")
                continue

# Τρέχουμε με το .gz για μεγαλύτερη ταχύτητα και αποδοτικότητα
find_related_products("meta_Electronics.json.gz", compressed=True, limit=20)
