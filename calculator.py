#!/usr/bin/env python3
"""
Простой CLI-калькулятор.
Запуск: py -3 calculator.py
"""

import operator


OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "**": operator.pow,
}


def calculate(a: float, op: str, b: float) -> float:
    if op not in OPS:
        raise ValueError(f"Неподдерживаемая операция: {op}")
    return OPS[op](a, b)


def main() -> None:
    try:
        raw = input("Введите выражение (пример: 2 + 3 или 2 ** 4): ").strip()
        if not raw:
            print("Пустой ввод. Завершение.")
            return
        parts = raw.split()
        if len(parts) != 3:
            print("Используйте формат: число операция число (пример: 10 / 4)")
            return
        a_str, op, b_str = parts
        a, b = float(a_str), float(b_str)
        result = calculate(a, op, b)
        print(f"Результат: {result}")
    except ZeroDivisionError:
        print("Ошибка: деление на ноль.")
    except ValueError as exc:
        print(f"Ошибка: {exc}")


if __name__ == "__main__":
    main()
