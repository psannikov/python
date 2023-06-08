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
# Работаем с файлом и записываем результат в базу
with zipfile.ZipFile(ZIP_PATH, 'r') as z:
    for file_name in z.namelist():
        if file_name.endswith('.json'):
            with z.open(file_name) as f:
                data = json.load(f)
                df = pd.DataFrame(data)
df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
conn.close()