import gzip
import json

def extract_related(input_path, output_path):
    with gzip.open(input_path, 'rt', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        count = 0
        for line_num, line in enumerate(infile, start=1):
            try:
                item = json.loads(line)
                if 'related' in item and item['related']:
                    outfile.write(json.dumps(item) + '\n')
                    count += 1
                    if count % 1000 == 0:
                        print(f"✅ {count} προϊόντα αποθηκεύτηκαν (γραμμή {line_num})")
            except json.JSONDecodeError:
                print(f"❌ JSON σφάλμα στη γραμμή {line_num}")
                continue

        print(f"\n🎉 Ολοκληρώθηκε! Συνολικά αποθηκεύτηκαν {count} προϊόντα στο {output_path}")

# Εκτέλεση
extract_related("meta_Electronics.json.gz", "related_products.jsonl")
