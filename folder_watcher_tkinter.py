import datetime
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Entry
from tkinter import Label


class Handler(PatternMatchingEventHandler):
    def on_created(self, event):
        callback(f"{datetime.datetime.now()}: {event.src_path} has been created")

    def on_deleted(self, event):
        callback(f"{datetime.datetime.now()}: {event.src_path} has been deleted")

    def on_modified(self, event):
        callback(f"{datetime.datetime.now()}: {event.src_path} has been modified")

    def on_moved(self, event):
        callback(f"{datetime.datetime.now()}: {event.src_path} moved to {event.dest_path}")


def start_observer(path):
    global observer, event_handler
    print(f"{datetime.datetime.now()}: Started watching {path}")
    callback(f"{datetime.datetime.now()}: Started watching {path}")
    observer.unschedule_all()
    observer.schedule(event_handler, path, recursive=True)
    if not observer.is_alive():
        observer.start()


def stop_observer():
    global observer
    observer.stop()
    if observer.is_alive():
        observer.join()


def callback(message): # функция, добавляющая сообщения обработчика в текстбокс
    global sctext_log
    sctext_log.configure(state='normal')
    sctext_log.insert('end', message+'\n')
    sctext_log.configure(state='disabled')
    return True


def exit():
    global root
    stop_observer()
    root.destroy()


def choose_dir():
    dir_path = filedialog.askdirectory()
    if dir_path:
        start_observer(dir_path)


def clear_journal():
    global sctext_log
    sctext_log.configure(state='normal')
    sctext_log.delete('1.0', tk.END)
    sctext_log.configure(state='disabled')


def get_format():
    global file_type
    global button_choose_dir
    global type_button
    button_choose_dir.configure(state='normal')
    create_event_handler(file_type)


def create_event_handler(file_type):
    global event_handler
    print(file_type.get())
    if file_type.get() is not None:
        str1 = '*' + file_type.get()

        event_handler = Handler(
            patterns=[str1],
            ignore_patterns=['cache/*'],
            ignore_directories=True,
            case_sensitive=False
        )
    else:
        event_handler = Handler(
            ignore_directories=False,
            case_sensitive=False
        )


def pause():
    global button_pause
    global observer
    observer.unschedule_all()


if __name__ == "__main__":

    event_handler = None
    observer = Observer()
    path = None
    # объявление элементов интерфейса
    root = tk.Tk()  # главное окно
    root.title("Folder watcher")  # его заголовок

    file_type = tk.StringVar()
    entered_format = Label(text="Enter file type (format: .type):", )
    entered_format.grid(row=0, column=0, sticky="w")
    format_entry = Entry(textvariable=file_type)  # поле для ввода типа
    format_entry.grid(row=0, column=1, padx=5, pady=5)
    type_button = ttk.Button(text="Ok", command=get_format)
    type_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

    button_choose_dir = ttk.Button(root, text='Choose a folder',
                                   command=choose_dir, state='disabled')  # кнопка выбора директории
    button_exit = ttk.Button(root, text='Exit', command=exit)  # кнопка выхода
    button_clear_journal = ttk.Button(root, text='Clear journal', command=clear_journal)  # очистка журнала
    button_pause = ttk.Button(root, text='Stop', command=pause)  # остановка отслеживания
    sctext_log = scrolledtext.ScrolledText(root, height=20, width=40, font=("Times New Roman", 12))  # окно журнала
    sctext_log.configure(state='disabled')  # нередактируемое
    # позиционирование элементов
    root.grid()
    root.grid_rowconfigure(1, weight=1)  # включаем реагирование столбцов/строк окна на его масштабирование
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    button_choose_dir.grid(row=2, column=0, pady=10, padx=10, sticky='ws')  # размещаем элементы
    button_pause.grid(row=2, column=1, pady=10, padx=10, sticky='s')
    button_clear_journal.grid(row=2, column=2, pady=10, padx=10, sticky='s')
    button_exit.grid(row=2, column=3, pady=10, padx=10, sticky='es')
    sctext_log.grid(row=1, columnspan=4, pady=10, padx=10, sticky='nesw')

    root.mainloop()  # запускаем работу основного потока программы
