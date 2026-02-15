#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Логгер
"""
import tkinter as tk
import time
import sys
import logging
import traceback
from tkinter import messagebox
import mod.config as config
from mod.config import LOG_FILE


# Инициализация стандартного логгера для записи в файл
logger_file = logging.getLogger("AppLogger")
logger_file.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(message)s'))
logger_file.addHandler(file_handler)

_display_widget = None
_status_label = None
_root = None

def save_full_log():
    """Принудительное сохранение всего текста из UI в файл."""
    if _display_widget:
        try:
            full_content = _display_widget.get("1.0", tk.END)
            with open(LOG_FILE, 'w', encoding='utf-8') as f:
                f.write(full_content)
            # Опционально: выводим в консоль для подтверждения
            print(f"Лог успешно сохранен в {LOG_FILE}")
        except Exception as e:
            print(f"Ошибка при финальном сохранении лога: {e}")


def get_timer():
    """Расчет времени HH:MM:SS.mmm относительно START_TIME из config"""
    # Берем время напрямую из модуля config
    elapsed = time.time() - config.START_TIME
    total_seconds = int(elapsed)
    ms = int((elapsed - total_seconds) * 1000)
    m, s = divmod(total_seconds, 60)
    h, m = divmod(m, 60)

    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

def init_logger(widgets_dict):
    """Инициализация тегов и ссылок на виджеты"""
    global _display_widget, _status_label, _root
    _display_widget = widgets_dict.get('log_area')
    _status_label = widgets_dict.get('status_label_1')
    _root = widgets_dict.get('root')

    if not _display_widget: return

    log_font = ("Consolas", 12)
    _display_widget.config(font=log_font, state='normal')
    _display_widget.delete('1.0', tk.END)

    # Ваша цветовая палитра
    tags = {
        "error": "#FF5252",
        "success": "#4CAF50",
        "warning": "#FFD740",
        "debug": "#757575",
        "valid": "#40C4FF",
        "info": "#40C4FF",
        "ok": "#4CAF50",
        "head": "#40C4FF",
        "but": "#ffff00",
        "fix": "#f600ff"
    }
    for tag, color in tags.items():
        _display_widget.tag_config(tag, foreground=color, font=log_font)

    _display_widget.tag_config("TIME", foreground="gray", font=log_font)
    _display_widget.tag_config("progress_theme", foreground="#FF9800", font=log_font)

    _display_widget.config(state='disabled')

def write_log(message, status=None):
    """Основная функция вывода лога (ваша логика log_mess)"""
    if not _display_widget: return

    status_config = {
        "error": (" ERROR ", "error"),
        "success": ("SUCCESS", "success"),
        "warning": ("WARNING", "warning"),
        "debug": (" DEBUG ", "debug"),
        "valid": (" VALID ", "valid"),
        "info": (" INFO  ", "info"),
        "ok": ("  OK   ", "ok"),
        "head": (" HEAD  ", "info"),
        "but": ("  BUT  ", "but"),
        "fix": ("  FIX  ", "fix")
    }

    current_time = get_timer()
    display_text, tag = status_config.get(status, ("", None))

    _display_widget.config(state='normal')

    if status == 'error':
        if _status_label: _status_label.config(text="ОШИБКА", foreground='#900100')

        # Traceback
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb_details = "".join(traceback.format_exception(exc_type, exc_value, exc_tb)) if exc_type else ""

        _display_widget.insert('end', f"[{current_time}] ", "TIME")
        _display_widget.insert('end', f"[{display_text}] {message}\n", tag)
        if tb_details:
            _display_widget.insert('end', f"\n--- СИСТЕМНЫЙ TRACEBACK ---\n{tb_details}\n", "debug")

        # Сохранение лога при краше
        full_content = _display_widget.get("1.0", "end-1c")
        with open(LOG_FILE, 'w', encoding='utf-8') as f: f.write(full_content)

        _display_widget.see('end')
        _display_widget.config(state='disabled')
        if _root:
            _root.update_idletasks()
            messagebox.showerror(" System Crash ", f"{message}", parent=_root)
        return

    # Обычный вывод
    if _status_label: _status_label.config(text=message, foreground='#000000')

    _display_widget.insert('end', f"[{current_time}] ", "TIME")

    if display_text:
        if status not in ("head", "but"):
            _display_widget.insert('end', f"[{display_text}] ", tag)

        msg_tag = tag if status in ["success","warning","fix","head","but","info"] else None
        _display_widget.insert('end', f"{message}\n", msg_tag)

        log_line = f"{current_time} [{display_text}] {message}" if status not in ("head", "but") else f"{current_time} {message}"
        logger_file.info(log_line)
    else:
        _display_widget.insert('end', f"{message}\n")
        logger_file.info(f"{current_time} {message}")

    _display_widget.see('end')
    _display_widget.config(state='disabled')


