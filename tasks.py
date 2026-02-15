#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Логика
"""

import time

import logger
from engine import log_to_ui, update_progress
import mod.config as config


# def func100():
#     log_to_ui("ЗАГРУЗКА БАЗЫ ДАННЫХ", "head")
#     for i in range(1, 101):
#         time.sleep(0.02)
#         update_progress(i, 100, "Чтение секторов…")
#     log_to_ui("База загружена успешно", "ok")
#     return "DB_READY"
#
# def func200(data):
#     log_to_ui(f"АНАЛИЗ ПАКЕТА: {data}", "head")
#     log_to_ui("Обнаружены несоответствия в заголовках", "but")
#     time.sleep(0.5)
#     log_to_ui("Применяю автоматическое исправление", "fix")
#
#     for i in range(1, 101):
#         time.sleep(0.03)
#         update_progress(i, 100, "Глубокое сканирование…")
#         if i == 65: raise RuntimeError("Обнаружено повреждение данных!")
#     return "Анализ завершен"

import time
from engine import log_to_ui, update_progress, stop_event

def func100():
    log_to_ui("Запуск 100", "head")
    for i in range(1, 101):
        if stop_event.is_set(): return "STOPPED" # Выход из цикла при стопе
        time.sleep(0.15)
        update_progress(i, 100, "Работа 100")
    return "Data100"


def func200(data):
    if data == "STOPPED": return "STOPPED"
    log_to_ui("Запуск 200", "head")
    for i in range(1, 101):
        if stop_event.is_set(): return "STOPPED"
        time.sleep(0.05)
        update_progress(i, 100, "Работа 200")
        if i == 65: raise RuntimeError("Обнаружено повреждение данных!")
    return "Анализ завершен"


def workflow_alpha():

    res = func100()
    # Если первая функция вернула сигнал остановки, не запускаем вторую
    if res == "STOPPED":
        log_to_ui("Цепочка прервана на первом этапе.", "debug")
        return "Aborted"

    return func200(res)

    # result = func100()
    # return func200(result)
