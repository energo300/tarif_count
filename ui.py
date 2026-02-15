import base64
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
import os
import platform as plt_module
import subprocess
import mod.config as config
import engine
import tasks
import logger
import progress_manager
from mod.big_logo import BIG_LOGO
from mod.config import NAM_PROG, VER_PROG, PROFILES_DIR, PRICES_DIR, CHASY_DIR, DATA_DIR, AUTOR, JOB


class SplashScreen(tk.Toplevel):
    def __init__(self, root, NAM_PROG, VER_PROG, BIG_LOGO, ICON, AUTOR, config_mod):
        super().__init__(root)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        # Константы
        BACKGROUND_COLOR = "#1a2835"
        FONT_15 = ('Noto Sans', 17)
        MAIN_FONT_11 = ('Noto Sans', 11)
        self.config(background=BACKGROUND_COLOR)
        if os.name == 'posix':
            self.wm_attributes("-type", "splash")
        # Геометрия
        w, h = 350, 650
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")
        # Ресурсы
        self.img_logo = tk.PhotoImage(data=BIG_LOGO)
        self.icon_data = tk.PhotoImage(data=ICON)
        # Виджеты
        opts = {"background": BACKGROUND_COLOR, "anchor": "center"}
        tk.Label(self, image=self.img_logo, **opts).pack(pady=(20, 0))
        tk.Label(self, text=f"{NAM_PROG} {VER_PROG}", font=FONT_15,
                 foreground="#cceeee", **opts).pack(pady=10)
        self.info_label = tk.Label(self, text="Loading…", font=MAIN_FONT_11,
                                   foreground="#ffc700", **opts)
        self.info_label.pack(padx=10)
        self.subinfo_label = tk.Label(self, text="", font=MAIN_FONT_11,
                                      foreground="#ffc700", **opts)
        self.subinfo_label.pack(padx=10)
        author_text = f"{AUTOR}\n{config_mod.MAIL}\n{config_mod.PHONE}\n{config_mod.JOB}\n{config_mod.COM}"
        tk.Label(self, text=author_text, font=('Noto Sans', 10), fg="#cceeee",
                 bg=BACKGROUND_COLOR, justify='left').pack(pady=20, padx=10)
        self.iconphoto(False, self.icon_data)
        self.update()


    def set_text(self, info=None, subinfo=None):
        """Обновляет текст статуса загрузки"""
        if info is not None:
            self.info_label.config(text=info)
        if subinfo is not None:
            self.subinfo_label.config(text=subinfo)
        self.update()


# Константы шрифтов
arial_9 = ("Arial", 9)
arial_10 = ("Arial", 10)
arial_11 = ("Arial", 11)
arial_12_bold = ("Arial", 12, "bold")



def open_directory(path):
    """Ваша функция открытия папок"""
    if not os.path.exists(path):
        messagebox.showerror("Ошибка", f"Путь не найден:\n{path}")
        return
    current_os = plt_module.system()
    if current_os == 'Windows':
        os.startfile(path)
    elif current_os == 'Darwin':
        subprocess.run(['open', path])
    else:
        subprocess.run(['xdg-open', path])


def create_row(parent, text, btn_text, folder_path):
    """Ваша функция создания строк с кнопками"""
    row_frame = ttk.Frame(parent)
    row_frame.pack(fill="x", anchor="n", pady=5)
    lbl = ttk.Label(row_frame, text=text, width=29, font=arial_11)
    lbl.pack(side="left", padx=5)
    btn = ttk.Button(row_frame, text=btn_text, width=25, command=lambda: open_directory(folder_path))
    btn.pack(side="left", padx=5)


def start_clicked(root, widgets):
    """Логика кнопки Start: Сброс -> Очистка -> Блокировка -> Запуск"""
    # 1. Сброс таймера в конфиге
    config.reset_time()

    # 2. Полная очистка лога и файла (инициализация заново)
    logger.init_logger(widgets)

    # 3. Первая запись [00:00:00.000]
    logger.write_log("Нажата кнопка [Start]", "info")

    # 4. Список исключений для блокировки (Кнопка Quit останется активной)
    exclude_list = [widgets['quit_button'], widgets['btn_stop']]

    # 5. Запуск через движок
    engine.run_in_thread(root, tasks.workflow_alpha, keep_enabled=exclude_list)



def create_ui(root):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # --- Стили ---
    style = ttk.Style()
    style.configure("TCheckbutton", font=arial_11)
    style.configure("TButton", font=arial_11)
    style.configure("TLabel", font=arial_11)
    default_bg = root.cget("bg")
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # --- Сетка окна ---
    root.columnconfigure(0, weight=1)
    root.rowconfigure(3, weight=1) # Только лог растягивается
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Ряд 0: Заголовок
    title_text = f"{NAM_PROG} {VER_PROG}"
    title_label = ttk.Label(root, text=title_text, font=arial_12_bold)
    title_label.grid(row=0, column=0, sticky='ew', padx=15, pady=(15, 5))
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Ряд 1: Опции (LabelFrames)
    options_frame = ttk.Frame(root)
    options_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
    options_frame.columnconfigure(0, weight=1)
    options_frame.columnconfigure(1, weight=1)

    frame_opts = tk.LabelFrame(options_frame, text="[ Файлы данных ]",
                               bg=default_bg, fg='#393939', padx=5, pady=5, font=arial_10)
    frame_reports = tk.LabelFrame(options_frame, text="[ Файлы настройки ]",
                                  bg=default_bg, fg='#393939', padx=5, pady=5, font=arial_10)

    frame_opts.grid(row=0, column=0, sticky='nsew', padx=5)
    frame_reports.grid(row=0, column=1, sticky='nsew', padx=5)
    options_frame.columnconfigure(0, weight=1, minsize=50)  # Колонка 0 не будет меньше 50px
    options_frame.columnconfigure(1, weight=10, minsize=260)  # Колонка 1 не будет меньше 250px
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    create_row(frame_opts, "Профили приборов учета:", "Открыть директорию", os.path.abspath(f"{PROFILES_DIR}"))
    create_row(frame_opts, "Цены на энергию:", "Открыть директорию", os.path.abspath(f"{PRICES_DIR}"))
    create_row(frame_opts, "Часы пиковой мощности:", "Открыть директорию", os.path.abspath(f"{CHASY_DIR}"))
    create_row(frame_opts, "Дополнительные данные:", "Открыть директорию", os.path.abspath(f"{DATA_DIR}"))
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Чекбоксы
    ttk.Checkbutton(frame_reports, text="Ведомость 4").pack(anchor='w')
    ttk.Checkbutton(frame_reports, text="Ведомость 4.1").pack(anchor='w')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Ряд 2: Статус
    status_period_frame = tk.LabelFrame(root, text="[ Статус ]", font=arial_10,
                                        bg=default_bg, fg='#393939', padx=5, pady=5)
    status_period_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=0)
    status_period_frame.columnconfigure(0, weight=1)

    status_label = ttk.Label(status_period_frame, text="Ожидание запуска…",
                             foreground='#000000', font=arial_11)
    status_label.grid(row=0, column=0, sticky='w')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Ряд 3: Область лога (ТЕМНАЯ)
    log_frame = ttk.Frame(root)
    log_frame.grid(row=3, column=0, sticky='nsew', padx=10, pady=5)
    log_area = tk.Text(log_frame, bg='#000000', fg='#bec2c6', relief='sunken', state='disabled')
    scrollbar = ttk.Scrollbar(log_frame, command=log_area.yview)
    log_area.config(yscrollcommand=scrollbar.set)
    log_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Ряд 4: Кнопки управления
    bottom_frame = ttk.Frame(root, padding="10")
    bottom_frame.grid(row=4, column=0, sticky='ew', padx=10, pady=(5, 10))
    bottom_frame.columnconfigure(3, weight=1)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Важно: команда запускает workflow через движок
    button1 = "Анализ ЦК"
    start_btn = ttk.Button(
        bottom_frame,
        text=button1,
        # command=lambda: (
        #    logger.init_logger(widgets), # Очищаем окно логов и файл
        #    config.reset_time(),  # Сброс общего таймера
        #    logger.write_log(f"Нажата кнопка [ {button1} ]", "but"),
        #    engine.run_in_thread(root, tasks.workflow_alpha)
        # )
        )
    start_btn.grid(row=0, column=0, padx=5)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    button2 = "Перерасчет тарифа"
    continue_btn = ttk.Button(bottom_frame, text=button2,
                              command=lambda: logger.write_log(f"Нажата кнопка [ {button2} ]", "but"))
    continue_btn.grid(row=0, column=1, padx=5)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def safe_exit(btn_name):
        if engine.is_running:
            answer = messagebox.askyesno(
                "Процесс запущен",
                "Задача выполняется. Попытаться безопасно остановить и выйти?",
                icon='warning', parent=root
            )
            if not answer: return

            # 1. Шлем сигнал остановки
            engine.request_stop()
            logger.write_log("Получен сигнал экстренной остановки...", "error")
            # Даем потоку 300мс на выход из цикла
            root.after(300)

        # 2. Обычная процедура выхода
        logger.write_log(f"Нажата кнопка [ {btn_name} ]", "but")
        logger.write_log("Завершение работы приложения...", "")
        # Сохраняем всё содержимое в файл
        logger.save_full_log()
        # Разблокируем кнопки (на всякий случай перед закрытием)
        engine.set_gui_state(root, tk.NORMAL)
        # Закрываем окно
        root.after(700, root.destroy)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Кнопка СТОП (новая)
    button00 = "Stop process"
    btn_stop = tk.Button(
        bottom_frame,
        text=button00,
        command=lambda: (
          logger.write_log(f"Нажата кнопка [ {button00} ]", "but"),
          engine.abort_process(root)),
        bg="blue",  # Цвет кнопки
        fg="white",  # Цвет текста
        activebackground="darkblue",  # Цвет при нажатии
        activeforeground="white")

    btn_stop.grid(row=0, column=2, padx=5, sticky='e')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    button3 = "Выход"
    quit_btn = tk.Button(
        bottom_frame,
        text=button3,
        command=lambda: safe_exit(button3),
        bg="red",              # Цвет кнопки
        fg="white",           # Цвет текста
        activebackground="darkred", # Цвет при нажатии
        activeforeground="white"
    )
    quit_btn.grid(row=0, column=3, sticky='w', padx=5)
    # Привязываем ту же логику к "крестику" окна
    buttonx = "✕"
    root.protocol("WM_DELETE_WINDOW", lambda: safe_exit(buttonx))
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    footer_label = ttk.Label(bottom_frame, text=f"{AUTOR}\n{JOB}",
                             font=arial_9, foreground='#555555', justify=tk.RIGHT)
    footer_label.grid(row=0, column=4, sticky='e', padx=10)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Настраиваем растягивание для root через columnconfigure и rowconfigure
    root.columnconfigure(0, weight=1)
    # Только ряд 3 (лог) будет растягиваться по вертикали
    root.rowconfigure(3, weight=1)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # СБОРКА СЛОВАРЯ WIDGETS
    widgets = {
        'log_area': log_area,
        'status_label_1': status_label,
        'start_button': start_btn,
        'quit_button': quit_btn,
        'btn_stop': btn_stop,
        'root': root
    }
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Назначаем команду кнопке Start теперь, когда widgets готов
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    start_btn.config(command=lambda: start_clicked(root, widgets))
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Инициализация подсистем
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    logger.init_logger(widgets)
    progress_manager.init_progress(log_area)
    return widgets
