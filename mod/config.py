#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Конфигурация приложения
"""
import os
import time
from pathlib import Path
START_TIME: float = time.time()  # запуск таймера


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def reset_time():
    """Сброс времени консоли и логов"""
    global START_TIME
    START_TIME = time.time()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Имя базы данных
DB_NAME = "database.db"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
NAM_PROG = "Inary Eye"
VER_PROG = "0.03"
AUTOR = "© 2026 Преснов С.В."
MAIL = "e-mail: energo300@gmail.com"
PHONE = "phone: +7 961-676-94-43"
JOB = "Ведущий инженер-энергетик СГЭ"
COM = "ООО «Концессии теплоснабжения»"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Список каталогов для поиска
PRICES_DIR = "prices"
SBYT_PRICES_DIR = "sbyt"
SETI_PRICES_DIR = "seti"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CHASY_DIR = "chasy"
SBYT_CHASY_DIR = "sbyt"
SETI_CHASY_DIR = "seti"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PROFILES_DIR = "profiles"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DATA_DIR = "data"
DATA_POWER_FILE = "Power.xlsx"
DATA_BAD_PROF_FILE = "Bad_profile.xlsx"
DATA_IGNOR_LIST_FILE = "Ignor_list.xlsx"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DIRECTORIES = [PRICES_DIR, CHASY_DIR, PROFILES_DIR]

# Расширение файла для поиска
FILE_EXTENSION = '.xlsx'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ICO_FILE = "icon.ico"
ROOT_DIR = os.path.join(os.getcwd(), '')  # текущий каталог
ICON_PATH = os.path.join(ROOT_DIR, ICO_FILE)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
BASE_DIR = Path(__file__).resolve().parent  # Директория, где лежит config.py
LOG_FILE = BASE_DIR.parent / "app_history.log"  # Поднимаемся на один уровень выше (../) и добавляем имя файла
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




if __name__ == "__main__":
    print("Это вызываемый модуль!")
