import pandas as pd
import sqlite3
import os

def inject(file, db, name):
    conn = sqlite3.connect(db)

    # Insert data into the SQL table
    df = pd.read_csv(file)
    df.to_sql(name, conn, if_exists='replace', index=False)

    conn.close()

def main():
    # Read the CSV file
    csv_dir = r"C:\Users\ultro\OneDrive\Documents\GitHub\CSE_111_Project\archive"
    names = ['']
    db = r"C:\Users\ultro\OneDrive\Documents\GitHub\CSE_111_Project\Checkpoint2-database.sqlite3"
    
    for i in os.listdir(csv_dir):
        file = os.path.join(csv_dir, i)
        name = os.path.splitext(i)[0]
        inject(file, db, name)
    
main()
        
