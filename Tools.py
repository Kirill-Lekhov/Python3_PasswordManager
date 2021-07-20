from hashlib import md5


def check_password(entered_password, hash_stored_password):
    """ Checking whether the password entered by the user matches the password stored in the program
        Проверка совпадения пароля введенного пользователем с паролем хранимым в программе """

    hash_entered_password = md5(entered_password.encode("utf-8")).hexdigest()

    return hash_stored_password == hash_entered_password


def file_read_try(file_name):
    """ Error handler for opening/loading data from a file
        Обработчик ошибок открытия/загрузки данных из файла """

    try:
        with open(file_name, mode='r', encoding="utf-8") as file:
            return file.read()

    except FileNotFoundError:
        return ""


def load_hash_password_from_file(file_name):
    """ Loading a password in a hash form from a file
        Загрузка пароля в хэш форме из файла """

    return file_read_try(file_name).strip()


if __name__ == "__main__":
    """Тестирование модулей"""