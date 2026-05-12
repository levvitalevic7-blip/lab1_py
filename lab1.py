"""
Лабораторна робота №1. Типи даних Python
"""

from __future__ import annotations

import copy
import datetime
import math
import os
import random
import re
import runpy
import string
import time
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent

# Якщо комп'ютер слабкий і тест на 10^6 записів виконується довго,
# можна запустити так:
# Windows PowerShell: $env:FAST_TEST="1"; python lab1_solution.py
# Linux / macOS: FAST_TEST=1 python lab1_solution.py
FAST_TEST = os.getenv("FAST_TEST") == "1"
BENCHMARK_SIZES = [10**2, 10**4, 10**5] if FAST_TEST else [10**2, 10**4, 10**6]


def section(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def read_text(filename: str) -> str:
    return (BASE_DIR / filename).read_text(encoding="utf-8")


def load_variable_from_py(filename: str, variable_name: str) -> Any:
    """Завантаження змінної з .py файлу, навіть якщо в імені файлу є дефіс."""
    data = runpy.run_path(str(BASE_DIR / filename))
    return data[variable_name]



# ЧАСТИНА 1. БАЗОВИЙ РІВЕНЬ


def tokenize_words(text: str) -> list[str]:
    """Повертає слова без цифр, пунктуації та спецсимволів."""
    return re.findall(r"[^\W\d_]+", text.lower(), flags=re.UNICODE)


def task_1_1_text_cleaner() -> None:
    section('Завдання 1.1 "Очищувач тексту"')

    text = read_text("bath-livingston.txt")
    words = tokenize_words(text)

    # Видаляємо артиклі a / the, але зберігаємо порядок і дублікати інших слів.
    cleaned_words = [word for word in words if word not in {"a", "the"}]
    unique_dictionary = set(cleaned_words)

    print("Кількість слів після очищення:", len(cleaned_words))
    print("Кількість унікальних слів:", len(unique_dictionary))
    print("Перші 30 слів очищеного списку:")
    print(cleaned_words[:30])
    print("Перші 30 унікальних слів у відсортованому вигляді:")
    print(sorted(unique_dictionary)[:30])


def format_article(article: str) -> str:
    """EL1005 -> EL-1005, DNF3761 -> DNF-3761."""
    return re.sub(r"^([A-Za-z]+)(\d+)$", r"\1-\2", article)


def task_1_2_assortment_analysis() -> None:
    section('Завдання 1.2 "Аналіз асортименту"')

    warehouse_1 = load_variable_from_py("assortment-analysis.py", "warehouse_1")
    warehouse_2 = load_variable_from_py("assortment-analysis.py", "warehouse_2")

    set_1 = set(warehouse_1)
    set_2 = set(warehouse_2)

    only_one_warehouse = set_1 ^ set_2
    all_unique = set_1 | set_2
    only_first = set_1 - set_2
    both = list(set_1 & set_2)
    formatted_sorted_articles = [format_article(article) for article in sorted(all_unique)]

    print("Товари лише на одному зі складів:", sorted(only_one_warehouse))
    print("Кількість унікальних товарів:", len(all_unique))
    print("Товари, які є хоча б на одному складі:", sorted(all_unique))
    print("Товари на першому складі, але відсутні на другому:", sorted(only_first))
    print("Товари, які є на обох складах, у вигляді списку:", sorted(both))
    print("Відсортований перелік усіх товарів із дефісом:")
    print(formatted_sorted_articles)


def remove_duplicates_in_place(items: list[list[Any]]) -> None:
    """Очищення списку від дублікатів in-place, без створення копії списку"""
    seen: set[tuple[Any, ...]] = set()
    index = 0

    while index < len(items):
        current = tuple(items[index])
        if current in seen:
            del items[index]
        else:
            seen.add(current)
            index += 1


def task_1_3_clean_list() -> None:
    section('Завдання 1.3 "Чистий список"')

    prices = load_variable_from_py("clean-list.py", "prices")

    print("Кількість записів до очищення:", len(prices))
    remove_duplicates_in_place(prices)
    print("Кількість записів після очищення:", len(prices))
    print("Очищений список:")
    for item in prices:
        print(item)


def top_items(counter: Counter, limit: int) -> list[tuple[Any, int]]:
    return counter.most_common(limit)


def analyze_language_units(text: str) -> dict[str, Any]:
    words = tokenize_words(text)

    word_counter = Counter(words)
    bigram_counter = Counter(zip(words, words[1:]))

    # беремо тільки літери, без пробілів, цифр і пунктуації
    char_counter = Counter(ch.lower() for ch in text if ch.isalpha())

    return {
        "words_count": len(words),
        "unique_words_count": len(word_counter),
        "top_3_words": top_items(word_counter, 3),
        "top_5_bigrams": top_items(bigram_counter, 5),
        "top_15_chars": top_items(char_counter, 15),
    }


def print_language_analysis(language_name: str, analysis: dict[str, Any]) -> None:
    print(f"\n--- {language_name} ---")
    print("Кількість слів:", analysis["words_count"])
    print("Кількість унікальних слів:", analysis["unique_words_count"])
    print("Топ-3 слова:", analysis["top_3_words"])
    print("Топ-5 біграм:")
    for bigram, count in analysis["top_5_bigrams"]:
        print(f"{bigram}: {count}")
    print("Топ-15 символів:", analysis["top_15_chars"])


def task_1_4_frequency_analysis() -> None:
    section('Завдання 1.4 "Частотний аналіз"')

    english_text = read_text("bester-eng.txt")
    russian_text = read_text("bester-rus.txt")

    english_analysis = analyze_language_units(english_text)
    russian_analysis = analyze_language_units(russian_text)

    print_language_analysis("Англійський текст", english_analysis)
    print_language_analysis("Російський текст", russian_analysis)


# ЧАСТИНА 2. СЕРЕДНІЙ РІВЕНЬ


def build_two_level_register(exam_results: list[tuple[str, str, int]]) -> dict[str, dict[str, int]]:
    register: dict[str, dict[str, int]] = {}

    for student, subject, grade in exam_results:
        if student not in register:
            register[student] = {}
        register[student][subject] = grade

    return register


def task_2_1_two_level_register() -> None:
    section('Завдання 2.1 "Дворівневий реєстр"')

    exam_results = load_variable_from_py("two-level-register.py", "exam_results")
    register = build_two_level_register(exam_results)

    print("Фрагмент вкладеного словника:")
    for student in list(register.keys())[:3]:
        print(student, "->", register[student])

    print("\nПриклади доступу O(1):")
    print('Shevchenko / Data Bases =', register["Shevchenko"]["Data Bases"])
    print('Petrenko / Algorithms =', register["Petrenko"]["Algorithms"])
    print('Lysenko / Databases Security =', register["Lysenko"]["Databases Security"])


def make_rbac_checker(role_permissions: dict[str, set[str]]):
    cache: dict[frozenset[str], set[str]] = {}

    def get_permissions(user_roles: list[str]) -> tuple[set[str], bool]:
        """
        Повертає підсумкові права та ознаку, чи взято результат із кешу
        Ключ кешу — frozenset,  порядок ролей не має значення
        """
        cache_key = frozenset(user_roles)

        if cache_key in cache:
            return cache[cache_key], True

        result_permissions: set[str] = set()
        for role in user_roles:
            result_permissions |= role_permissions.get(role, set())

        cache[cache_key] = result_permissions
        return result_permissions, False

    return get_permissions, cache


def task_2_2_rbac() -> None:
    section('Завдання 2.2 "Role-Based Access Control (RBAC)"')

    role_permissions = load_variable_from_py("rbac.py", "ROLE_PERMISSIONS")
    test_requests = load_variable_from_py("rbac.py", "test_requests")

    get_permissions, cache = make_rbac_checker(role_permissions)

    previous_by_key: dict[frozenset[str], int] = {}
    for number, roles in enumerate(test_requests, start=1):
        permissions, from_cache = get_permissions(roles)
        cache_key = frozenset(roles)
        object_id = id(permissions)

        same_object_note = ""
        if from_cache and previous_by_key.get(cache_key) == object_id:
            same_object_note = ", той самий об'єкт із кешу"
        previous_by_key[cache_key] = object_id

        source = "кеш" if from_cache else "обчислення"
        print(f"Запит {number:02d}: {roles} -> {sorted(permissions)} ({source}{same_object_note})")

    print("Кількість записів у кеші:", len(cache))


def vigenere_decrypt(cipher_text: str, key: str) -> str:
    alphabet = string.ascii_lowercase
    key_shifts = {letter: alphabet.index(letter) for letter in alphabet}
    decrypted: list[str] = []

    for index, char in enumerate(cipher_text):
        if char not in alphabet:
            decrypted.append(char)
            continue

        shift = key_shifts[key[index % len(key)]]

        # Використовуємо deque і rotate()
        shifted_alphabet = deque(alphabet)
        shifted_alphabet.rotate(-shift)

        plain_index = shifted_alphabet.index(char)
        decrypted.append(alphabet[plain_index])

    return "".join(decrypted)


def task_2_3_vigenere() -> None:
    section('Завдання 2.3 "Дешифратор Віженера"')

    encrypted_text = read_text("vigenere.txt").strip()
    key = "python"
    decrypted_text = vigenere_decrypt(encrypted_text, key)

    print("Зашифрований текст:", encrypted_text)
    print("Ключ:", key)
    print("Розшифрований текст:", decrypted_text)
    print("Пояснення:")
    print("deque.rotate() змінює чергу без створення нового рядка через slicing на кожному кроці.")
    print("Це зменшує кількість зайвих тимчасових об'єктів у пам'яті.")


def xor_bytes(message: bytes, key: bytes) -> bytes:
    if not key:
        raise ValueError("Ключ не може бути порожнім")

    return bytes(byte ^ key[index % len(key)] for index, byte in enumerate(message))


def task_2_4_xor() -> None:
    section('Завдання 2.4 "Бінарне шифрування XOR та bytes"')

    original_text = "Hello, Python XOR!"
    key_text = "custom key"

    encrypted = xor_bytes(original_text.encode("utf-8"), key_text.encode("utf-8"))
    decrypted = xor_bytes(encrypted, key_text.encode("utf-8")).decode("utf-8")

    print("Перевірка алгоритму:")
    print("Початковий текст:", original_text)
    print("Зашифровані bytes:", encrypted)
    print("Розшифрований текст:", decrypted)
    print("Співпадає з початковим:", decrypted == original_text)

    binary_message = (BASE_DIR / "xor-message.bin").read_bytes()
    binary_key = b"python"
    decoded_message = xor_bytes(binary_message, binary_key).decode("utf-8")

    print("\nРозшифрування xor-message.bin ключем 'python':")
    print(decoded_message)


# ЧАСТИНА 3. ВИСОКИЙ РІВЕНЬ


def get_similarity(storage: dict[Any, dict[Any, int]], user_a: Any, user_b: Any) -> float:
    profile_a = storage.get(user_a, {})
    profile_b = storage.get(user_b, {})

    if user_a == user_b and profile_a:
        return 1.0

    if not profile_a or not profile_b:
        return 0.0

    # Для ефективності ітеруємося за меншим профілем
    smaller, larger = (profile_a, profile_b) if len(profile_a) <= len(profile_b) else (profile_b, profile_a)

    dot_product = 0
    for item_id, count in smaller.items():
        dot_product += count * larger.get(item_id, 0)

    length_a = math.sqrt(sum(count ** 2 for count in profile_a.values()))
    length_b = math.sqrt(sum(count ** 2 for count in profile_b.values()))

    denominator = length_a * length_b
    if denominator == 0:
        return 0.0

    return dot_product / denominator


def update_purchase(storage: dict[Any, dict[Any, int]], user_id: Any, item_id: Any, delta: int) -> None:
    profile = storage.setdefault(user_id, {})
    new_count = profile.get(item_id, 0) + delta

    if new_count <= 0:
        profile.pop(item_id, None)
    else:
        profile[item_id] = new_count


def generate_task8_data(num_users: int = 10000) -> dict[str, dict[str, int]]:
    categories = ["Laptop", "Smartphone", "Headphones", "Camera", "Monitor", "Watch"]
    brands = ["Apple", "Samsung", "Sony", "Dell", "HP", "Logitech", "LG", "Canon"]
    models = ["Pro", "Air", "Ultra", "Max", "Plus", "GaminX", "Elite", "Series 5"]

    catalog = [f"{brand} {category} {model} {variant}"
               for brand in brands
               for category in categories
               for model in models
               for variant in range(2)]

    storage: dict[str, dict[str, int]] = {}
    for i in range(num_users):
        user_id = f"user_{i:05d}"
        item_count = random.randint(3, 15)
        bought = random.sample(catalog, item_count)
        storage[user_id] = {item: random.randint(1, 5) for item in bought}

    return storage


def benchmark_similarity() -> None:
    print("\nТаблиця часу для cosine similarity:")
    print(f"{'Кількість елементів':>22} | {'Час, секунд':>12} | {'Схожість':>10}")
    print("-" * 52)

    for size in BENCHMARK_SIZES:
        profile_a = {i: 1 for i in range(size)}
        profile_b = {i: 1 for i in range(size // 2, size + size // 2)}
        storage = {"A": profile_a, "B": profile_b}

        start = time.perf_counter()
        similarity = get_similarity(storage, "A", "B")
        elapsed = time.perf_counter() - start

        print(f"{size:>22} | {elapsed:>12.6f} | {similarity:>10.4f}")

        # Звільняємо пам'ять перед наступним тестом
        del profile_a, profile_b, storage


def task_3_1_recommendation_similarity() -> None:
    section("Завдання 3.1 Аналіз схожості покупців")

    storage = {
        "user_101": {"iPhone": 1, "AirPods": 1},
        "user_102": {"iPhone": 1, "MacBook": 1},
        "user_empty": {},
    }

    print("Приклад із завдання:")
    print('similarity(user_101, user_102) =', get_similarity(storage, "user_101", "user_102"))
    print('similarity(user_101, user_101) =', get_similarity(storage, "user_101", "user_101"))
    print('similarity(user_101, user_empty) =', get_similarity(storage, "user_101", "user_empty"))

    print("\nОновлення покупок:")
    update_purchase(storage, "user_101", "iPhone", 2)
    print("Після додавання 2 iPhone:", storage["user_101"])
    update_purchase(storage, "user_101", "AirPods", -1)
    print("Після зменшення AirPods на 1 товар видалено:", storage["user_101"])

    benchmark_similarity()


def tokenize_log_message(message: str) -> list[str]:
    # Дозволяємо дефіс усередині токена, щоб auth-service не розпадався повністю
    return re.findall(r"[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*", message.lower())


def build_message_index(logs: list[dict[str, Any]]) -> dict[str, set[int]]:
    index: dict[str, set[int]] = defaultdict(set)

    for log in logs:
        for token in tokenize_log_message(log["message"]):
            index[token].add(log["id"])

    return dict(index)


def build_exact_index(logs: list[dict[str, Any]], field_name: str) -> dict[Any, set[int]]:
    index: dict[Any, set[int]] = defaultdict(set)

    for log in logs:
        index[log[field_name]].add(log["id"])

    return dict(index)


def search_message_and(index: dict[str, set[int]], query: str) -> set[int]:
    tokens = tokenize_log_message(query)
    if not tokens:
        return set()

    result = index.get(tokens[0], set()).copy()
    for token in tokens[1:]:
        result &= index.get(token, set())

    return result


def search_logs(all_logs: list[dict[str, Any]], indexes: dict[str, dict[Any, set[int]]], **filters: Any) -> list[dict[str, Any]]:
    """Розумний пошук через перетин множин"""
    result_ids: set[int] | None = None

    for field_name, value in filters.items():
        if field_name not in indexes:
            raise KeyError(f"Немає індексу для поля {field_name}")

        current_ids = indexes[field_name].get(value, set())
        result_ids = current_ids.copy() if result_ids is None else result_ids & current_ids

    if result_ids is None:
        return []

    return [all_logs[i] for i in sorted(result_ids)]


def generate_task9_data(num_logs: int = 1000000) -> list[dict[str, Any]]:
    levels = ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]
    services = ["auth-gateway", "payment-processor", "inventory-db", "user-session-manager"]
    actions = ["connected to", "failed to process", "successfully updated", "timed out during", "rejected request from"]
    resources = ["database", "s3-bucket", "external-api", "redis-cache", "oauth-provider"]
    start_time = datetime.datetime.now()

    logs: list[dict[str, Any]] = []
    for i in range(num_logs):
        service = services[i % len(services)]
        action = actions[i % len(actions)]
        resource = resources[i % len(resources)]

        log_entry = {
            "id": i,
            "timestamp": (start_time + datetime.timedelta(milliseconds=i * 10)).isoformat(),
            "level": levels[i % len(levels)],
            "service": service,
            "trace_id": f"TRC-{i % 50000:06d}",
            "message": f"Service {service} {action} {resource}",
        }
        logs.append(log_entry)

    return logs


def generate_trace_logs(num_logs: int) -> list[dict[str, Any]]:
    """Мінімальні логи для тесту унікального trace_id"""
    return [{"id": i, "trace_id": f"TRC-{i:06d}"} for i in range(num_logs)]


def build_unique_trace_index(logs: list[dict[str, Any]]) -> dict[str, int]:
    return {log["trace_id"]: log["id"] for log in logs}


def benchmark_trace_search() -> None:
    target_trace_id = "TRC-000050"

    print("\nПорівняння пошуку за унікальним TraceID:")
    print(f"{'Кількість логів':>18} | {'Прямий перебір, с':>17} | {'Індекс, с':>10} | {'ID знайдено':>10}")
    print("-" * 69)

    for size in BENCHMARK_SIZES:
        logs = generate_trace_logs(size)
        trace_index = build_unique_trace_index(logs)

        start_scan = time.perf_counter()
        # Не зупиняємось на першому збігу, а переглядаємо весь список
        # Так добре видно лінійну складність прямого перебору O(N)
        scan_result = [log["id"] for log in logs if log["trace_id"] == target_trace_id]
        scan_time = time.perf_counter() - start_scan

        start_index = time.perf_counter()
        index_result = trace_index.get(target_trace_id)
        index_time = time.perf_counter() - start_index

        print(f"{size:>18} | {scan_time:>17.8f} | {index_time:>10.8f} | {str(index_result):>10}")

        assert scan_result == [index_result]
        del logs, trace_index


def task_3_2_inverted_index() -> None:
    section("Завдання 3.2 Повнотекстовий пошук")

    logs = [
        {
            "id": 0,
            "trace_id": "TRC-101",
            "service": "auth-gateway",
            "level": "ERROR",
            "message": "User login failed: invalid password.",
        },
        {
            "id": 1,
            "trace_id": "TRC-102",
            "service": "payment-processor",
            "level": "ERROR",
            "message": "Payment failed: connection timeout.",
        },
        {
            "id": 2,
            "trace_id": "TRC-103",
            "service": "auth-gateway",
            "level": "INFO",
            "message": "User login success.",
        },
    ]

    message_index = build_message_index(logs)
    level_index = build_exact_index(logs, "level")
    service_index = build_exact_index(logs, "service")
    trace_index = build_exact_index(logs, "trace_id")

    print("Індекс повідомлень:")
    for token, ids in sorted(message_index.items()):
        print(token, "->", ids)

    query = "failed login"
    result_ids = search_message_and(message_index, query)
    print(f"\nРезультат пошуку '{query}' через перетин множин:", result_ids)
    print("Знайдені логи:", [logs[i] for i in sorted(result_ids)])

    indexes = {
        "level": level_index,
        "service": service_index,
        "trace_id": trace_index,
    }
    smart_results = search_logs(logs, indexes, level="ERROR", service="auth-gateway")
    print("\nSmart Search level='ERROR' AND service='auth-gateway':")
    print(smart_results)

    benchmark_trace_search()


DELETED = "<DELETED>"


def get_diff(old_dict: dict[str, Any], new_dict: dict[str, Any], path: str = "") -> dict[str, Any]:
    changes: dict[str, Any] = {}
    all_keys = set(old_dict.keys()) | set(new_dict.keys())

    for key in all_keys:
        current_path = f"{path}.{key}" if path else str(key)

        if key not in old_dict:
            changes[current_path] = new_dict[key]
        elif key not in new_dict:
            changes[current_path] = DELETED
        else:
            old_value = old_dict[key]
            new_value = new_dict[key]

            if isinstance(old_value, dict) and isinstance(new_value, dict):
                changes.update(get_diff(old_value, new_value, current_path))
            elif old_value != new_value:
                changes[current_path] = new_value

    return changes


def set_by_dot_path(data: dict[str, Any], dot_path: str, value: Any) -> None:
    keys = dot_path.split(".")
    current = data

    for key in keys[:-1]:
        current = current.setdefault(key, {})

    if value == DELETED:
        current.pop(keys[-1], None)
    else:
        current[keys[-1]] = value


def merge_versions(base: dict[str, Any], version_a: dict[str, Any], version_b: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    diff_a = get_diff(base, version_a)
    diff_b = get_diff(base, version_b)

    merged = copy.deepcopy(base)
    conflicts: list[dict[str, Any]] = []

    for path, value in diff_a.items():
        set_by_dot_path(merged, path, value)

    for path, value_b in diff_b.items():
        if path in diff_a and diff_a[path] != value_b:
            conflicts.append({
                "path": path,
                "user_a_value": diff_a[path],
                "user_b_value": value_b,
            })
        else:
            set_by_dot_path(merged, path, value_b)

    return merged, conflicts


def get_random_path(d: Any, current_path: list[str] | None = None) -> list[str]:
    if current_path is None:
        current_path = []

    if not isinstance(d, dict):
        return current_path

    key = random.choice(list(d.keys()))
    current_path.append(key)
    return get_random_path(d[key], current_path)


def set_by_path(d: dict[str, Any], path: list[str], value: Any) -> None:
    current = d
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = value


def generate_task3_stress_test(depth: int = 5, width: int = 3) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    def gen(level: int) -> Any:
        if level == 0:
            return random.randint(1, 100)
        return {f"node_{i}": gen(level - 1) for i in range(width)}

    v0 = gen(depth)
    v1 = copy.deepcopy(v0)
    v2 = copy.deepcopy(v0)

    for _ in range(3):
        path = get_random_path(v0)
        set_by_path(v1, path, random.randint(1000, 2000))

    for _ in range(3):
        path = get_random_path(v0)
        set_by_path(v2, path, random.randint(3000, 4000))

    return v0, v1, v2


def task_3_3_recursive_diff() -> None:
    section("Завдання 3.3 Рекурсивний Diff вкладених структур")

    v0 = {
        "system": {
            "network": {"ip": "192.168.1.1", "dns": "8.8.8.8"},
            "display": {"brightness": 70, "theme": "light"},
        },
        "user": {"name": "Admin", "role": "root"},
    }

    print("Приклад без конфлікту:")
    v1_no_conflict = copy.deepcopy(v0)
    v2_no_conflict = copy.deepcopy(v0)
    v1_no_conflict["system"]["display"]["brightness"] = 80
    v1_no_conflict["user"]["name"] = "Administrator"
    v2_no_conflict["system"]["network"]["dns"] = "1.1.1.1"
    v2_no_conflict["system"]["display"]["theme"] = "dark"

    print("Diff користувача A:", get_diff(v0, v1_no_conflict))
    print("Diff користувача B:", get_diff(v0, v2_no_conflict))
    merged, conflicts = merge_versions(v0, v1_no_conflict, v2_no_conflict)
    print("Об'єднана версія:", merged)
    print("Конфлікти:", conflicts)

    print("\nПриклад із конфліктом:")
    v1_conflict = copy.deepcopy(v0)
    v2_conflict = copy.deepcopy(v0)
    v1_conflict["system"]["display"]["brightness"] = 80
    v2_conflict["system"]["display"]["brightness"] = 40
    v2_conflict["system"]["network"]["ip"] = "192.168.1.2"

    merged_conflict, conflicts_conflict = merge_versions(v0, v1_conflict, v2_conflict)
    print("Diff користувача A:", get_diff(v0, v1_conflict))
    print("Diff користувача B:", get_diff(v0, v2_conflict))
    print("Об'єднана версія:", merged_conflict)
    print("Конфлікти:", conflicts_conflict)

    print("\nСтрес-тест глибиною 5 рівнів:")
    random.seed(42)
    stress_v0, stress_v1, stress_v2 = generate_task3_stress_test(depth=5, width=3)
    stress_diff_a = get_diff(stress_v0, stress_v1)
    stress_diff_b = get_diff(stress_v0, stress_v2)
    stress_merged, stress_conflicts = merge_versions(stress_v0, stress_v1, stress_v2)

    print("Перші зміни користувача A:", dict(list(stress_diff_a.items())[:5]))
    print("Перші зміни користувача B:", dict(list(stress_diff_b.items())[:5]))
    print("Кількість конфліктів:", len(stress_conflicts))
    print("Приклад конфліктів:", stress_conflicts[:3])
    print("Тип результату після merge:", type(stress_merged).__name__)


# ЗАПУСК УСІЄЇ ЛАБОРАТОРНОЇ


def main() -> None:
    print("Лабораторна робота №1. Типи даних Python")
    print("Режим швидкого тесту:", FAST_TEST)
    print("Розміри для замірів продуктивності:", BENCHMARK_SIZES)

    task_1_1_text_cleaner()
    task_1_2_assortment_analysis()
    task_1_3_clean_list()
    task_1_4_frequency_analysis()

    task_2_1_two_level_register()
    task_2_2_rbac()
    task_2_3_vigenere()
    task_2_4_xor()

    task_3_1_recommendation_similarity()
    task_3_2_inverted_index()
    task_3_3_recursive_diff()


if __name__ == "__main__":
    main()
