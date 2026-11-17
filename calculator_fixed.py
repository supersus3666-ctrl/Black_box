"""
Улучшенная версия калькулятора (исправлены дефекты BUG-001 ... BUG-011).
"""
import math


class ExitRequested(Exception):
    """Пользователь ввёл 'exit' (или поток ввода закончился)."""


def read_raw(prompt):
    try:
        value = input(prompt).strip()
    except EOFError:
        raise ExitRequested
    if value.lower() == "exit":
        raise ExitRequested
    return value


def read_number(prompt):
    """Запрашивает число, пока не будет введено корректное конечное значение."""
    while True:
        text = read_raw(prompt).replace(",", ".")
        try:
            value = float(text)
        except ValueError:
            print(f"ОШИБКА ввода: '{text}' не является числом. Введите число, например 3.5")
            continue
        if not math.isfinite(value):
            print("ОШИБКА ввода: значения nan и inf не поддерживаются")
            continue
        return value


def read_operation(prompt):
    valid = {"+", "-", "*", "/", "sqrt", "power"}
    while True:
        op = read_raw(prompt).lower()
        if op in valid:
            return op
        print("ОШИБКА: Неизвестная операция! Допустимы: +, -, *, /, sqrt, power")


def calculate(op, a, b=None):
    """Возвращает результат или бросает ValueError с понятным сообщением."""
    if op == "sqrt":
        if a < 0:
            raise ValueError("Мнимые числа не поддерживаются!")
        return math.sqrt(a)
    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    elif op == "/":
        if b == 0:
            raise ValueError("Деление на ноль!")
        result = a / b
    else:  # power
        try:
            result = a ** b
        except ZeroDivisionError:
            raise ValueError("Деление на ноль (ноль в отрицательной степени)!")
        except OverflowError:
            raise ValueError("Результат слишком велик!")
        if isinstance(result, complex):
            raise ValueError("Результат не является вещественным числом!")
    if not math.isfinite(result):
        raise ValueError("Переполнение: результат слишком велик!")
    return result


def calculator():
    print("=" * 50)
    print("КАЛЬКУЛЯТОР (исправленная версия)")
    print("=" * 50)
    print("Операции: +, -, *, /, sqrt, power")
    print("Для выхода введите 'exit' в любой момент")
    print("=" * 50)
    while True:
        try:
            a = read_number("\nВведите первое число: ")
            op = read_operation("Введите операцию (+, -, *, /, sqrt, power): ")
            b = None if op == "sqrt" else read_number("Введите второе число: ")
            print(f"Результат: {calculate(op, a, b)}")
        except ValueError as e:
            print(f"ОШИБКА: {e}")
        except ExitRequested:
            print("До свидания!")
            break


if __name__ == "__main__":
    calculator()
