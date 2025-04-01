import os
import json
import random
from random import randint, getrandbits
from typing import Tuple

# Быстрое возведение по модулю
def mod_pow(a: int, exp: int, mod: int) -> int:
    res = 1
    a = a % mod
    while exp > 0:
        if exp % 2 == 1:
            res = (res * a) % mod
        a = (a * a) % mod
        exp //= 2
    return res

# Генерация простого числа
def prime_generation(bits: int = 1024) -> int:
    while True:
        num = getrandbits(bits) | 1
        if is_prime(num):
            return num

# Проверка на простоту
def is_prime(n: int) -> bool:
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True

    n_min_1 = n - 1
    s = 0
    d = n_min_1

    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(5):
        a = randint(2, n - 2)
        x = mod_pow(a, d, n)
        if x == 1 or x == n_min_1:
            continue

        for _ in range(s - 1):
            x = mod_pow(x, 2, n)
            if x == n_min_1:
                break
        else:
            return False

    return True

# Перевод строки в число
def string_to_num(s: str) -> int:
    return int.from_bytes(s.encode('utf-8'), 'big')

# Перевод числа в байты
def num_to_string(n: int) -> bytes:
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')

# Расширенный алгоритм Евклида для НОД
def extended_gcd(a: int, b: int) -> tuple:
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Обратный элемент по модулю
def mod_inverse(e: int, phi: int) -> int:
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Обратного элемента не существует.")
    else:
        return x % phi

# Генерация ключей
def generate_key(bits: int = 1024) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    p = prime_generation(bits)
    q = prime_generation(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = mod_inverse(e, phi)
    return (e, n), (d, n)

# Функция сохранения сообщения в файл
def save_to_file(content: bytes, path: str = 'msg.txt') -> bool:
    if not path:
        path = 'msg.txt'
    try:
        with open(path, 'wb') as file:
            file.write(content)
        print(f"Сообщение успешно записано в файл: {path}")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        return False

# Сохранение ключей в файлы
def save_keys(public_key: Tuple[int, int], private_key: Tuple[int, int],
              public_key_path: str = 'public_key.json',
              private_key_path: str = 'private_key.json'):
    try:
        with open(public_key_path, 'w') as pub_file:
            # Преобразуем кортеж в список для записи
            json.dump(list(public_key), pub_file)
        with open(private_key_path, 'w') as priv_file:
            json.dump(list(private_key), priv_file)
        print("Ключи успешно сохранены.")
    except Exception as e:
        print("Ошибка при сохранении ключей:", e)

# Загрузка ключей из файлов
def load_keys(public_key_path: str = 'public_key.json',
              private_key_path: str = 'private_key.json'):
    if os.path.exists(public_key_path) and os.path.exists(private_key_path):
        try:
            with open(public_key_path, 'r') as pub_file:
                public_key = tuple(json.load(pub_file))
            with open(private_key_path, 'r') as priv_file:
                private_key = tuple(json.load(priv_file))
            print("Ключи успешно загружены.")
            return public_key, private_key
        except Exception as e:
            print("Ошибка при загрузке ключей:", e)
            return None, None
    else:
        return None, None

# Чтение из файла
def read_file(path: str):
    try:
        with open(path, 'rb') as file:
            content = file.read()
            print("Содержимое файла: ")
            print(content)
    except FileNotFoundError:
        print(f"Ошибка: файл по пути '{path}' не найден.")
    except IOError:
        print(f"Ошибка при чтении файла '{path}'")
    except Exception as e:
        print(f"Ошибка: {e}")

# Шифрование
def encrypt(msg: str, key: Tuple[int, int]):
    m = string_to_num(msg)
    e = key[0]
    n = key[1]
    c = mod_pow(m, e, n)
    path = input("Введите путь к файлу для сохранения зашифрованного сообщения: ")
    res = save_to_file(num_to_string(c), path)
    if res:
        print("Файл успешно создан или перезаписан.")
    else:
        print("Ошибка создания файла.")

# Расшифровка
def decrypt(path: str, key: Tuple[int, int]):
    try:
        with open(path, 'rb') as file:
            c = int.from_bytes(file.read(), 'big')
            d = key[0]
            n = key[1]
            m = mod_pow(c, d, n)
            return num_to_string(m).decode('utf-8')
    except Exception as e:
        print(f"Ошибка: {e}")

# Меню программы
def menu(public_key, private_key):
    print("1. Зашифровать сообщение")
    print("2. Расшифровать сообщение")
    print("3. Выход")
    choice = input()
    if choice == "1":
        print("Введите сообщение, которое хотите зашифровать:")
        msg = input()
        encrypt(msg, public_key)
        menu(public_key, private_key)
    elif choice == "2":
        print("Введите полный путь к файлу для расшифровки:")
        path = input()
        result = decrypt(path, private_key)
        print(f"Расшифрованное сообщение: {result}")
        menu(public_key, private_key)
    elif choice == "3":
        exit()
    else:
        print("Неверный ввод!")
        menu(public_key, private_key)

if __name__ == "__main__":
    public_key, private_key = load_keys()
    if public_key is None or private_key is None:
        print("Ключи не найдены, генерация новых ключей...")
        public_key, private_key = generate_key(1024)
        save_keys(public_key, private_key)
    else:
        print("Используем загруженные ключи.")

    print("Открытый ключ (e, n):", public_key)
    print("Закрытый ключ (d, n):", private_key)
    menu(public_key, private_key)