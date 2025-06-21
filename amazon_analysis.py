import json
import gzip
import ast
import pandas as pd
from collections import defaultdict

def parse_reviews(path):
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        for line in f:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue

def parse_related_products(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                yield ast.literal_eval(line)
            except Exception:
                continue

# === ΦΟΡΤΩΣΗ ΔΕΔΟΜΕΝΩΝ ===
print("🔍 Φόρτωση related προϊόντων...")
related_data = list(parse_related_products("related_products.txt"))
related_lookup = {item['asin']: item['related'] for item in related_data}
category_lookup = {item['asin']: item.get('categories', []) for item in related_data}

print("📦 Φόρτωση δεδομένων πωλήσεων...")
sales_data = list(parse_reviews("Electronics_5.json.gz"))
sales_lookup = defaultdict(list)
for item in sales_data:
    sales_lookup[item['asin']].append(item)

# === ΑΝΑΛΥΣΗ ===
print("📊 Ανάλυση σχέσεων προϊόντων...")
results = []
substitute_sales = 0
supplementary_sales = 0
substitute_revenue = 0.0
supplementary_revenue = 0.0
substitute_count = 0
supplementary_count = 0

for i, (asin, related) in enumerate(related_lookup.items(), start=1):
    if i % 1000 == 0:
        print(f"➡️ Επεξεργασία προϊόντος {i}/{len(related_lookup)}...")

    main_sales = sales_lookup.get(asin, [])
    main_categories = category_lookup.get(asin, [])
    if not main_categories:
        continue

    main_category_set = set(main_categories[0]) if main_categories else set()

    for rel_type, rel_asins in related.items():
        for rel_asin in rel_asins:
            rel_sales = sales_lookup.get(rel_asin, [])
            rel_categories = category_lookup.get(rel_asin, [])
            if not rel_categories:
                continue

            rel_category_set = set(rel_categories[0])
            relationship = "substitute" if rel_category_set == main_category_set else "supplementary"
            total_sales = len(rel_sales)
            revenue = sum(r.get("overall", 0) for r in rel_sales)  # proxy για έλλειψη τιμής

            results.append({
                "asin": rel_asin,
                "relationship": relationship,
                "revenue": revenue,
                "sales": total_sales
            })

            if relationship == "substitute":
                substitute_sales += total_sales
                substitute_revenue += revenue
                substitute_count += 1
            else:
                supplementary_sales += total_sales
                supplementary_revenue += revenue
                supplementary_count += 1

# === ΑΠΟΘΗΚΕΥΣΗ ===
print("💾 Αποθήκευση αποτελεσμάτων...")
df = pd.DataFrame(results)
df.to_csv("type_of_products.csv", index=False)

with open("electronics_summary.txt", "w", encoding="utf-8") as f:
    f.write(f"- Συνολικά υπήρχαν {substitute_count} υποκαταστάτα προϊόντα\n")
    f.write(f"- Συνολικά υπήρχαν {supplementary_count} συμπληρωματικά προϊόντα\n")
    f.write(f"- Συνολικά πωλήθηκαν {substitute_sales} υποκαταστάτα προϊόντα\n")
    f.write(f"- Συνολικά πωλήθηκαν {supplementary_sales} συμπληρωματικά προϊόντα\n")
    f.write(f"- Το συνολικό κέρδος σε $ από τα υποκατάστατα προϊόντα ήταν {substitute_revenue:.2f}\n")
    f.write(f"- Το συνολικό κέρδος σε $ από τα συμπληρωματικά προϊόντα ήταν {supplementary_revenue:.2f}\n\n")

    most_profitable = "υποκατάστατα" if substitute_revenue > supplementary_revenue else "συμπληρωματικά"
    f.write(f"➤ Συμφέρει περισσότερο να προτείνονται: {most_profitable} προϊόντα\n")

print("✅ Η ανάλυση ολοκληρώθηκε.")
