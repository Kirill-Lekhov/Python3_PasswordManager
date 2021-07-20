from hashlib import md5


def get_hash(string: str) -> str:
    return md5(string.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    print("Хэш-код строки:", get_hash(input("Введите строку: ")))
