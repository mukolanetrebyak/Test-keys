import random
import math

def random_numbers(length): #генерація рандомних бітів
    numbers = []
    for _ in range(length):
        bit = random.choice([0, 1])
        numbers.append(bit)
    return numbers

def test_monobit(numbers):#тест на кількість одиниць і нулів 
    count_ones = sum(numbers)
    count_zeros = len(numbers) - count_ones
    s = abs(count_ones - count_zeros)
    p_value = math.erfc(s / math.sqrt(2 * len(numbers)))
    return p_value <= 0.01

def test_pokker(numbers): #тест на подібність покерних рук
    blocks = [numbers[i:i+4] for i in range(0, len(numbers), 4)]
    frequencies = [blocks.count(block) for block in blocks]
    chi_squared = sum((f - len(blocks)/16)**2 / (len(blocks)/16) for f in frequencies)
    p_value = math.erfc(chi_squared / 2)
    return p_value >= 0.01

def test_runs(numbers): #тест на кількість однакових бітів
    runs = [numbers[0]]
    for bit in numbers[1:]:
        if bit != runs[-1]:
            runs.append(bit)
    num_runs = len(runs)
    pi = sum(bit for bit in numbers) / len(numbers)
    expected_runs = 2 * pi * (1 - pi) * len(numbers) + 1
    variance = 2 * len(numbers) * (2 * len(numbers) - 1) / (len(numbers)**2 * (len(numbers) - 1))
    z_score = (num_runs - expected_runs) / math.sqrt(variance)
    p_value = math.erfc(abs(z_score) / math.sqrt(2))
    return p_value >= 0.01

def test_long(numbers): #тест на довгі серії однакових бітів
    max_run = 0
    current_run = 0
    for bit in numbers:
        if bit == 1:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 0
    p_value = math.erfc((max_run - 10) / (math.sqrt(20) * 2))
    return p_value >= 0.01

def tests(numbers):
    tests = [test_monobit, test_pokker, test_runs, test_long]
    results = [test(numbers) for test in tests]
    return all(results)

numbers = random_numbers(20000)
if tests(numbers):
    print("Послідовність бітів є достатньо випадковими.")
else:
    print("Послідовність бітів не є достатньо випадковими.")

