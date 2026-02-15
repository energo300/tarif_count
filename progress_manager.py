#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Менеджер прогресс-бара
"""

import time
import tkinter as tk
import logger
from mod import config


class TextProgressBar:
    def __init__(self, log_widget):
        self.log_widget = log_widget
        self.last_percent = -1
        self.start_time = None
        self.length = 40
        self.fill, self.empty, self.error_fill = '▓', '░', '▓'  # ░  ▚ ▓

    def reset(self):
        self.last_percent = -1
        self.start_time = None

    def draw_error_strip(self):
        if not self.log_widget or "progress_start" not in self.log_widget.mark_names(): return
        self.log_widget.config(state='normal')

        percent = max(0, self.last_percent)
        filled_len = int(self.length * percent // 100)

        self.log_widget.delete("progress_start", "end-1c")
        prefix = logger.get_timer()

        self.log_widget.insert('end', f"[{prefix}] │", "TIME")
        self.log_widget.insert('end', self.fill * filled_len, "success")
        self.log_widget.insert('end', self.error_fill * (self.length - filled_len), "error")
        self.log_widget.insert('end', f"│ {percent:3.0f}% [ERROR]", "error")
        # self.log_widget.insert('end', f"│ {percent:3.0f}% [ПРЕРВАНО]", "error")
        self.log_widget.insert('end', '\n')

        self.log_widget.mark_unset("progress_start")
        self.log_widget.config(state='disabled')
        self.reset()

    def update(self, iteration, total, suffix=''):
        if not self.log_widget or total <= 0: return
        # if self.start_time is None: self.start_time = time.time()
        # Синхронизируем старт прогресс-бара с конфигом
        if self.start_time is None or self.start_time != config.START_TIME:
            self.start_time = config.START_TIME

        percent_val = 100 * (iteration / float(total))
        self.last_percent = percent_val

        if 1 < iteration < total and abs(percent_val - getattr(self, '_prev_p', -1)) < 0.5: return
        self._prev_p = percent_val

        elapsed = time.time() - self.start_time
        speed = iteration / elapsed if elapsed > 0 else 0
        ete = int((total - iteration) / speed) if speed > 0 else 0
        h_e, r_e = divmod(ete, 3600); m_e, s_e = divmod(r_e, 60)

        prefix = logger.get_timer()
        self.log_widget.config(state='normal')

        if "progress_start" not in self.log_widget.mark_names():
            if suffix: self.log_widget.insert('end', f"[{prefix}] {suffix}\n", "info")
            self.log_widget.insert('end', '\n')
            self.log_widget.mark_set("progress_start", "end-2c linestart")
            self.log_widget.mark_gravity("progress_start", "left")
        else:
            self.log_widget.delete("progress_start", "end-1c")

        filled_len = int(self.length * iteration // total)
        self.log_widget.insert('end', f"[{prefix}] │", "TIME")
        self.log_widget.insert('end', self.fill * filled_len, "success")
        self.log_widget.insert('end', self.empty * (self.length - filled_len), "TIME")
        self.log_widget.insert('end', f"│ {percent_val:3.0f}%", "warning")
        self.log_widget.insert('end', f" ETE: {h_e:02d}:{m_e:02d}:{s_e:02d} ({speed:.1f} it/s)", "info")

        if iteration >= total:
            self.log_widget.insert('end', '\n')
            self.log_widget.mark_unset("progress_start")
            self.reset()

        self.log_widget.see('end')
        self.log_widget.config(state='disabled')

progress_bus = None

def init_progress(widget):
    global progress_bus
    progress_bus = TextProgressBar(widget)
