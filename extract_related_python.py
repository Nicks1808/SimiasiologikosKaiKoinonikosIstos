import ast

def extract_related(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        count = 0
        for line_num, line in enumerate(infile, start=1):
            try:
                item = ast.literal_eval(line)
                if 'related' in item and item['related']:
                    outfile.write(str(item) + '\n')  # Ή json.dumps() αν θέλεις JSON μορφή
                    count += 1
                    if count % 1000 == 0:
                        print(f"✅ {count} προϊόντα αποθηκεύτηκαν (γραμμή {line_num})")
            except (ValueError, SyntaxError):
                print(f"❌ Σφάλμα σε γραμμή {line_num}")
                continue

        print(f"\n🎉 Ολοκληρώθηκε! Συνολικά αποθηκεύτηκαν {count} προϊόντα στο {output_path}")

# Εκτέλεση
extract_related("meta_Electronics.json", "related_products.txt")
