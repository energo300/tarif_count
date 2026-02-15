# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# """
# Ядро
# Универсальный менеджер потоков и ошибок.
# Универсальный код, который берет любую функцию и запускает её безопасно.
# """
#
# import threading
# import queue
# import tkinter as tk
# from tkinter import ttk, messagebox
# import logger
# import progress_manager
#
# comm_queue = queue.Queue()
# is_running = False
# stop_event = threading.Event() # Флаг для сигнализации об остановке
#
#
# def abort_process(root):
#     """Функция для кнопки СТОП."""
#     if is_running:
#         request_stop()
#         log_to_ui("Запрос на остановку отправлен пользователем...", "error")
#         # Не дожидаясь монитора, сразу разблокируем кнопки через небольшую паузу
#         root.after(500, lambda: finalize_abort(root))
#
# def finalize_abort(root):
#     """Очистка UI после остановки."""
#     global is_running
#     is_running = False
#     set_gui_state(root, tk.NORMAL)
#     if progress_manager.progress_bus:
#         progress_manager.progress_bus.draw_error_strip() # Красим полосу красным
#     log_to_ui("Процесс принудительно прерван.", "error")
#
#
# def log_to_ui(msg, status=None):
#     comm_queue.put(("LOG", (msg, status)))
#
# def update_progress(it, tot, suf=''):
#     comm_queue.put(("PROGRESS", (it, tot, suf)))
#
# def request_stop():
#     """Сигнал всем функциям: пора закругляться."""
#     stop_event.set()
#
# def run_in_thread(root, task_func):
#     global is_running
#     stop_event.clear() # Сбрасываем флаг перед началом
#     is_running = True
#     set_gui_state(root, tk.DISABLED)
#
#     def worker():
#         global is_running
#         try:
#             res = task_func()
#             if not stop_event.is_set():
#                 comm_queue.put(("SUCCESS", res))
#         except Exception as e:
#             comm_queue.put(("ERROR", str(e)))
#         finally:
#             is_running = False
#
#     threading.Thread(target=worker, daemon=True).start()
#     _monitor(root)
#
#
# def log_to_ui(msg, status=None):
#     comm_queue.put(("LOG", (msg, status)))
#
#
# def update_progress(it, tot, suf=''):
#     comm_queue.put(("PROGRESS", (it, tot, suf)))
#
#
#
# def set_gui_state(container, state):
#     """Рекурсивно блокирует/разблокирует кнопки и чекбоксы."""
#     for child in container.winfo_children():
#         # Проверяем на стандартные кнопки и чекбоксы, а также на TTK аналоги
#         if isinstance(child, (tk.Button, tk.Checkbutton, ttk.Button, ttk.Checkbutton)):
#             child.configure(state=state)
#         elif child.winfo_children():
#             set_gui_state(child, state)
#
#
#
# def run_in_thread(root, task_func):
#     """Запуск фоновой задачи с блокировкой UI."""
#     set_gui_state(root, tk.DISABLED) # Блокируем всё
#
#     def worker():
#         try:
#             res = task_func()
#             comm_queue.put(("SUCCESS", res))
#         except Exception as e:
#             comm_queue.put(("ERROR", str(e)))
#
#     threading.Thread(target=worker, daemon=True).start()
#     _monitor(root)
#
#
#
#
# def _monitor(root):
#     try:
#         while True:
#             m_type, content = comm_queue.get_nowait()
#
#             if m_type == "LOG":
#                 msg, status = content
#                 logger.write_log(msg, status)
#
#             elif m_type == "PROGRESS":
#                 if progress_manager.progress_bus:
#                     progress_manager.progress_bus.update(*content)
#
#             elif m_type == "ERROR":
#                 if progress_manager.progress_bus:
#                     progress_manager.progress_bus.draw_error_strip()
#                 logger.write_log(content, "error")
#                 set_gui_state(root, tk.NORMAL) # Разблокируем всё
#                 return
#
#             elif m_type == "SUCCESS":
#                 logger.write_log(f"Завершено: {content}", "success")
#                 set_gui_state(root, tk.NORMAL) # Разблокируем всё
#                 return
#
#     except queue.Empty:
#         root.after(100, lambda: _monitor(root))


import threading
import queue
import tkinter as tk
from tkinter import ttk, messagebox
import logger
import progress_manager

# Очередь для безопасной связи фонового потока с основным окном
comm_queue = queue.Queue()
is_running = False
stop_event = threading.Event() # Флаг для сигнализации об остановке


def abort_process(root):
    """Функция для кнопки СТОП."""
    print("""Функция для кнопки СТОП.""")
    if is_running:
        request_stop()
        log_to_ui("Запрос на остановку отправлен пользователем...", "error")
        # Не дожидаясь монитора, сразу разблокируем кнопки через небольшую паузу
        root.after(500, lambda: finalize_abort(root))


def finalize_abort(root):
    """Очистка UI после остановки."""
    global is_running
    is_running = False
    set_gui_state(root, tk.NORMAL)
    if progress_manager.progress_bus:
        progress_manager.progress_bus.draw_error_strip() # Красим полосу красным
    log_to_ui("Процесс принудительно прерван.", "error")

def request_stop():
    """Сигнал всем функциям: пора закругляться."""
    stop_event.set()

def log_to_ui(msg, status=None):
    """Отправка сообщения в логгер (вызывается из задач)."""
    comm_queue.put(("LOG", (msg, status)))

def update_progress(it, tot, suf=''):
    """Обновление текстового прогресс-бара (вызывается из задач)."""
    comm_queue.put(("PROGRESS", (it, tot, suf)))

def set_gui_state(container, state, exclude=None):
    """
    Рекурсивно меняет состояние элементов.
    :param container: Корневой элемент (root или frame)
    :param state: tk.DISABLED или tk.NORMAL
    :param exclude: Список виджетов, которые ТРОГАТЬ НЕ НУЖНО
    """
    if exclude is None:
        exclude = []

    for child in container.winfo_children():
        # Если виджет в списке исключений — игнорируем его
        if child in exclude:
            continue

        # Блокируем стандартные и ttk элементы управления
        if isinstance(child, (tk.Button, tk.Checkbutton, ttk.Button, ttk.Checkbutton)):
            try:
                child.configure(state=state)
            except tk.TclError:
                pass # На случай, если виджет не поддерживает state

        # Если у элемента есть дочерние (Frame, LabelFrame) — идем внутрь
        elif child.winfo_children():
            set_gui_state(child, state, exclude)

def run_in_thread(root, task_func, keep_enabled=None):
    """
    Запуск фонового потока с блокировкой интерфейса.
    :param keep_enabled: список виджетов, остающихся активными (например, кнопка Quit).
    """
    # 1. Блокируем всё, кроме исключений
    set_gui_state(root, tk.DISABLED, exclude=keep_enabled)

    def worker():
        try:
            # Выполняем цепочку функций (workflow)
            res = task_func()
            # Если всё успешно — отправляем результат
            comm_queue.put(("SUCCESS", res))
        except Exception as e:
            # При любой ошибке в потоке — отправляем её текст для Traceback
            comm_queue.put(("ERROR", str(e)))

    # Запускаем поток как daemon, чтобы он закрылся при выходе из программы
    threading.Thread(target=worker, daemon=True).start()

    # Начинаем мониторинг очереди в основном потоке
    # _monitor(root)
    _monitor(root, keep_enabled)


def _monitor(root, keep_enabled):
    """Проверка очереди сообщений каждые 100 мс."""
    try:
        while True:
            # Пытаемся забрать сообщение без ожидания
            m_type, content = comm_queue.get_nowait()

            # При завершении или ошибке возвращаем всё в NORMAL
            if m_type in ("SUCCESS", "ERROR"):
                if m_type == "ERROR":
                    if progress_manager.progress_bus:
                        progress_manager.progress_bus.draw_error_strip()
                    logger.write_log(content, "error")

                set_gui_state(root, tk.NORMAL) # Разблокируем всё
                return

            if m_type == "LOG":
                msg, status = content
                logger.write_log(msg, status)

            elif m_type == "PROGRESS":
                if progress_manager.progress_bus:
                    progress_manager.progress_bus.update(*content)

            elif m_type == "ERROR":
                # Отрисовка сломанного бара (красным)
                if progress_manager.progress_bus:
                    progress_manager.progress_bus.draw_error_strip()

                # Вывод ошибки через ваш логгер с Traceback
                logger.write_log(content, "error")

                # Разблокируем интерфейс
                set_gui_state(root, tk.NORMAL)
                return

            elif m_type == "SUCCESS":
                # Успешное завершение
                logger.write_log(f"Завершено: {content}", "success")

                # Разблокируем интерфейс
                set_gui_state(root, tk.NORMAL)
                return

    except queue.Empty:
        # Если очередь пуста, планируем следующую проверку через 100 мс
        # root.after(100, lambda: _monitor(root))
        root.after(100, lambda: _monitor(root, keep_enabled))
