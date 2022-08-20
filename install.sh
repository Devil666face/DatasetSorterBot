#!/bin/bash
echo Укажите путь к текущей директории. Пример /home/king/pythonProject/DatasetSorterBot/
read dir_name
cd $dir_name
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt