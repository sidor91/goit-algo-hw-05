import timeit

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено


def build_shift_table(pattern):
  table = {}
  length = len(pattern)
  for index, char in enumerate(pattern[:-1]):
    table[char] = length - index - 1
  
  table.setdefault(pattern[-1], length)
  return table


def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1



def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    base = 256 
    modulus = 101  
    
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


# Завантаження тексту з файлу
def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

text1 = load_text("article1.txt")  # Скачай статтю з Google Drive і збережи під цим іменем
text2 = load_text("article2.txt")

# Підрядки для тесту
existing_substring = "наукове дослідження"  # має бути в тексті
non_existing_substring = "qwertyuiopasdfgh"  # точно не має бути

# Алгоритми і тексти
algorithms = {
    "KMP": kmp_search,
    "Boyer-Moore": boyer_moore_search,
    "Rabin-Karp": rabin_karp_search
}

texts = {
    "Article 1": text1,
    "Article 2": text2
}

# Вимірювання часу
def measure(algorithm, text, pattern):
    return timeit.timeit(lambda: algorithm(text, pattern), number=10)  # 10 повторів

results = {}

for text_name, text in texts.items():
    results[text_name] = {}
    for algo_name, algo_func in algorithms.items():
        t1 = measure(algo_func, text, existing_substring)
        t2 = measure(algo_func, text, non_existing_substring)
        results[text_name][algo_name] = {
            "existing": t1,
            "non_existing": t2
        }

# Вивід результатів
for text_name, res in results.items():
    print(f"\n=== {text_name} ===")
    for algo, times in res.items():
        print(f"{algo}:")
        print(f"  Знайдено:     {times['existing']:.6f} сек")
        print(f"  Не знайдено:  {times['non_existing']:.6f} сек")

"""
Загальні висновки
	•	Алгоритм Бойєра-Мура є найбільш ефективним серед трьох протестованих для обох текстів і в обох випадках (якщо підрядок існує і не існує в тексті). Його продуктивність пояснюється оптимізацією порівняння з кінця підрядка і використанням таблиці зсувів.
	•	Алгоритм Кнута-Морріса-Пратта має хорошу продуктивність, особливо при відсутності збігів, завдяки використанню префікс-функції, яка дозволяє уникати повторних перевірок.
	•	Алгоритм Рабіна-Карпа, хоча і використовує хешування для пришвидшення, у даному випадку працює повільніше через додаткові обчислення хешів, що не окупаються при пошуку одного підрядка.
"""