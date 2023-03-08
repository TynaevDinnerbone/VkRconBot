@echo off
chcp 65001
cd rcon_bot
echo Установка виртуального окружения...
call python -m venv venv
call venv\Scripts\activate
echo Установка модулей и библиотек...
pip install -r modules.txt
echo Создание файлов...
python create_files.py
del modules.txt
cd ..
del installer.bat