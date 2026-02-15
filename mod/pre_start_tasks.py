#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Первичная загрузка и проверка
"""
import time
from pathlib import Path

import logger
from mod import config
from mod.config import PROFILES_DIR, PRICES_DIR, CHASY_DIR, DATA_DIR


def run_pre_start_tasks(splash):
    """Проверка директорий и инициализация с выводом в Splash и Логгер"""

    # Список папок для проверки (названия из вашего интерфейса)
    folders = [
        ("Профили учета", PROFILES_DIR),
        ("Цены на энергию", PRICES_DIR),
        ("Часы пиковой мощности", CHASY_DIR),
        ("Дополнительные данные", DATA_DIR)
    ]

    config.reset_time()  # Сброс общего таймера

    logger.write_log("--- НАЧАЛО ИНИЦИАЛИЗАЦИИ СИСТЕМЫ ---", "head")
    base_path = Path(__file__).resolve().parent.parent

    for name, folder_name in folders:
        full_path = base_path / folder_name
        splash.set_text("Инициализация:", f"Проверка {name}...")
        time.sleep(0.3) # Для визуального отклика на Splash


        if full_path.exists():
            logger.write_log(f"Директория {name}: OK", "ok")
        else:
            try:
                full_path.mkdir(parents=True, exist_ok=True)
                logger.write_log(f"Директория {name}: СОЗДАНА", "fix")
            except Exception as e:
                # Это вызовет ваш системный Traceback и прервет запуск
                logger.write_log(f"Ошибка доступа к {name}: {e}", "error")
                return False # Сигнал к отмене запуска

    splash.set_text("Завершение:", "Подготовка интерфейса...")
    logger.write_log("Все компоненты системы проверены успешно", "success")
    time.sleep(1.3)
    return True