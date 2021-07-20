from pyAesCrypt import encryptFile, decryptFile
from Tools import check_password, load_hash_password_from_file


def checking_library_encoder(decorated_method):
    """ Decorator of encryption/decryption methods
        Декоратор методов шифрования/дешифрования """

    def wrapper(self, data):
        """ Method Wrapper
            Обёртка методов """

        if self.password is not None:
            try:
                return decorated_method(self, data)

            except ValueError:
                return -3   # Ошибка исполнения метода
        else:
            return -2       # Пароль не установлен

    return wrapper


class Scrambler:
    def __init__(self):
        self.buffer_size = 64 * 1024    # Размер буфера дешифровки
        self.password = None            # Пароль шифрования

    def set_library_encoder(self, entered_password, hash_stored_password_filename):
        """ Setting the Library Cryptographer
            Установка библиотечного шифровальщика """

        hash_stored_password = load_hash_password_from_file(hash_stored_password_filename)

        if not hash_stored_password:
            return -1   # Ошибка чтения из файла

        if not check_password(entered_password, hash_stored_password):
            return 0    # Пароли не идентичны

        self.password = entered_password

        return 1

    @checking_library_encoder
    def encrypt_file(self, filename):
        """ Encrypting a file with a password
            Шифрование файла по паролю """

        new_filename = filename.split('.')[0]
        encryptFile(filename, new_filename+".aes", self.password, self.buffer_size)

        return 1

    @checking_library_encoder
    def decrypt_file(self, filename):
        """ Decryption of the file with the password
            Дешифрование файла по паролю """

        new_filename = filename.split('.')[0]
        decryptFile(filename, new_filename+".txt", self.password, self.buffer_size)

        return 1


if __name__ == "__main__":
    """Тестирование модулей"""

    test_obj = Scrambler()
    test_obj.set_library_encoder(input("Пароль: "), "/home/kasper/Рабочий стол/PasswordsManager/pswrd")
    print(test_obj.decrypt_file("/home/kasper/Рабочий стол/Документ.aes"))
