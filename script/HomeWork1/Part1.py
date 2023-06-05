import pandas as pd
import zipfile
import json
import sqlite3

# Определяем константы
ZIP_PATH = 'okved_2.json.zip'
DB_NAME = 'hw1.db'
TABLE_NAME = 'okved'
# Определяем переменные и коннекты
df = pd.DataFrame
conn = sqlite3.connect(DB_NAME)
# Open the ZIP file
with zipfile.ZipFile(ZIP_PATH, 'r') as z:
    # Iterate over each file in the ZIP archive
    for file_name in z.namelist():
        # Check if the file is a JSON file
        if file_name.endswith('.json'):
            # Read the JSON file into a list of dictionaries
            with z.open(file_name) as f:
                data = json.load(f)
                # Create a pandas DataFrame from the JSON data
                df = pd.DataFrame(data)
                # Process the DataFrame as needed
# Insert the DataFrame data into the SQLite database
df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
# Close the database connection
conn.close()
