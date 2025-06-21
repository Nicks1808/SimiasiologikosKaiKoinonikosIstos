import pandas as pd

# Φόρτωση του JSON Lines αρχείου
df = pd.read_json("meta_Electronics.json", lines=True)

# Έλεγχος αν υπάρχει η στήλη 'related'
if 'related' in df.columns:
    related_products = df[df['related'].notnull()]

    if not related_products.empty:
        for index, row in related_products.head(5).iterrows():
            print("ASIN:", row.get("asin"))
            print("Related keys:", list(row["related"].keys()))
            print("Sample related ASINs:", row["related"])
            print("-" * 50)
    else:
        print("Υπάρχει στήλη 'related', αλλά δεν υπάρχουν γραμμές με τιμές.")
else:
    print("Δεν υπάρχει στήλη 'related' στο dataset.")
