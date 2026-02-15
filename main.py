#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Точка входа, создание окна Tkinter
Файл для запуска приложения.
………………………………………………………… … … … … … … … … …
"""
import base64
import os
import time
import tkinter as tk

from PIL import ImageTk

import logger
import mod.config as config
from mod.big_logo import BIG_LOGO
from mod.config import ICON_PATH
from mod.config import NAM_PROG, VER_PROG, AUTOR
from mod.icon import ICON
from mod.pre_start_tasks import run_pre_start_tasks
from ui import create_ui, SplashScreen


# ==============================================
# def run_pre_start_tasks(splash):
#     """Задачи запуска с выводом в Splash и в основной Лог"""
#
#     tasks = [
#         ("Инициализация:", "Проверка путей...", "success"),
#         ("Загрузка:", "База данных SQLite...", "info"),
#         ("Конфигурация:", "Чтение настроек...", "ok"),
#         ("Завершение:", "Подготовка интерфейса...", "success")
#     ]
#
#     for info, subinfo, status in tasks:
#         # 1. Обновляем текст на Сплэше
#         splash.set_text(info, subinfo)
#
#         # 2. Пишем в основной лог (который пока скрыт вместе с root)
#         # Используем ваши статусы (info, success, ok и т.д.)
#         logger.write_log(f"{info} {subinfo}", status)
#         # Здесь может быть реальный код, например:
#         # database.connect() или os.makedirs(...)
#         # Имитация работы
#         time.sleep(0.6)
# ==============================================


if __name__ == "__main__":
    root = tk.Tk()
    root.title(f"{NAM_PROG} {VER_PROG}")
    try:
        if os.name == 'nt':
            # Для Windows лучше всего работает .ico файл
            if os.path.exists(ICON_PATH):
                root.iconbitmap(ICON_PATH)
            else:
                # Если файла нет, используем данные из переменной ICON
                icon_bytes = base64.b64decode(ICON)
                img = ImageTk.PhotoImage(data=icon_bytes)
                root.iconphoto(True, img)
        else:
            # Для Linux/macOS используем iconphoto
            icon_bytes = base64.b64decode(ICON)
            # Сохраняем ссылку на объект img в root, чтобы его не удалил garbage collector
            root._icon_img = ImageTk.PhotoImage(data=icon_bytes)
            root.iconphoto(True, root._icon_img)
    except Exception as e:
        print(f"Не удалось установить иконку: {e}")




    # Скрываем основное окно
    root.withdraw()
    # 2. Создаем и показываем Splash
    splash = SplashScreen(root, NAM_PROG, VER_PROG, BIG_LOGO, ICON, AUTOR, config)

    # 2. Инициализируем интерфейс (создаем лог-зону и настраиваем logger)
    # Теперь logger.write_log готов к работе!
    create_ui(root)

    # 3. Выполняем задачи (они полетят и в Splash, и в Log)
    run_pre_start_tasks(splash)


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    root.geometry("1600x700")
    # Настройка минимального размера окна, чтобы элементы не пропадали
    root.minsize(1200, 500)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 5. Закрываем Splash и "проявляем" основное окно
    splash.destroy()
    root.deiconify() # Показываем основное окно
    root.mainloop()

# if __name__ == "__main__":
#     root = tk.Tk()
#     root.withdraw() # Прячем основное окно
#
#     # 1. Создаем Splash
#     splash = SplashScreen(root, NAM_PROG, VER_PROG, BIG_LOGO, ICON, AUTOR, config)
#
#     # 2. Инициализируем интерфейс (создаем лог-зону и настраиваем logger)
#     create_ui(root)
#
#     # 3. Выполняем проверку. Если вернуло False (ошибка) — выходим
#     if run_pre_start_tasks(splash):
#         time.sleep(0.5) # Пауза, чтобы успеть прочитать "Готово"
#         splash.destroy()
#         root.deiconify() # Показываем основное окно
#         root.mainloop()
#     else:
#         # Если была критическая ошибка, logger уже показал messagebox
#         root.destroy()
