"""Калькулятор распределения наследства по заданным условиям (валюта: кроны)."""

from __future__ import annotations

import sys

# Настраиваем кодировку консоли на UTF-8.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")
except Exception:
    pass


def ask_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            value = float(raw)
            if value < 0:
                print("Введите неотрицательное число.")
                continue
            return value
        except ValueError:
            print("Не удалось распознать число, попробуйте еще раз.")


def ask_yes_no(prompt: str) -> bool:
    while True:
        raw = input(f"{prompt} (да/нет): ").strip().lower()
        if raw in {"да", "d", "y", "yes"}:
            return True
        if raw in {"нет", "n", "no"}:
            return False
        print("Ответьте 'да' или 'нет'.")


def ask_int(prompt: str, min_value: int = 0, max_value: int | None = None) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw:
            raw = "0"
        try:
            value = int(raw)
            if value < min_value:
                print(f"Введите число не меньше {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Введите число не больше {max_value}.")
                continue
            return value
        except ValueError:
            print("Нужно целое число, попробуйте еще раз.")


def main() -> None:
    if not sys.stdin.isatty():
        print("Этот скрипт требует интерактивного ввода. Запустите его в обычной консоли.")
        return

    print("=== Калькулятор наследства ===")
    marital_money = ask_float("Сколько денег было у вас в браке (общие деньги, NOK): ")
    personal_money = ask_float("Сколько у вас было личных денег (NOK): ")

    spouse_alive = ask_yes_no("Есть ли живая жена/муж")

    # Наследственная масса
    if spouse_alive:
        estate = marital_money / 2 + personal_money
    else:
        estate = marital_money + personal_money

    shares: dict[str, float] = {}
    remaining = estate

    # Супруг/супруга
    if spouse_alive:
        children_count = ask_int("Сколько у вас детей (число): ", min_value=0)

        if children_count > 0:
            spouse_share = max(estate / 4, 520_000)
            spouse_share = min(spouse_share, estate)  # если денег меньше порога
            shares["Супруг(а)"] = spouse_share
            remaining -= spouse_share

            child_share = remaining / children_count
            shares["Дети (каждый)"] = child_share
            remaining = 0.0
        else:
            parents_count = ask_int(
                "Сколько у вас живых родителей (0-2): ", min_value=0, max_value=2
            )

            if parents_count > 0:
                spouse_share = max(estate / 2, 780_000)
                spouse_share = min(spouse_share, estate)
                shares["Супруг(а)"] = spouse_share
                remaining -= spouse_share

                parent_share = remaining / parents_count if parents_count else 0.0
                shares["Родители (каждый)"] = parent_share
                remaining = 0.0
            else:
                grandparents_count = ask_int(
                    "Сколько у вас живых бабушек/дедушек: ", min_value=0
                )
                if grandparents_count > 0:
                    shares["Супруг(а)"] = estate  # супруг забирает все
                    remaining = 0.0
                else:
                    shares["Супруг(а)"] = estate  # других наследников нет
                    remaining = 0.0
    else:
        # Супруг(а) нет
        children_count = ask_int("Сколько у вас детей (число): ", min_value=0)
        if children_count > 0:
            child_share = estate / children_count
            shares["Дети (каждый)"] = child_share
            remaining = 0.0
        else:
            parents_count = ask_int(
                "Сколько у вас живых родителей (0-2): ", min_value=0, max_value=2
            )
            if parents_count > 0:
                parent_share = estate / parents_count if parents_count else 0.0
                shares["Родители (каждый)"] = parent_share
                remaining = 0.0
            else:
                grandparents_count = ask_int(
                    "Сколько у вас живых бабушек/дедушек: ", min_value=0
                )
                if grandparents_count > 0:
                    grand_share = estate / grandparents_count
                    shares["Бабушки/дедушки (каждый)"] = grand_share
                    remaining = 0.0

    print("\n--- Итоговое распределение ---")
    print(f"Наследственная масса: {estate:,.2f} NOK")
    if shares:
        for role, amount in shares.items():
            print(f"{role}: {amount:,.2f} NOK")
    else:
        print("Нет наследников по заданным условиям.")

    if remaining > 0:
        print(f"Нераспределено: {remaining:,.2f} NOK")


if __name__ == "__main__":
    main()
