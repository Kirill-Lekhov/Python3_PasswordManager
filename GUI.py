from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from time import time


from Scrambler import Scrambler


def entry_proc(entry, self):
    new_click_entry_time = time()

    if new_click_entry_time - self.last_click_entry_time < 0.5:
        filename = filedialog.askopenfilename(filetypes=[("All files", "*.*")])

        entry.delete(0, 'end')
        entry.insert(0, filename)

    self.last_click_entry_time = new_click_entry_time


class PasswordsManagerGUI(Tk):
    WindowSize = 300, 400

    @staticmethod
    def get_geometry(window):
        """ Calculating the window geometry (the window will be positioned exactly in the center of the screen)
            Вычисление геометрии окна (окно будет расположено ровно по центру экрана)"""

        display_size = window.winfo_screenwidth(), window.winfo_screenheight()
        display_center = display_size[0] // 2, display_size[1] // 2

        window_centering_offset = (display_center[0] - PasswordsManagerGUI.WindowSize[0] // 2,
                                   display_center[1] - PasswordsManagerGUI.WindowSize[1] // 2)

        window_size_string = "{}x{}+{}+{}".format(*list(map(str, [*PasswordsManagerGUI.WindowSize,
                                                                  *window_centering_offset])))
        return window_size_string

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scrambler = Scrambler()

        # Инициализация окна приложения
        self.title("Менеджер паролей")
        self.geometry(self.get_geometry(self))
        self.resizable(False, False)
        self.config(bg="white")

        parent_frame = Frame(self)
        parent_frame.pack(expand=True)
        parent_frame.grid_rowconfigure(0, weight=1)
        parent_frame.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for class_frame in (EnterPasswordPage, EncodingPage):
            frame_page = class_frame(parent_frame, self)
            self.frames[class_frame] = frame_page
            frame_page.grid(row=0, column=0, sticky='nsew')

        self.show_frame(EnterPasswordPage)

    def show_frame(self, class_frame):
        """ Changing the active frame
            Смена активного фрейма"""

        self.frames[class_frame].tkraise()


class EnterPasswordPage(Frame):
    def __init__(self, parent_frame, frame_controller):
        super().__init__(parent_frame)

        self.last_click_entry_time = 0
        self.config(bg="white")

        password_file_entry = Entry(self, width=30)
        password_entry = Entry(self, width=30)
        password_button = Button(self, text="Продолжить", width=20,
                                 command=lambda: self.button_proc(password_entry.get(),
                                                                  password_file_entry.get(),
                                                                  frame_controller))

        password_file_entry.bind("<Button-1>", lambda event: entry_proc(password_file_entry, self))
        password_file_entry.insert(0, "Введите путь до файла с ключом")
        password_entry.insert(0, "Введите пароль")
        password_button.config(bg="white")

        password_file_entry.pack()
        password_entry.pack()
        password_button.pack()

    @staticmethod
    def button_proc(password, password_file_path, frame_controller):
        result = frame_controller.scrambler.set_library_encoder(password, password_file_path)

        if result == -1:
            messagebox.showerror("Ошибка работы с файлами", "Не удалось прочитать файл")

        elif result == 0:
            messagebox.showerror("Ошибка сравнения паролей", "Пароли не совпадают")

        elif result == 1:
            frame_controller.show_frame(EncodingPage)


class EncodingPage(Frame):
    def __init__(self, parent_frame, frame_controller):
        super().__init__(parent_frame)

        self.last_click_entry_time = 0
        self.config(bg="white")

        path_entry = Entry(self, width=30)
        encrypt_button = Button(self, text="Зашифровать", width=20,
                                command=lambda: self.encrypt_proc(frame_controller, path_entry.get()))
        decrypt_button = Button(self, text="Расшифровать", width=20,
                                command=lambda: self.decrypt_proc(frame_controller, path_entry.get()))

        path_entry.bind('<Button-1>', lambda event: entry_proc(path_entry, self))
        path_entry.insert(0, "Выберите файл")
        encrypt_button.config(bg="white")
        decrypt_button.config(bg="white")

        path_entry.pack(pady=10.)
        encrypt_button.pack()
        decrypt_button.pack()

    @staticmethod
    def scrambler_result_messagebox(result, name_operation):
        if result != 1:
            messagebox.showerror(f"Ошибка {name_operation}", f"Во время {name_operation} произошла ошибка!")
            return

        messagebox.showinfo("Успех", f"Операция {name_operation} прошла успешно")

    @staticmethod
    def encrypt_proc(frame_controller, filepath):
        EncodingPage.scrambler_result_messagebox(frame_controller.scrambler.encrypt_file(filepath), "шифрования")

    @staticmethod
    def decrypt_proc(frame_controller, filepath):
        EncodingPage.scrambler_result_messagebox(frame_controller.scrambler.decrypt_file(filepath), "дешифрования")


if __name__ == "__main__":
    user_gui = PasswordsManagerGUI()
    user_gui.mainloop()
