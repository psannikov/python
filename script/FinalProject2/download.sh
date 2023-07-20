#!/bin/sh

echo "Начало работы" 

dir="/home/psannikov/airflow/dags"
download_url="https://ofdata.ru/open-data/download/egrul.json.zip"
file_name="egrul.json.zip"

# Проверяем, существует ли файл

if [ -f "$dir/$file_name" ]; then

  echo "Файл уже существует."

else

  # Файла нет, запускаем закачку

  echo "Файл не найден. Закачиваем..."
  cd $dir
  wget $download_url 

fi
