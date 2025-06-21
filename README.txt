Οδηγίες Χρήσης


Για την εκτέλεση του κύριου προγράμματος: 

1. Τοποθετήστε τα παρακάτω αρχεία στον ίδιο φάκελο με το πρόγραμμα amazon_analysis.py:
   - related_products.txt (παραγόμενο από το προηγούμενο φίλτρο)
   - Electronics_5.json.gz (το αρχείο πωλήσεων)

2. Εκτελέστε το πρόγραμμα με την εντολή:
   python amazon_analysis.py

3. Θα δημιουργηθούν δύο αρχεία:
   - electronics_with_relationships.csv (αναλυτικά δεδομένα ανά προϊόν)
   - relationship_summary.csv (σύνοψη κερδών και πωλήσεων ανά τύπο σχέσης)


Για τη δημιουργία του related_products.txt:

1. Τοποθετήστε το αρχείο meta_Electronics.json στον ίδιο φάκελο με το extract_related_python.py.

2. Εκτελέστε το πρόγραμμα με την εντολή: 
   python extract_related_python.py

3. Θα δημιουργηθεί ένα αρχείο: related_products.txt

